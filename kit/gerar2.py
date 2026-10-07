"""Gera os posts do @verdades_atemporais com uma cena inédita por slide.

Uso:  python3 gerar2.py lote.json cenas.json pasta_das_fotos pasta_de_saida [--debug]

- lote.json: os posts (mesmo formato de sempre: linhas/destaque/apoio, placas com branca/preta, lacuna).
- cenas.json: para cada slide ("821-01"), a foto e o estilo da escrita:
    {"821-01": {"estilo": "marcador", "semente": [540, 600], "tinta": "#1b1b1b", ...}}
  Campos opcionais: "quad" (4 pontos x,y em 1080x1350), "caixa" [x0,y0,x1,y1], "semente" [x,y]
  (ponto dentro da superfície em branco para detectar a área), "folga" (margem interna, 0-0.3),
  "zoom" [cx, cy, escala], "giro" (graus), "tol" (tolerância da detecção), "max" (fonte máxima).
- pasta_das_fotos: {slide}.png ou .jpg (ex.: 821-01.png), qualquer tamanho com proporção ~4:5.
"""
import pathlib, asyncio, html, json, sys
import numpy as np, cv2
from PIL import Image, ImageChops, ImageFilter
from playwright.async_api import async_playwright

S = pathlib.Path(__file__).parent
sys.path.insert(0, str(S))
from gerar import CORES, NEON, cor_do_numero  # mesma sequência de cores da página

W, H = 1080, 1350
e = html.escape
HANDLE = '@verdades_atemporais'

def furi(nome):
    return (S / 'fonts' / nome).as_uri().replace('[', '%5B').replace(']', '%5D').replace(',', '%2C')

FONTES = {
    'AR': ('Archivo[wdth,wght].ttf', '100 900'), 'CAV': ('caveat-latin-700-normal.woff2', '700'),
    'CAV5': ('caveat-latin-500-normal.woff2', '500'), 'KAL': ('kalam-latin-700-normal.woff2', '700'),
    'KAL4': ('kalam-latin-400-normal.woff2', '400'), 'PM': ('permanent-marker-latin-400-normal.woff2', '400'),
    'SE': ('special-elite-latin-400-normal.woff2', '400'), 'GH': ('gochi-hand-latin-400-normal.woff2', '400'),
    'PAC': ('pacifico-latin-400-normal.woff2', '400'), 'DOTO': ('doto-latin-800-normal.woff2', '800'),
    'CP': ('courier-prime-latin-700-normal.woff2', '700'), 'CP4': ('courier-prime-latin-400-normal.woff2', '400'),
    'DMS': ('dm-serif-display-latin-400-normal.woff2', '400'), 'RS': ('rock-salt-latin-400-normal.woff2', '400'),
    'CS': ('cabin-sketch-latin-700-normal.woff2', '700'),
}
FONT_CSS = ''.join(f"@font-face{{font-family:'{k}';src:url('{furi(f)}');font-weight:{w}}}" for k, (f, w) in FONTES.items())

# estilos de escrita. modo: mult (tinta sobre superfície clara) | screen (luz/giz sobre superfície escura)
ESTILOS = {
    'marcador':  dict(fonte='PM', tinta='#1c1c1e', caixa=None, lh=1.02, apoio='KAL4', hl='marca', modo='mult', giro=-1.5),
    'caneta':    dict(fonte='CAV', tinta='#1f3a8a', caixa=None, lh=0.95, apoio='CAV5', hl='marca', modo='mult', giro=-2),
    'mao':       dict(fonte='KAL', tinta='#222', caixa=None, lh=1.05, apoio='KAL4', hl='marca', modo='mult', giro=-1),
    'lapis':     dict(fonte='CAV', tinta='#4a4a4a', caixa=None, lh=0.95, apoio='CAV5', hl='marca', modo='mult', giro=-1.5, grao=0.35),
    'giz_cera':  dict(fonte='GH', tinta='#2b59c3', caixa=None, lh=1.0, apoio='GH', hl='marca', modo='mult', giro=-2, grao=0.45, multicor=True),
    'maquina':   dict(fonte='SE', tinta='#222', caixa=None, lh=1.12, apoio='SE', hl='sublinha', modo='mult', giro=0, grao=0.25),
    'recibo':    dict(fonte='CP', tinta='#2a2a2a', caixa='upper', lh=1.08, apoio='CP4', hl='inverso', modo='mult', giro=0, grao=0.3, recibo=True),
    'carimbo':   dict(fonte='SE', tinta='#2b2b2b', caixa='upper', lh=1.05, apoio='SE', hl='cor', modo='mult', giro=-3, grao=0.5),
    'impresso':  dict(fonte='AR', tinta='#141414', caixa='upper', lh=0.9, apoio='AR', hl='bloco', modo='mult', giro=0, peso=900),
    'serifa':    dict(fonte='DMS', tinta='#1a1a1a', caixa=None, lh=1.0, apoio='CAV5', hl='marca', modo='mult', giro=0),
    'tela':      dict(fonte='AR', tinta='#111', caixa=None, lh=1.05, apoio='AR', hl='marca', modo='mult', giro=0, peso=800, tela=True),
    'pincel':    dict(fonte='PM', tinta='#1c1c1e', caixa='upper', lh=1.0, apoio='PM', hl='cor_escura', modo='mult', giro=-2),
    'batom':     dict(fonte='RS', tinta='#c1121f', caixa=None, lh=1.25, apoio='RS', hl='nenhum', modo='mult', giro=-4, alfa=0.9),
    'letreiro':  dict(fonte='AR', tinta='#141414', caixa='upper', lh=1.0, apoio='AR', hl='nenhum', modo='mult', giro=0, peso=800, ls='0.04em', estreito=80),
    'giz':       dict(fonte='CS', tinta='#f2f2ee', caixa='upper', lh=1.0, apoio='CAV5', hl='cor', modo='screen', giro=-1, grao=0.55),
    'feltro':    dict(fonte='AR', tinta='#f4f4f0', caixa='upper', lh=1.12, apoio='AR', hl='nenhum', modo='screen', giro=0, peso=700, ls='0.08em', estreito=75),
    'neon':      dict(fonte='PAC', tinta='#ffffff', caixa=None, lh=1.15, apoio='PAC', hl='cor', modo='screen', giro=-3, neon=True),
    'led':       dict(fonte='DOTO', tinta='#ffb400', caixa='upper', lh=1.08, apoio='DOTO', hl='cor', modo='screen', giro=0, led=True),
}

def linhas_do_slide(sl):
    """lista de (texto, destaque) + apoio + lacuna"""
    if 'branca' in sl:
        ls = [(t, False) for t in sl['branca']] + [(sl['preta'][0], False), (sl['preta'][1], True)]
        return ls, sl.get('apoio'), False
    ls = [(t, False) for t in sl.get('linhas', [])]
    if sl.get('destaque'):
        ls.append((sl['destaque'], True))
    return ls, sl.get('apoio'), bool(sl.get('lacuna'))

def ordenar(p):
    p = np.array(p, dtype=np.float32).reshape(-1, 2)
    s, d = p.sum(1), np.diff(p, axis=1).ravel()
    return np.float32([p[np.argmin(s)], p[np.argmin(d)], p[np.argmax(s)], p[np.argmax(d)]])

def detectar(img, semente, tol=28):
    a = cv2.GaussianBlur(np.array(img), (0, 0), 2.2)
    mask = np.zeros((H + 2, W + 2), np.uint8)
    cv2.floodFill(a.copy(), mask, tuple(int(v) for v in semente), (0, 0, 0), (tol,) * 3, (tol,) * 3,
                  flags=4 | cv2.FLOODFILL_MASK_ONLY | cv2.FLOODFILL_FIXED_RANGE | (255 << 8))
    m = cv2.morphologyEx(mask[1:-1, 1:-1], cv2.MORPH_CLOSE, np.ones((41, 41), np.uint8))
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key=cv2.contourArea)
    hull = cv2.convexHull(c)
    peri = cv2.arcLength(hull, True)
    for eps in np.linspace(0.005, 0.08, 40):
        ap = cv2.approxPolyDP(hull, eps * peri, True)
        if len(ap) == 4:
            return ordenar(ap), m
    return ordenar(cv2.boxPoints(cv2.minAreaRect(c))), m

def encolher(q, f):
    c = q.mean(0)
    return np.float32([c + (p - c) * (1 - f) for p in q])

def preparar(foto, zoom=None):
    im = Image.open(foto).convert('RGB')
    w, h = im.size
    if zoom:
        cx, cy, z = zoom
        cw, ch = w / z, w / z * 1.25
        if ch > h / z * 1.0001:
            ch = h / z; cw = ch * 0.8
        x0 = min(max(cx * w / W - cw / 2, 0), w - cw); y0 = min(max(cy * h / H - ch / 2, 0), h - ch)
        im = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))
    else:
        if w / h > 0.8:
            nw = h * 0.8; im = im.crop((int((w - nw) / 2), 0, int((w + nw) / 2), h))
        else:
            nh = w / 0.8; im = im.crop((0, int((h - nh) / 2), w, int((h + nh) / 2)))
    return im.resize((W, H), Image.LANCZOS)

FIT = """<script>
document.fonts.ready.then(()=>{
 const box=document.querySelector('.box'), t=document.querySelector('.txt'); let s=+t.dataset.max;
 const cs=getComputedStyle(box), pw=parseFloat(cs.paddingLeft)*2, ph=parseFloat(cs.paddingTop)*2;
 const cw=box.clientWidth-pw, ch=box.clientHeight-ph;
 const over=()=>t.offsetWidth>cw+1||t.offsetHeight>ch+1||[...t.querySelectorAll('.l')].some(d=>d.scrollWidth>cw+1);
 t.style.fontSize=s+'px'; while(over()&&s>14){s-=2;t.style.fontSize=s+'px';}
 document.body.dataset.ready=1;});
</script>"""

def html_texto(est, cfg, linhas, apoio, lacuna, cor, bw, bh):
    E = dict(ESTILOS[est]); E.update({k: v for k, v in cfg.items() if k in ('tinta', 'giro', 'caixa', 'hl', 'fonte', 'apoio_fonte', 'alinhar')})
    tinta = E['tinta']; corp = CORES[cor]; neon = NEON[cor]
    escuro = E['modo'] == 'screen'
    up = 'uppercase' if E.get('caixa') == 'upper' else 'none'
    peso = E.get('peso', 'normal'); ls = E.get('ls', '0'); st = f"font-stretch:{E['estreito']}%;" if E.get('estreito') else ''
    alinhar = cfg.get('alinhar', 'center' if est in ('neon', 'led', 'feltro', 'letreiro', 'giz', 'batom', 'impresso', 'pincel', 'carimbo') else 'left')
    multicor = ['#2b59c3', '#d62828', '#2a9d3c', '#e76f00', '#7b2cbf'] if E.get('multicor') else None
    hlmode = E['hl']
    linhas_html = []
    for i, (t, dest) in enumerate(linhas):
        tx = e(t)
        estilo_l = f"color:{multicor[i % len(multicor)]};" if multicor and not dest else ''
        if dest:
            if hlmode == 'marca': tx = f"<span class='mk'>{tx}</span>"
            elif hlmode == 'bloco': tx = f"<span class='bk'>{tx}</span>"
            elif hlmode == 'inverso': tx = f"<span class='iv'>{tx}</span>"
            elif hlmode == 'sublinha': tx = f"<span class='ul'>{tx}</span>"
            elif hlmode == 'cor': tx = f"<span style='color:{neon if escuro else cfg.get('cor_destaque', '#b3261e')}'>{tx}</span>"
            elif hlmode == 'cor_escura': tx = f"<span style='color:{cfg.get('cor_destaque', '#b3261e')}'>{tx}</span>"
        linhas_html.append(f"<div class='l' style='{estilo_l}'>{tx}</div>")
    if lacuna:
        linhas_html.append("<div class='l'><span class='lac'>&nbsp;</span></div>")
    if cfg.get('uma_linha'):
        linhas_html = ["<div class='l'>" + ' '.join(h[h.index('>') + 1:-6] for h in linhas_html) + "</div>"]
    ap = ''
    if apoio and not cfg.get('sem_apoio'):
        ap = '<br>'.join(e(x) for x in apoio.split('|'))
        afonte = cfg.get('apoio_fonte', E['apoio'])
        apeso = '600' if afonte == 'AR' else 'normal'
        ap = f"<div class='ap' style=\"font-family:'{afonte}';font-weight:{apeso}\">{ap}</div>"
    glow = ''
    if E.get('neon'):
        glow = (f".txt{{color:#fff;text-shadow:0 0 .04em #fff,0 0 .12em {neon},0 0 .3em {neon},0 0 .6em {neon},0 0 1.1em {neon}}}"
                f".ap{{color:#fff;text-shadow:0 0 .05em #fff,0 0 .2em {neon},0 0 .5em {neon}}}")
    if E.get('led'):
        glow = (f".txt,.ap{{color:{cfg.get('tinta', '#ffb400')};text-shadow:0 0 .05em {cfg.get('tinta', '#ffb400')},0 0 .25em {cfg.get('tinta', '#ffb400')}}}")
    recibo = ''
    if E.get('recibo'):
        recibo = "<div class='l rc'>* * * * * * * * *</div>"
    tela = ''
    if E.get('tela'):
        tela = "<div class='tb'><span>‹ Notas</span><span>Concluído</span></div>"
    giro = cfg.get('giro', E['giro'])
    fundo = '#000' if escuro else '#fff'
    pad = cfg.get('pad', '0.06')
    return f"""<!doctype html><html><head><meta charset='utf-8'><style>{FONT_CSS}
*{{margin:0;box-sizing:border-box}}
body{{width:{bw}px;height:{bh}px;background:{fundo};overflow:hidden}}
.box{{position:absolute;inset:0;padding:{float(pad) * min(bw, bh):.0f}px;display:flex;flex-direction:column;justify-content:center;
  align-items:{'center' if alinhar == 'center' else 'flex-start'};text-align:{alinhar};transform:rotate({giro}deg)}}
.txt{{font-family:'{E['fonte']}';font-weight:{peso};{st}color:{tinta};line-height:{E['lh']};text-transform:{up};letter-spacing:{ls}}}
.l{{white-space:nowrap;width:max-content}}
.mk{{background:linear-gradient(176deg,transparent 18%,{corp} 22%,{corp} 86%,transparent 90%);padding:0 .12em;margin:0 -.06em;border-radius:.2em .5em .3em .6em;-webkit-box-decoration-break:clone}}
.bk{{background:{corp};padding:.02em .12em 0;margin-left:-.1em}}
.iv{{background:{tinta};color:#fff;padding:0 .15em}}
.ul{{text-decoration:underline;text-decoration-color:{corp};text-decoration-thickness:.12em;text-underline-offset:.12em}}
.lac{{display:inline-block;width:4.2em;border-bottom:.08em solid {corp if not escuro else neon};margin-left:.1em}}
.ap{{margin-top:.7em;font-size:.42em;line-height:1.2;color:{tinta};white-space:normal;max-width:100%;text-transform:none;letter-spacing:0}}
.rc{{font-size:.5em;opacity:.8;margin:.2em 0}}
.tb{{position:absolute;top:0;left:0;right:0;display:flex;justify-content:space-between;padding:{bh*0.02:.0f}px {bw*0.05:.0f}px;font:600 {bh*0.03:.0f}px 'AR';color:#e0a800}}
{glow}
</style></head><body><div class='box'><div class='txt' data-max='{cfg.get('max', 400)}'>{recibo if recibo else ''}{''.join(linhas_html)}{recibo}{ap}</div></div>{tela}{FIT}</body></html>"""

def textura(layer, forca, escuro, seed=1):
    if not forca:
        return layer
    rng = np.random.default_rng(seed)
    n = rng.random((layer.size[1], layer.size[0])).astype(np.float32)
    n = cv2.GaussianBlur(n, (0, 0), 0.9)
    n = (n - n.min()) / (n.max() - n.min())
    k = 1 - forca + forca * n
    a = np.array(layer).astype(np.float32)
    if escuro:
        a = a * k[..., None]
    else:
        a = 255 - (255 - a) * k[..., None]
    return Image.fromarray(a.clip(0, 255).astype('uint8'))

def warp(layer, quad, fundo):
    w, h = layer.size
    M = cv2.getPerspectiveTransform(np.float32([(0, 0), (w, 0), (w, h), (0, h)]), quad)
    return Image.fromarray(cv2.warpPerspective(np.array(layer), M, (W, H), flags=cv2.INTER_AREA, borderValue=fundo))

async def shot(pg, tmp, doc, w, h, transparente=False):
    t = tmp / '_r.html'; t.write_text(doc)
    await pg.set_viewport_size({'width': w, 'height': h})
    await pg.goto(t.as_uri()); await pg.wait_for_selector('body[data-ready]')
    p = tmp / '_r.png'; await pg.screenshot(path=str(p), omit_background=transparente)
    return Image.open(p).convert('RGBA' if transparente else 'RGB')

def fr(i, total):
    return 'arraste →' if (i == 1 and total > 1) else ('salva pra lembrar →' if i == total else f'{i}/{total}')

def html_marca(n, i, total):
    return f"""<!doctype html><html><head><meta charset='utf-8'><style>{FONT_CSS}
*{{margin:0}} body{{width:{W}px;height:{H}px;background:transparent;font-family:'AR';color:#fff}}
.top{{position:absolute;left:46px;top:40px;font-weight:900;font-size:30px;letter-spacing:.04em;text-shadow:0 1px 10px rgba(0,0,0,.55),0 0 2px rgba(0,0,0,.4)}}
.bot{{position:absolute;left:46px;right:46px;bottom:34px;display:flex;justify-content:space-between;font-weight:700;font-size:19px;letter-spacing:.08em;text-transform:uppercase;text-shadow:0 1px 8px rgba(0,0,0,.6),0 0 2px rgba(0,0,0,.5)}}
.g{{position:absolute;left:0;right:0;bottom:0;height:150px;background:linear-gradient(transparent,rgba(0,0,0,.28))}}
.g2{{position:absolute;left:0;top:0;width:360px;height:140px;background:radial-gradient(ellipse at 0 0,rgba(0,0,0,.30),transparent 70%)}}
</style></head><body><div class='g'></div><div class='g2'></div><div class='top'>Nº {n}</div>
<div class='bot'><span>{HANDLE}</span><span>{e(fr(i, total))}</span></div><script>document.fonts.ready.then(()=>document.body.dataset.ready=1)</script></body></html>"""

def area(q):
    return float(cv2.contourArea(q.reshape(-1, 1, 2)))

async def gerar(lote, cenas, fotos, out, debug=False):
    out.mkdir(parents=True, exist_ok=True); arquivos = []
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--allow-file-access-from-files'])
        pg = await b.new_page()
        for post in lote:
            n = post['numero']; cor = post.get('cor') or cor_do_numero(n)
            slides = post['slides']; total = len(slides)
            for i, sl in enumerate(slides, 1):
                key = f'{n}-{i:02d}'; cfg = cenas[key]; est = cfg['estilo']; E = ESTILOS[est]
                foto = next(f for f in (fotos / f'{key}.png', fotos / f'{key}.jpg') if f.exists())
                base = preparar(foto, cfg.get('zoom'))
                if 'quad' in cfg:
                    quad = ordenar(cfg['quad'])
                elif 'caixa' in cfg:
                    x0, y0, x1, y1 = cfg['caixa']; quad = np.float32([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
                else:
                    quad, _ = detectar(base, cfg.get('semente', (W // 2, H // 2)), cfg.get('tol', 28))
                q2 = encolher(quad, cfg.get('folga', 0.1))
                bw = int(max(np.linalg.norm(q2[1] - q2[0]), np.linalg.norm(q2[2] - q2[3])) * 1.6)
                bh = int(max(np.linalg.norm(q2[3] - q2[0]), np.linalg.norm(q2[2] - q2[1])) * 1.6)
                linhas, apoio, lacuna = linhas_do_slide(sl)
                layer = await shot(pg, out, html_texto(est, cfg, linhas, apoio, lacuna, cor, bw, bh), bw, bh)
                escuro = E['modo'] == 'screen'
                layer = textura(layer, cfg.get('grao', E.get('grao', 0)), escuro, seed=n * 10 + i)
                fundo = (0, 0, 0) if escuro else (255, 255, 255)
                wl = warp(layer, q2, fundo).filter(ImageFilter.GaussianBlur(cfg.get('suave', 0.6)))
                if escuro:
                    img = ImageChops.screen(base, wl)
                else:
                    alfa = E.get('alfa', cfg.get('alfa', 0.95))
                    mult = ImageChops.multiply(base, wl)
                    img = Image.blend(base, mult, alfa)
                if debug:
                    d = np.array(img); cv2.polylines(d, [quad.astype(int).reshape(-1, 1, 2)], True, (255, 0, 0), 3)
                    cv2.polylines(d, [q2.astype(int).reshape(-1, 1, 2)], True, (0, 200, 255), 2); img = Image.fromarray(d)
                marca = await shot(pg, out, html_marca(n, i, total), W, H, transparente=True)
                img = img.convert('RGBA'); img.alpha_composite(marca); img = img.convert('RGB')
                f = out / f"{n}-{post.get('slug', 'post')}-{i:02d}.png"; img.save(f); arquivos.append(f)
            print('ok', n, post.get('slug'), cor, total)
        await b.close()
    for t in ('_r.html', '_r.png'):
        (out / t).unlink(missing_ok=True)
    return arquivos

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    asyncio.run(gerar(json.loads(pathlib.Path(a[0]).read_text()), json.loads(pathlib.Path(a[1]).read_text()),
                      pathlib.Path(a[2]), pathlib.Path(a[3]), '--debug' in sys.argv))
