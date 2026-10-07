"""Gera o Story das 20h05: a verdade da noite em 1080x1920, com o Nº e o aviso "Nova verdade no feed".

Uso:
  python3 kit/story.py 820             # gera posts/<pasta do 820>/story.jpg a partir do fila.json
  python3 kit/story.py 820 821 822

Como fica:
- Fundo: a própria imagem ampliada, desfocada e escurecida.
- No topo, uma etiqueta na cor do post: "NOVA VERDADE NO FEED".
- No meio, a primeira imagem do post inteira (com o Nº: Stories divulgam o post numerado).
- Embaixo, "Toque no perfil e leia agora" e o @verdades_atemporais.
O Story não tem número próprio: ele só aponta para a verdade numerada do feed.

Requer pillow.
"""
import json, pathlib, sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / 'kit'))
from gerar import CORES, cor_do_numero  # mesma sequência de cores da página

W, H = 1080, 1920
FONTE = RAIZ / 'kit' / 'fonts' / 'Archivo[wdth,wght].ttf'


def fonte(tam, peso):
    f = ImageFont.truetype(str(FONTE), tam)
    try:
        f.set_variation_by_axes([peso, 100])
    except Exception:
        pass
    return f


def espacado(d, xy_centro, texto, f, cor, esp):
    larg = sum(d.textlength(c, font=f) for c in texto) + esp * (len(texto) - 1)
    x, y = xy_centro[0] - larg / 2, xy_centro[1]
    for c in texto:
        d.text((x, y), c, font=f, fill=cor)
        x += d.textlength(c, font=f) + esp
    return larg


def hex_rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def gerar(imagem, numero, saida):
    img = Image.open(imagem).convert('RGB')
    img = img.crop((0, 0, img.width, img.height - round(98 * img.height / 1350)))  # tira rodapé (@, ARRASTE, 1/5)
    s = max(W / img.width, H / img.height) * 1.1
    fundo = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x, y = (fundo.width - W) // 2, (fundo.height - H) // 2
    fundo = fundo.crop((x, y, x + W, y + H)).filter(ImageFilter.GaussianBlur(46))
    fundo = ImageEnhance.Brightness(fundo).enhance(0.45)

    larg = 900
    frente = img.resize((larg, round(larg * img.height / img.width)), Image.LANCZOS)
    fx, fy = (W - larg) // 2, 420
    sombra = Image.new('L', (W, H), 0)
    sombra.paste(120, (fx, fy + 16, fx + larg, fy + frente.height + 16))
    fundo = Image.composite(Image.new('RGB', (W, H)), fundo, sombra.filter(ImageFilter.GaussianBlur(26)))
    fundo.paste(frente, (fx, fy))

    d = ImageDraw.Draw(fundo)
    cor = hex_rgb(CORES[cor_do_numero(numero)])
    escuro = (20, 20, 20)
    # etiqueta "NOVA VERDADE NO FEED" na cor do post
    f1 = fonte(40, 800)
    texto = 'NOVA VERDADE NO FEED'
    tl = sum(d.textlength(c, font=f1) for c in texto) + 4 * (len(texto) - 1)
    caixa = (W / 2 - tl / 2 - 34, 250, W / 2 + tl / 2 + 34, 336)
    d.rounded_rectangle(caixa, radius=10, fill=cor)
    espacado(d, (W / 2, 268), texto, f1, escuro, 4)
    # chamada e @ embaixo
    base = fy + frente.height
    f2 = fonte(44, 600)
    espacado(d, (W / 2, base + 70), 'Toque no perfil e leia agora', f2, (255, 255, 255), 0)
    f3 = fonte(30, 600)
    espacado(d, (W / 2, base + 146), '@VERDADES_ATEMPORAIS', f3, (220, 220, 220), 2.2)

    saida = pathlib.Path(saida)
    fundo.save(saida, quality=93)
    print(f'{saida} · Nº {numero} · {cor_do_numero(numero)}')
    return saida


def main():
    fila = json.loads((RAIZ / 'fila.json').read_text())
    for n in map(int, sys.argv[1:]):
        post = next((p for p in fila if p['numero'] == n and p.get('imagens') and not p.get('chave')), None)
        if not post:
            sys.exit(f'Nº {n} não está no fila.json como post do feed.')
        pasta = (RAIZ / post['imagens'][0]).parent
        gerar(RAIZ / post['imagens'][0], n, pasta / 'story.jpg')


if __name__ == '__main__':
    main()
