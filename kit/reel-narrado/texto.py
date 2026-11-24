"""Legenda palavra por palavra, assinatura e fechamento com a logo piscando, sobre o fundo.
Uso: python texto.py INICIO FIM SAIDA   (segundos; quadros [INICIO*30, FIM*30))"""
import json, subprocess, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
OFF = 0.30                         # a voz entra 0,3 s depois do início
FIM_VOZ = 24.6                    # fim da fala no vídeo
CARD = 24.95                       # entra o fechamento
AMARELO = (255, 205, 17)
VERD = '/home/claude/verdades/'
SERIF = '/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf'
SERIF_I = '/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf'
POP = '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'

import difflib, unicodedata
tokens = json.load(open(VERD + 'kit/voz/caber.json'))['texto'].split()
ali = json.load(open(VERD + 'kit/voz/caber-gemini-palavras.json'))['palavras']
def norm(w):
    w = ''.join(c for c in unicodedata.normalize('NFD', w.lower()) if c.isalpha())
    return {'para': 'pra'}.get(w, w)
a_, b_ = [norm(t) for t in tokens], [norm(w['palavra']) for w in ali]
tempo = [None] * len(tokens)
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a_, b_, autojunk=False).get_opcodes():
    for k in range(i2 - i1):
        if j1 + k < j2:
            tempo[i1 + k] = ali[j1 + k]['inicio']
for i in range(len(tempo)):
    if tempo[i] is None:
        tempo[i] = tempo[i - 1] + 0.15
pal = [{'inicio': t} for t in tempo]
DESTAQUE = {'diminuir', 'prisão.', 'inteiro.', 'por', 'completo.'}
# frases (índices de palavra) em que a tela troca
QUEBRAS = [0, 10, 21, 23, 35, 44, 48, 60]

def fonte(path, size, wght):
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_axes([wght])
    except Exception:
        pass
    return f

TAM = 66
F_N = fonte(SERIF, TAM, 500)
F_I = fonte(SERIF_I, TAM, 600)

def glifo(txt, dest):
    f = F_I if dest else F_N
    cor = AMARELO if dest else (255, 255, 255)
    l, t, r, b = f.getbbox(txt)
    pad = 30
    im = Image.new('RGBA', (r - l + 2 * pad, TAM + 40 + 2 * pad), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((pad - l, pad), txt, font=f, fill=(0, 0, 0, 170))
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    ImageDraw.Draw(im).text((pad - l, pad), txt, font=f, fill=cor + (255,))
    out = Image.alpha_composite(sh, im)
    return out, r - l, pad

# disposição de cada frase em linhas centralizadas
ESP = int(TAM * 0.30)
MAXW = 860
LINHA = int(TAM * 1.42)
layout = {}
for q in range(len(QUEBRAS) - 1):
    a, b = QUEBRAS[q], QUEBRAS[q + 1]
    itens = []
    for i in range(a, b):
        tok = tokens[i]
        dest = tok in DESTAQUE
        im, w, pad = glifo(tok, dest)
        itens.append((i, im, w, pad))
    linhas, atual, larg = [], [], 0
    for it in itens:
        add = it[2] + (ESP if atual else 0)
        if atual and larg + add > MAXW:
            linhas.append(atual); atual, larg = [], 0; add = it[2]
        atual.append(it); larg += add
    linhas.append(atual)
    y0 = 905 - (len(linhas) * LINHA) // 2
    pos = []
    for k, ln in enumerate(linhas):
        tot = sum(it[2] for it in ln) + ESP * (len(ln) - 1)
        x = (W - tot) // 2
        for it in ln:
            pos.append((it[0], it[1], x - it[3], y0 + k * LINHA - it[3]))
            x += it[2] + ESP
    layout[q] = pos

ini = [p['inicio'] + OFF for p in pal]
q_ini = [ini[QUEBRAS[q]] - 0.08 for q in range(len(QUEBRAS) - 1)]
q_fim = [q_ini[q + 1] - 0.05 for q in range(len(QUEBRAS) - 2)] + [FIM_VOZ + 0.35]

def ease(x):
    x = min(max(x, 0), 1)
    return 1 - (1 - x) ** 3

# assinatura
logo = Image.open(VERD + 'marca/va-circulo-1080.png').convert('RGBA')
F_AS = ImageFont.truetype(POP, 30)
ass = Image.new('RGBA', (620, 80), (0, 0, 0, 0))
d = ImageDraw.Draw(ass)
lg = logo.resize((46, 46), Image.LANCZOS)
txt = '@verdades_atemporais'
tw = d.textlength(txt, font=F_AS)
x0 = int((620 - (46 + 14 + tw)) / 2)
sha = Image.new('RGBA', ass.size, (0, 0, 0, 0))
ImageDraw.Draw(sha).text((x0 + 60, 21), txt, font=F_AS, fill=(0, 0, 0, 150))
sha = sha.filter(ImageFilter.GaussianBlur(5))
ass = Image.alpha_composite(ass, sha)
ass.alpha_composite(lg, (x0, 17))
ImageDraw.Draw(ass).text((x0 + 60, 21), txt, font=F_AS, fill=(255, 255, 255, 225))
ASS_POS = ((W - 620) // 2, 1650)

# fechamento: quadros da piscada
PIS = '/home/claude/w/pisc/'
F_CARD = ImageFont.truetype(POP, 44)
card_txt = Image.new('RGBA', (900, 90), (0, 0, 0, 0))
d = ImageDraw.Draw(card_txt)
tw = d.textlength(txt, font=F_CARD)
d.text(((900 - tw) / 2, 14), txt, font=F_CARD, fill=(255, 255, 255, 240))

# faixa escura suave atrás do texto
yy = np.arange(H)[:, None]
banda = np.exp(-((yy - 900) / 330.0) ** 2) * 95
BANDA = Image.fromarray(np.dstack([np.zeros((H, W, 3), np.uint8), np.repeat(banda, W, 1).astype(np.uint8)]), 'RGBA')

def piscada(t):
    """k (0..20) e b (0..6) da piscada, t a partir do início da piscada."""
    if t < 0 or t > 0.40:
        return 0, 0
    if t < 0.12:
        k = t / 0.12
    elif t < 0.24:
        k = 1
    else:
        k = 1 - (t - 0.24) / 0.16
    b = math.sin(min(t / 0.40, 1) * math.pi)
    return round(k * 20), round(b * 6)

def quadro(t, bg):
    fr = Image.fromarray(bg, 'RGB').convert('RGBA')
    # fechamento escurece e desfoca o fundo
    c = ease((t - CARD) / 0.5)
    if c > 0:
        bl = fr.filter(ImageFilter.GaussianBlur(18 * c))
        fr = Image.blend(fr, bl, 1)
        fr = Image.blend(fr, Image.new('RGBA', fr.size, (8, 8, 8, 255)), 0.55 * c)
    else:
        fr = Image.alpha_composite(fr, BANDA)
    # legenda
    for q in range(len(QUEBRAS) - 1):
        if t < q_ini[q] or t > q_fim[q] + 0.25:
            continue
        sai = 1 - ease((t - q_fim[q]) / 0.25)
        for i, im, x, y in layout[q]:
            a = ease((t - ini[i] + 0.04) / 0.22) * sai
            if a <= 0:
                continue
            dy = int(10 * (1 - ease((t - ini[i] + 0.04) / 0.30)))
            g = im if a >= 1 else Image.fromarray((np.asarray(im) * [1, 1, 1, a]).astype(np.uint8), 'RGBA')
            fr.alpha_composite(g, (x, y + dy))
    # assinatura (some no fechamento)
    sa = (1 - c) * ease(t / 0.6)
    if sa > 0:
        g = Image.fromarray((np.asarray(ass) * [1, 1, 1, sa]).astype(np.uint8), 'RGBA')
        fr.alpha_composite(g, ASS_POS)
    # logo grande + @
    if t >= CARD + 0.15:
        u = (t - CARD - 0.15) / 0.45
        s = 0.82 + 0.18 * (1 - (1 - min(u, 1)) ** 3) + 0.04 * math.sin(min(u, 1) * math.pi)
        k, b = piscada(t - (CARD + 1.35))
        lg = Image.open(f'{PIS}w_{k:02d}_{b}.png').convert('RGBA')
        sz = int(300 * s)
        lg = lg.resize((sz, sz), Image.LANCZOS)
        al = ease(u * 1.6)
        if al < 1:
            lg = Image.fromarray((np.asarray(lg) * [1, 1, 1, al]).astype(np.uint8), 'RGBA')
        fr.alpha_composite(lg, ((W - sz) // 2, 760 - sz // 2))
        ta = ease((t - CARD - 0.45) / 0.4)
        if ta > 0:
            g = Image.fromarray((np.asarray(card_txt) * [1, 1, 1, ta]).astype(np.uint8), 'RGBA')
            fr.alpha_composite(g, ((W - 900) // 2, 960 + int(12 * (1 - ta))))
    return fr.convert('RGB')

if __name__ == '__main__':
    a, b, saida = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    if saida.endswith('.jpg'):            # quadro de conferência
        bg = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(a), '-i', '/home/claude/w/fundo.mp4', '-frames:v', '1',
                             '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
        quadro(a, np.frombuffer(bg, np.uint8).reshape(H, W, 3)).save(saida, quality=90)
        sys.exit()
    n0, n1 = round(a * FPS), round(b * FPS)
    src = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{a:.4f}', '-i', '/home/claude/w/fundo.mp4', '-frames:v', str(n1 - n0),
                            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    tmp = saida[:-4] + '.tmp.mp4'
    dst = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                            '-i', '-', '-c:v', 'libx264', '-crf', '17', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for n in range(n0, n1):
        raw = src.stdout.read(W * H * 3)
        if len(raw) < W * H * 3:
            break
        dst.stdin.write(quadro(n / FPS, np.frombuffer(raw, np.uint8).reshape(H, W, 3)).tobytes())
    dst.stdin.close(); dst.wait(); src.wait()
    if dst.returncode == 0:
        import os; os.replace(tmp, saida)
