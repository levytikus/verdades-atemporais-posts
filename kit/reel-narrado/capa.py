"""Capa do Reel narrado (vai para o Instagram como cover_url; nunca usar o 1º quadro, que é escuro).

Uso:
  python capa.py --clipe kit/clipes/m46702.mp4 --t 8 --px 0.52 \
      --frase "Repara no jeito que você fala com você." --destaque "jeito,você." \
      --saida posts/reel-x/capa.jpg

O texto fica no centro da área 3:4 que a grade do perfil mostra (y 240 a 1680).
"""
import argparse, subprocess, io
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1080, 1920
AMARELO = (255, 205, 17)
SERIF = '/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf'
SERIF_I = '/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf'
POP = '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
RAIZ = __file__.rsplit('/kit/', 1)[0] + '/'


def fonte(path, size, wght):
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_axes([wght])
    except Exception:
        pass
    return f


def quadro(clipe, t, px):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', clipe, '-frames:v', '1',
                          '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True, check=True).stdout
    im = Image.open(io.BytesIO(raw)).convert('RGB')
    iw, ih = im.size
    cw = min(iw, int(ih * 9 / 16)); ch = min(ih, int(iw * 16 / 9))
    x = int(max(0, min(iw - cw, iw * px - cw / 2)))
    im = im.crop((x, (ih - ch) // 2, x + cw, (ih - ch) // 2 + ch)).resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(0.82)
    im = ImageEnhance.Brightness(im).enhance(0.9)
    return im.convert('RGBA')


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--clipe', required=True); a.add_argument('--t', type=float, default=2)
    a.add_argument('--px', type=float, default=0.5); a.add_argument('--frase', required=True)
    a.add_argument('--destaque', default=''); a.add_argument('--saida', required=True)
    a.add_argument('--tam', type=int, default=88)
    o = a.parse_args()
    dest = {d.strip().lower() for d in o.destaque.split(',') if d.strip()}

    fr = quadro(o.clipe, o.t, o.px)
    # escurece o centro e as bordas para o texto respirar
    yy = np.arange(H)[:, None].astype(float)
    alfa = np.clip(np.exp(-((yy - 960) / 420.0) ** 2) * 95 + 25, 0, 255)
    xx = np.arange(W)[None, :].astype(float)
    vin = np.clip(((xx - W / 2) / (W * 0.62)) ** 2 * 140, 0, 140)
    camada = np.clip(alfa + vin, 0, 210).astype(np.uint8)
    fr = Image.alpha_composite(fr, Image.fromarray(np.dstack([np.zeros((H, W, 3), np.uint8), camada]), 'RGBA'))

    F_N, F_I = fonte(SERIF, o.tam, 600), fonte(SERIF_I, o.tam, 650)
    esp = int(o.tam * 0.28); maxw = 880; linha = int(o.tam * 1.32)
    pal = []
    for w in o.frase.split():
        d = w.lower() in dest
        f = F_I if d else F_N
        l, _, r, _ = f.getbbox(w)
        pal.append((w, d, f, r - l, l))
    linhas, atual, larg = [], [], 0
    for p in pal:
        add = p[3] + (esp if atual else 0)
        if atual and larg + add > maxw:
            linhas.append(atual); atual, larg = [], 0; add = p[3]
        atual.append(p); larg += add
    linhas.append(atual)

    txt = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sombra = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    y0 = 960 - (len(linhas) * linha) // 2 - int(o.tam * 0.15)
    for k, ln in enumerate(linhas):
        tot = sum(p[3] for p in ln) + esp * (len(ln) - 1)
        x = (W - tot) // 2
        for w, d, f, wd, l in ln:
            pos = (x - l, y0 + k * linha)
            ImageDraw.Draw(sombra).text(pos, w, font=f, fill=(0, 0, 0, 190))
            ImageDraw.Draw(txt).text(pos, w, font=f, fill=(AMARELO if d else (255, 255, 255)) + (255,))
            x += wd + esp
    fr = Image.alpha_composite(fr, sombra.filter(ImageFilter.GaussianBlur(12)))
    fr = Image.alpha_composite(fr, txt)

    # assinatura dentro da área 3:4
    logo = Image.open(RAIZ + 'marca/va-circulo-1080.png').convert('RGBA').resize((52, 52), Image.LANCZOS)
    fa = ImageFont.truetype(POP, 32)
    s = '@verdades_atemporais'
    tw = ImageDraw.Draw(fr).textlength(s, font=fa)
    x0 = int((W - (52 + 16 + tw)) / 2); y = 1560
    fr.alpha_composite(logo, (x0, y))
    ImageDraw.Draw(fr).text((x0 + 68, y + 6), s, font=fa, fill=(255, 255, 255, 235))
    fr.convert('RGB').save(o.saida, quality=93)


if __name__ == '__main__':
    main()
