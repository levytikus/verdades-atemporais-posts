"""Funções comuns das peças do rebrand do Verdades Atemporais."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageStat

AQUI = os.path.dirname(os.path.abspath(__file__))
MARCA = os.path.join(AQUI, '..', 'marca')
W, H = 1080, 1350

_F = os.path.join(AQUI, 'fontes')
FONTES = {
    'inter-bold': os.path.join(_F, 'Inter-Bold.otf'),
    'inter-reg': os.path.join(_F, 'Inter-Regular.otf'),
    'inter-semi': os.path.join(_F, 'Inter-SemiBold.otf'),
    'poppins-bold': os.path.join(_F, 'Poppins-Bold.ttf'),
    'poppins-semi': os.path.join(_F, 'Poppins-Medium.ttf'),
}


def fonte(nome, tam):
    return ImageFont.truetype(FONTES[nome], tam)


def aparar_borda(img, limiar=245, folga=4):
    """Remove moldura branca que o gerador às vezes coloca em volta da imagem."""
    import numpy as np
    a = np.asarray(img.convert('L'))
    linhas = np.where(a.mean(1) < limiar)[0]
    cols = np.where(a.mean(0) < limiar)[0]
    if len(linhas) == 0 or len(cols) == 0:
        return img
    t, b, l, r = linhas[0], linhas[-1], cols[0], cols[-1]
    if t == 0 and l == 0 and b == a.shape[0] - 1 and r == a.shape[1] - 1:
        return img
    return img.crop((l + folga, t + folga, r - folga, b - folga))


def preencher(img, w=W, h=H, fy=0.5, fx=0.5):
    """Recorta e redimensiona para w x h, escolhendo o ponto focal (0 a 1)."""
    img = aparar_borda(img.convert('RGB'))
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = round((img.width - w) * fx)
    y = round((img.height - h) * fy)
    return img.crop((x, y, x + w, y + h))


def luminancia(img, caixa):
    return ImageStat.Stat(img.crop(caixa).convert('L')).mean[0]


def quebrar(runs, largura, d):
    """runs: lista de (texto, fonte). Quebra em linhas por palavra mantendo a fonte de cada trecho."""
    palavras = []
    for texto, f in runs:
        for i, p in enumerate(texto.split(' ')):
            if p:
                palavras.append((p, f))
    linhas, atual, larg = [], [], 0
    for p, f in palavras:
        esp = d.textlength(' ', font=f) if atual else 0
        lp = d.textlength(p, font=f)
        if atual and larg + esp + lp > largura:
            linhas.append(atual)
            atual, larg = [], 0
            esp = 0
        atual.append((p, f))
        larg += esp + lp
    if atual:
        linhas.append(atual)
    return linhas


def escrever(img, runs, y, cor, largura=900, alinhamento='esq', x=90, entrelinha=1.22,
             sombra=True, sombra_cor=None):
    """Escreve texto misto (negrito + regular) com quebra automática. Devolve o y final."""
    base = img.convert('RGBA')
    camada = Image.new('RGBA', base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    linhas = quebrar(runs, largura, d)
    # evita palavra sozinha na última linha
    lw = largura
    while len(linhas) > 1 and len(linhas[-1]) < 2 and lw > largura * 0.6:
        lw -= 20
        linhas = quebrar(runs, lw, d)
    tam = max(f.size for _, f in runs)
    alt = round(tam * entrelinha)
    yy = y
    pos = []
    for ln in linhas:
        total = sum(d.textlength(p, font=f) for p, f in ln) + sum(d.textlength(' ', font=f) for p, f in ln[1:])
        xx = x if alinhamento == 'esq' else (W - total) / 2
        for i, (p, f) in enumerate(ln):
            if i:
                xx += d.textlength(' ', font=f)
            pos.append((xx, yy, p, f))
            xx += d.textlength(p, font=f)
        yy += alt
    if sombra:
        sc = sombra_cor or ((0, 0, 0, 110) if sum(cor[:3]) > 380 else (255, 255, 255, 60))
        sh = Image.new('RGBA', base.size, (0, 0, 0, 0))
        ds = ImageDraw.Draw(sh)
        for xx, y0, p, f in pos:
            ds.text((xx, y0 + 2), p, font=f, fill=sc)
        sh = sh.filter(ImageFilter.GaussianBlur(5))
        base = Image.alpha_composite(base, sh)
    for xx, y0, p, f in pos:
        d.text((xx, y0), p, font=f, fill=cor)
    return Image.alpha_composite(base, camada).convert('RGB'), yy


def assinatura(img, clara=None, tam=24, alpha=175):
    """Carinha + @verdades_atemporais no canto inferior direito. Escolhe branco ou preto pelo fundo."""
    im = img.convert('RGBA')
    d = ImageDraw.Draw(im)
    f = fonte('inter-semi', tam)
    texto = '@verdades_atemporais'
    tw = d.textlength(texto, font=f)
    ih = int(tam * 1.05)
    iw = int(ih * 680 / 515)
    gap = int(tam * 0.45)
    x = W - tw - 40
    y = H - tam - 42
    ix = int(x - gap - iw)
    if clara is None:
        clara = luminancia(img, (int(ix) - 10, y - 10, W - 30, H - 30)) < 150
    cor = (255, 255, 255) if clara else (17, 17, 17)
    selo = 'va-selo-branco.png' if clara else 'va-selo-preto.png'
    camada = Image.new('RGBA', im.size, (0, 0, 0, 0))
    dc = ImageDraw.Draw(camada)
    dc.text((x, y), texto, font=f, fill=cor + (alpha,))
    ic = Image.open(os.path.join(MARCA, selo)).convert('RGBA').resize((iw, ih), Image.LANCZOS)
    a = ic.split()[3].point(lambda v: v * alpha // 255)
    ic.putalpha(a)
    camada.alpha_composite(ic, (ix, int(y + tam * 0.58 - ih / 2)))
    if clara:
        sh = camada.split()[3].filter(ImageFilter.GaussianBlur(3)).point(lambda v: v // 2)
        sombra = Image.new('RGBA', im.size, (0, 0, 0, 0))
        sombra.putalpha(sh)
        im = Image.alpha_composite(im, sombra)
    return Image.alpha_composite(im, camada).convert('RGB')


def grao(img, forca=6, seed=0):
    """Grão leve de filme para unificar fotos de fontes diferentes."""
    import random
    import numpy as np
    rng = np.random.default_rng(seed)
    a = np.asarray(img).astype('int16')
    n = rng.normal(0, forca, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a + n, 0, 255).astype('uint8'))


def faixa_escura(img, centro, altura=520, forca=0.38):
    """Escurece suavemente uma faixa horizontal para o texto branco ler bem em fundo claro."""
    import numpy as np
    a = np.asarray(img).astype('float32')
    ys = np.arange(a.shape[0])[:, None]
    m = np.exp(-((ys - centro) / (altura / 2.2)) ** 2) * forca
    return Image.fromarray(np.clip(a * (1 - m[..., None]), 0, 255).astype('uint8'))


FONTES['amatic'] = os.path.join(_F, 'AmaticSC-Bold.ttf')
FONTES['marker'] = os.path.join(_F, 'PermanentMarker.ttf')


def _linha_mao(texto, alvo_w, fonte_nome, seed, cor, max_h=None):
    """Desenha uma linha de letras à mão com tamanho e inclinação levemente irregulares."""
    import random
    rnd = random.Random(seed)
    base = 200
    letras = []
    for ch in texto:
        if ch == ' ':
            letras.append((' ', None, 0, 0))
            continue
        tam = int(base * rnd.uniform(0.9, 1.1))
        letras.append((ch, ImageFont.truetype(FONTES[fonte_nome], tam), rnd.uniform(-4, 4), rnd.uniform(-8, 8)))
    # mede
    tmp = ImageDraw.Draw(Image.new('L', (10, 10)))
    pecas, x = [], 0
    for ch, f, rot, dy in letras:
        if f is None:
            x += base * 0.28
            continue
        bb = tmp.textbbox((0, 0), ch, font=f)
        if ch in '.,;:!?”"\'' and pecas:
            x -= base * 0.07
        w, h = bb[2] - bb[0] + 20, int(base * 1.6)
        m = Image.new('L', (w, h), 0)
        ImageDraw.Draw(m).text((10 - bb[0], int(base * 0.25)), ch, font=f, fill=255)
        m = m.rotate(rot, resample=Image.BICUBIC, expand=False)
        pecas.append((x, dy, m))
        x += bb[2] - bb[0] + base * 0.03
    W0 = int(x) + 20
    H0 = int(base * 1.8)
    mask = Image.new('L', (W0, H0), 0)
    for px, dy, m in pecas:
        mask.paste(255, (int(px), int(dy + base * 0.1)), m)
    mask = mask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(1.2))
    bb = mask.getbbox()
    mask = mask.crop(bb)
    if alvo_w < 0:  # altura fixa em px
        s = -alvo_w / mask.height
        return mask.resize((max(1, int(mask.width * s)), max(1, int(mask.height * s))), Image.LANCZOS)
    s = alvo_w / mask.width
    if max_h and mask.height * s > max_h:
        s = max_h / mask.height
    return mask.resize((max(1, int(mask.width * s)), max(1, int(mask.height * s))), Image.LANCZOS)


def letreiro(img, linhas, x0, y0, largura, cor=(29, 26, 23), alinhamento='esq', espaco=14, seed=1,
             textura=True):
    """Título em letras à mão empilhadas, cada linha esticada para a largura do bloco
    linhas: lista de (texto, altura da letra em px); palavras curtas pequenas, palavras-chave grandes."""
    import numpy as np
    camadas, y = [], y0
    for k, (txt, alt) in enumerate(linhas):
        m = _linha_mao(txt.upper(), -int(alt), 'amatic', seed * 31 + k, cor)
        if m.width > largura:
            m = m.resize((largura, int(m.height * largura / m.width)), Image.LANCZOS)
        if alinhamento == 'esq':
            x = x0
        elif alinhamento == 'dir':
            x = x0 + largura - m.width
        else:
            x = x0 + (largura - m.width) // 2
        camadas.append((x, y, m))
        y += m.height + espaco
    base = img.convert('RGBA')
    for x, yy, m in camadas:
        if textura:
            rng = np.random.default_rng(seed + yy)
            a = np.asarray(m).astype('float32') / 255
            ruido = rng.random(a.shape)
            a = a * np.where(ruido < 0.025, 0.6, 1.0)
            m = Image.fromarray((a * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.6))
        tinta = Image.new('RGBA', m.size, cor + (255,))
        tinta.putalpha(m)
        base.alpha_composite(tinta, (int(x), int(yy)))
    return base.convert('RGB'), y
