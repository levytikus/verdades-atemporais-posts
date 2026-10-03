"""Gera os posts do @verdades_atemporais a partir de um lote em JSON.

Uso:  python3 gerar.py lote.json pasta_de_saida

Cada post do lote:
  {"numero": 821, "cor": "vermelho", "cena": "papel", "slug": "coragem",
   "slides": [{"linhas": ["...", "..."], "destaque": "...", "apoio": "..."}], "legenda": "..."}

Cenas: placa, metro, papel, outdoor  -> slides com linhas/destaque/apoio
       placas                        -> slides com {"branca": [l1, l2], "preta": [l1, l2]}
       enter                         -> 1 slide com linhas + "lacuna": true (espaço para completar) e "apoio"
"""
import pathlib, asyncio, html, json, sys
import numpy as np, cv2
from PIL import Image, ImageChops, ImageFilter
from playwright.async_api import async_playwright

S = pathlib.Path(__file__).parent
FONT = (S/'fonts'/'Archivo[wdth,wght].ttf').as_uri().replace('[','%5B').replace(']','%5D').replace(',','%2C')
e = html.escape
H_ = '@verdades_atemporais'

# sequência de cores da página: verde, laranja, azul, rosa, amarelo, vermelho,
# verde limão, azul bebê, roxo, amarelo trator, rosa choque (e recomeça)
SEQ = ['verde','laranja','azul','rosa','amarelo','vermelho','verde limão','azul bebê','roxo','amarelo trator','rosa choque']
CORES = {  # cor de destaque (impressa) por nome
 'verde':'#63D691','laranja':'#FF9A52','azul':'#7D95FF','rosa':'#FF8FC4','amarelo':'#FFD84A','vermelho':'#FF6B5E',
 'verde limão':'#D4F54A','azul bebê':'#9FD4FF','roxo':'#B49BFF','amarelo trator':'#F6B800','rosa choque':'#FF5FAA'}
PAINEL = {  # cor do painel iluminado do metrô
 'verde':(40,170,95),'laranja':(255,128,40),'azul':(50,90,220),'rosa':(255,140,190),'amarelo':(255,214,40),'vermelho':(235,60,50),
 'verde limão':(205,240,60),'azul bebê':(150,205,255),'roxo':(140,95,235),'amarelo trator':(246,184,0),'rosa choque':(255,60,150)}
NEON = {  # texto colorido sobre a placa preta
 'verde':'#5BE08F','laranja':'#FF9A52','azul':'#8FA6FF','rosa':'#FF9FCC','amarelo':'#FFE066','vermelho':'#FF7A6E',
 'verde limão':'#D9FF4F','azul bebê':'#A8DAFF','roxo':'#C2ADFF','amarelo trator':'#FFC51A','rosa choque':'#FF5FAA'}

def cor_do_numero(n):
    """815 é roxo; a sequência anda uma cor por post."""
    return SEQ[(SEQ.index('roxo') + (n - 815)) % len(SEQ)]

BASE_CSS = f"""
@font-face{{font-family:'AR';src:url('{FONT}');font-weight:100 900;font-stretch:62% 125%}}
*{{box-sizing:border-box;margin:0}}
body{{position:relative;font-family:'AR',sans-serif;color:#141414;overflow:hidden}}
.box{{position:absolute;display:flex;flex-direction:column}}
.mid{{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center}}
.big{{font-weight:900;font-stretch:94%;text-transform:uppercase;line-height:0.9;letter-spacing:-0.01em}}
.big div{{white-space:nowrap}}
.hl{{display:inline-block;position:relative;z-index:0}}
.hl::before{{content:'';position:absolute;z-index:-1;left:-0.1em;right:-0.06em;top:0.1em;bottom:0.0em;background:var(--hl)}}
.inv{{display:inline-block;background:#141414;color:#fff;padding:0.04em 0.12em 0 0.1em;margin-left:-0.1em}}
.small{{margin-top:0.6em;font-weight:600;font-stretch:100%;line-height:1.14;letter-spacing:-0.01em}}
.badge2{{display:flex;gap:.7em;align-items:baseline;font-weight:700;letter-spacing:.08em;text-transform:uppercase;line-height:1}}
.badge2 b{{font-weight:900;font-size:1.35em;letter-spacing:.02em}}
.foot{{display:flex;justify-content:space-between;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;opacity:.8}}
"""
FIT = """<script>
document.fonts.ready.then(()=>{
 document.querySelectorAll('.fit').forEach(big=>{
  const mid=big.closest('.mid'); const W=mid.clientWidth; let s=parseFloat(big.dataset.max||260); big.style.fontSize=s+'px';
  const widest=()=>Math.max(...[...big.children].map(d=>d.scrollWidth));
  while((widest()>W||mid.scrollHeight>mid.clientHeight)&&s>30){s-=2;big.style.fontSize=s+'px';}
 });
 document.body.dataset.ready=1;});
</script>"""

def doc(w, h, inner, bg='#fff', hl='#ccc', extra=''):
    return f"""<!doctype html><html><head><meta charset='utf-8'><style>{BASE_CSS}
body{{width:{w}px;height:{h}px;background:{bg};--hl:{hl}}}{extra}</style></head><body>{inner}{FIT}</body></html>"""

def badge(n, px): return f"<div class='badge2' style='font-size:{px}px'><b>Nº {n}</b></div>"

def bigrows(lines, hl, mode='hl'):
    rows = ''.join(f'<div>{e(l)}</div>' for l in lines)
    if hl: rows += f"<div><span class='{mode}'>{e(hl)}</span></div>"
    return rows

def sign_box(x, y, w, h, pad, n, lines, hl, small, foot_r, bpx, small_px, foot_px, mode='hl', maxfs=240):
    return f"""<div class='box' style='left:{x}px;top:{y}px;width:{w}px;height:{h}px;padding:{pad}'>
{badge(n, bpx)}
<div class='mid'><div class='big fit' data-max='{maxfs}'>{bigrows(lines, hl, mode)}</div>
{f"<div class='small' style='font-size:{small_px}px'>{e(small)}</div>" if small else ''}</div>
<div class='foot' style='font-size:{foot_px}px'><span>{H_}</span><span>{e(foot_r)}</span></div></div>"""

def fr(i, total): return 'arraste →' if (i == 1 and total > 1) else ('salva pra lembrar →' if i == total else f'{i}/{total}')

FLAT = {  # caixa de texto em px na imagem 1080x1350
 'placa':   dict(box=(145,179,806,971), pad='84px 54px 70px', bpx=26, small_px=54, foot_px=20),
 'metro':   dict(box=(279,458,525,628), pad='34px 36px 26px', bpx=21, small_px=38, foot_px=15, mode='inv'),
 'papel':   dict(box=(247,280,632,872), pad='40px 46px 30px', bpx=24, small_px=44, foot_px=17),
 'outdoor': dict(box=(116,326,940,646), pad='40px 60px 30px', bpx=24, small_px=42, foot_px=17),
}

def quad_out(q): return [(x*1080/736, y*1350/920) for x, y in q]
WQ = quad_out([(130,327),(627,232),(629,378),(131,447)])
BQ = quad_out([(130,487),(626,410),(630,562),(131,625)])
def sub(q, u0, u1, v0, v1):
    tl, tr, br, bl = [np.array(p) for p in q]
    P = lambda u, v: (1-v)*((1-u)*tl + u*tr) + v*((1-u)*bl + u*br)
    return np.float32([P(u0,v0), P(u1,v0), P(u1,v1), P(u0,v1)])

def warp(img, dst, fill):
    w, h = img.size
    M = cv2.getPerspectiveTransform(np.float32([(0,0),(w,0),(w,h),(0,h)]), dst)
    return Image.fromarray(cv2.warpPerspective(np.array(img), M, (1080,1350), flags=cv2.INTER_CUBIC, borderValue=fill))

def mult(base, layer, blur=0.55): return ImageChops.multiply(base, layer.filter(ImageFilter.GaussianBlur(blur)))

def painel_metro(base, rgb):
    a = np.array(base).astype(float); x0,y0,x1,y1 = 279,458,806,1088
    H, W = y1-y0, x1-x0; ys, xs = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xs-W/2)/(W/2))**2 + ((ys-H/2)/(H/2))**2)
    rng = np.random.default_rng(1); g = cv2.GaussianBlur(rng.normal(0,1,(H,W)).astype('float32'),(0,0),0.8)
    a[y0:y1, x0:x1] = np.array(rgb,float)[None,None,:]*(1.03-0.10*d**2)[...,None] + (g*3)[...,None]
    return Image.fromarray(a.clip(0,255).astype('uint8'))

async def shot(pg, tmpdir, html_s, w, h):
    t = tmpdir/'_r.html'; t.write_text(html_s)
    await pg.set_viewport_size({'width': w, 'height': h})
    await pg.goto(t.as_uri()); await pg.wait_for_selector('body[data-ready]')
    p = tmpdir/'_r.png'; await pg.screenshot(path=str(p))
    return Image.open(p).convert('RGB')

async def gerar(lote, out):
    out.mkdir(parents=True, exist_ok=True); arquivos = []
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        for post in lote:
            n, cena = post['numero'], post['cena']
            cor = post.get('cor') or cor_do_numero(n)
            nome = f"{n}-{post.get('slug','post')}"
            slides = post['slides']; total = len(slides)
            base = Image.open(S/'bases'/f'{cena}.png').convert('RGB')
            for i, sl in enumerate(slides, 1):
                if cena in FLAT:
                    c = FLAT[cena]; b0 = painel_metro(base, PAINEL[cor]) if cena == 'metro' else base
                    hl = '#141414' if cena == 'metro' else CORES[cor]
                    inner = sign_box(*c['box'], c['pad'], n, sl['linhas'], sl.get('destaque'), sl.get('apoio'), fr(i, total),
                                     c['bpx'], c['small_px'], c['foot_px'], c.get('mode','hl'))
                    img = mult(b0, await shot(pg, out, doc(1080,1350,inner,hl=hl), 1080, 1350))
                elif cena == 'placas':
                    (w1, w2), (k1, k2) = sl['branca'], sl['preta']; cw, ch = 1100, 300
                    st = "font-weight:800;font-stretch:96%;line-height:0.98;letter-spacing:-0.02em"
                    white = await shot(pg, out, doc(cw, ch, f"<div class='box' style='left:0;top:0;width:{cw}px;height:{ch}px;padding:10px 20px'><div class='mid'><div class='fit' data-max='170' style='{st}'><div style='white-space:nowrap'>{e(w1)}</div><div style='white-space:nowrap'>{e(w2)}</div></div></div></div>"), cw, ch)
                    black = await shot(pg, out, doc(cw, ch, f"<div class='box' style='left:0;top:0;width:{cw}px;height:{ch}px;padding:10px 20px;color:#fff'><div class='mid'><div class='fit' data-max='170' style='{st};text-align:right'><div style='white-space:nowrap'>{e(k1)}</div><div style='white-space:nowrap;color:{NEON[cor]}'>{e(k2)}</div></div></div></div>", bg='#000'), cw, ch)
                    img = mult(base, warp(white, sub(WQ,.05,.79,.14,.84), (255,255,255)), 0.5)
                    img = ImageChops.lighter(img, warp(black, sub(BQ,.19,.965,.17,.85), (0,0,0)).filter(ImageFilter.GaussianBlur(0.5)))
                    sten = await shot(pg, out, doc(1080,1350, f"<div style='position:absolute;left:58px;top:70px'>{badge(n,31)}</div><div class='foot' style='position:absolute;left:58px;right:58px;bottom:44px;font-size:20px'><span>{H_}</span><span>{e(fr(i,total))}</span></div>"), 1080, 1350)
                    img = mult(img, sten, 0.7)
                elif cena == 'enter':
                    rows = ''.join(f'<div>{e(l)}</div>' for l in sl['linhas'][:-1])
                    last = e(sl['linhas'][-1]) + (" <span class='hl' style='width:3.3em'>&nbsp;</span>" if sl.get('lacuna') else '')
                    apoio = '<br>'.join(e(x) for x in sl.get('apoio','Complete nos comentários|e aperte enter.').split('|'))
                    inner = f"""<div class='box' style='left:84px;top:52px;width:912px;height:580px;padding:0'>{badge(n,24)}
<div class='mid' style='margin-top:18px'><div class='big fit' data-max='200'>{rows}<div>{last}</div></div></div></div>
<div class='box' style='left:84px;top:1150px;width:912px;height:160px;align-items:center;text-align:center'>
<div style='font-weight:600;font-size:40px;line-height:1.15;letter-spacing:-0.01em'>{apoio}</div>
<div class='foot' style='font-size:17px;margin-top:18px;gap:30px'><span>{H_}</span><span>salva pra lembrar →</span></div></div>"""
                    img = mult(base, await shot(pg, out, doc(1080,1350,inner,hl=CORES[cor],extra='.hl::before{bottom:0.08em}'), 1080, 1350))
                else:
                    raise ValueError(f'cena desconhecida: {cena}')
                f = out/f'{nome}-{i:02d}.png'; img.save(f); arquivos.append(f)
            print('ok', nome, cor, cena, total)
        await b.close()
    for t in ('_r.html','_r.png'): (out/t).unlink(missing_ok=True)
    return arquivos

if __name__ == '__main__':
    lote = json.loads(pathlib.Path(sys.argv[1]).read_text())
    asyncio.run(gerar(lote, pathlib.Path(sys.argv[2])))
