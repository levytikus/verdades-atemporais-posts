"""Transforma as imagens de um post (1080x1350) num Reel vertical 1080x1920 com música.

Uso:
  python3 kit/reel.py 820                 # gera posts/<pasta do 820>/reel.mp4 a partir do fila.json
  python3 kit/reel.py 820 821 822         # vários números
  python3 kit/reel.py --imagens a.jpg b.jpg --numero 850 --saida reel.mp4

Como fica:
- Fundo: a própria imagem ampliada, desfocada e escurecida, cobrindo a tela 9:16.
- Frente: a imagem, um pouco acima do centro para fugir dos botões do Instagram, com um zoom
  lento e suave. Reels não levam número: a faixa de cima (onde fica o "Nº") e o rodapé
  (@, "ARRASTE →", "2/5") são cortados, e o vídeo leva só o @verdades_atemporais embaixo da imagem.
  A contagem (Nº) é exclusiva dos posts do feed.
- Post único: 8 s. Carrossel: cada slide fica ~3,2 s, com transição curta entre eles.
- O primeiro quadro já mostra a frase (é o gancho e a capa). Sem fade de entrada nem de saída
  na imagem, para o loop ficar contínuo.
- Música: uma das trilhas de kit/musicas (livres de direitos, geradas para a página), escolhida
  pelo número do post, com trecho inicial variado, fade de áudio no começo e no fim.

Requer ffmpeg, pillow e numpy.
"""
import argparse, json, pathlib, subprocess, sys, math
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont

RAIZ = pathlib.Path(__file__).resolve().parent.parent
MUSICAS = RAIZ / 'kit' / 'musicas'
W, H, FPS = 1080, 1920, 30
FRENTE_W = 1000                       # largura da imagem da frente (sobra margem para o zoom)
CENTRO_Y = 840                        # centro vertical da imagem da frente
ZOOM = 0.055                          # quanto a imagem cresce ao longo de cada slide
SEG_UNICO, SEG_SLIDE, TRANS = 8.0, 3.2, 0.38
TOPO = 105                            # px cortados em cima (tira o "Nº"; Reels não têm número)
RODAPE = 98                           # px cortados embaixo (tira @, "ARRASTE →", "2/5"; o @ volta abaixo)
ARROBA = '@verdades_atemporais'
FONTE = RAIZ / 'kit' / 'fonts' / 'Archivo[wdth,wght].ttf'


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * min(max(t, 0), 1))


def assinatura(fundo, prop):
    """Escreve o @ da página centralizado logo abaixo da imagem (posição fixa, não acompanha o zoom)."""
    f = ImageFont.truetype(str(FONTE), 30)
    try:
        f.set_variation_by_axes([100, 600])
    except Exception:
        pass
    d = ImageDraw.Draw(fundo)
    texto = ARROBA.upper()
    larg = d.textlength(texto, font=f) + 2.2 * (len(texto) - 1)
    y = CENTRO_Y + FRENTE_W * (1 + ZOOM) * prop / 2 + 46
    x = (W - larg) / 2
    for ch in texto:
        d.text((x, y), ch, font=f, fill=(255, 255, 255))
        x += d.textlength(ch, font=f) + 2.2
    return fundo


def preparar(caminho, cortar_rodape=True):
    img = Image.open(caminho).convert('RGB')
    if cortar_rodape:
        k = img.height / 1350
        img = img.crop((0, round(TOPO * k), img.width, img.height - round(RODAPE * k)))
    # fundo: cobre 9:16, desfoca e escurece
    s = max(W / img.width, H / img.height) * 1.08
    fundo = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x, y = (fundo.width - W) // 2, (fundo.height - H) // 2
    fundo = fundo.crop((x, y, x + W, y + H)).filter(ImageFilter.GaussianBlur(42))
    fundo = ImageEnhance.Brightness(fundo).enhance(0.62)
    fundo = assinatura(fundo, img.height / img.width)
    # frente em resolução alta para o zoom não perder nitidez
    base = img.resize((round(FRENTE_W * (1 + ZOOM) * 1.5), round(FRENTE_W * (1 + ZOOM) * 1.5 * img.height / img.width)), Image.LANCZOS)
    sombra = Image.new('L', (W, H), 0)
    return fundo, base, img.height / img.width, sombra


def frente(prep, t, dx=0, fundo=None):
    """Desenha a imagem da frente (t de 0 a 1 dentro do slide) deslocada dx px sobre o fundo."""
    _, base, prop, _ = prep
    z = 1 + ZOOM * ease(t)
    fw = FRENTE_W * z
    fh = fw * prop
    img = base.resize((round(fw), round(fh)), Image.BICUBIC)
    x0, y0 = round((W - fw) / 2 + dx), round(CENTRO_Y - fh / 2)
    sh = Image.new('L', (W, H), 0)
    sh.paste(110, (x0, y0 + 14, x0 + round(fw), y0 + round(fh) + 14))
    sh = sh.filter(ImageFilter.GaussianBlur(24))
    fundo = Image.composite(Image.new('RGB', (W, H), (0, 0, 0)), fundo, sh)
    fundo.paste(img, (x0, y0))
    return fundo


def quadro(prep, t):
    return frente(prep, t, 0, prep[0].copy())


def sem_numero(img):
    """Trava da regra da contagem: procura "Nº 123" no quadro (tesseract). Se não houver OCR, avisa e segue."""
    import re, shutil
    if not shutil.which('tesseract'):
        print('Aviso: tesseract não instalado; confira o quadro a olho (Reel não pode ter Nº).'); return True
    import tempfile, subprocess as sp
    with tempfile.NamedTemporaryFile(suffix='.png') as t:
        img.convert('L').resize((W, H)).save(t.name)
        txt = sp.run(['tesseract', t.name, '-', '--psm', '11'], capture_output=True, text=True).stdout
    achou = re.search(r'N\s*[º°o0ª]\s*\.?\s*\d{3}', txt)
    if achou:
        print(f'Encontrado no quadro: {achou.group(0)!r}')
    return not achou


def duracao_audio(f):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def gerar(imagens, numero, saida):
    imagens = [pathlib.Path(i) for i in imagens]
    seg = SEG_UNICO if len(imagens) == 1 else SEG_SLIDE
    total = seg * len(imagens) if len(imagens) == 1 else SEG_SLIDE * len(imagens)
    nq = round(total * FPS)
    preps = [preparar(i) for i in imagens]
    for i, pr in enumerate(preps):
        if not sem_numero(quadro(pr, 0)):
            sys.exit(f'PARADO: a imagem {imagens[i]} ainda mostra o Nº depois do corte (o número está dentro da cena). '
                     'Reels não podem ter número: apague o Nº dessa imagem (ex.: cv2.inpaint) e gere de novo.')

    trilhas = sorted(p for p in MUSICAS.glob('*') if p.suffix.lower() in ('.wav', '.mp3', '.m4a'))
    if not trilhas:
        sys.exit('Nenhuma trilha em kit/musicas.')
    trilha = trilhas[numero % len(trilhas)]
    dur = duracao_audio(trilha)
    folga = max(dur - total - 0.5, 0)
    inicio = (numero * 7.3) % folga if folga > 1 else 0

    saida = pathlib.Path(saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg', '-y', '-loglevel', 'error',
           '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-ss', f'{inicio:.2f}', '-t', f'{total:.2f}', '-i', str(trilha),
           '-filter_complex', f'[1:a]volume=0.8,afade=t=in:st=0:d=0.4,afade=t=out:st={total - 0.9:.2f}:d=0.9[a]',
           '-map', '0:v', '-map', '[a]',
           '-c:v', 'libx264', '-profile:v', 'high', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p',
           '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-ac', '2',
           '-movflags', '+faststart', '-shortest', str(saida)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for q in range(nq):
        tempo = q / FPS
        i = min(int(tempo // seg), len(preps) - 1)
        t_local = (tempo - i * seg) / seg
        resta = (i + 1) * seg - tempo
        if i + 1 < len(preps) and resta < TRANS:
            # transição: desliza para a esquerda como um carrossel; o fundo troca junto
            a = ease(1 - resta / TRANS)
            fundo = Image.blend(preps[i][0], preps[i + 1][0], a)
            desloc = a * (W + 40)
            img = frente(preps[i], t_local, -desloc, fundo)
            img = frente(preps[i + 1], 0, W + 40 - desloc, img)
        else:
            img = quadro(preps[i], t_local)
        p.stdin.write(np.asarray(img, dtype=np.uint8).tobytes())
    p.stdin.close()
    if p.wait() != 0:
        sys.exit(f'ffmpeg falhou ao gerar {saida}')
    print(f'{saida} · {len(imagens)} imagem(ns) · {total:.1f}s · trilha {trilha.name} a partir de {inicio:.1f}s')
    return saida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('numeros', nargs='*', type=int)
    ap.add_argument('--imagens', nargs='+')
    ap.add_argument('--numero', type=int)
    ap.add_argument('--saida')
    a = ap.parse_args()
    if a.imagens:
        gerar(a.imagens, a.numero or 0, a.saida or 'reel.mp4'); return
    fila = json.loads((RAIZ / 'fila.json').read_text())
    for n in a.numeros:
        post = next((p for p in fila if p['numero'] == n and p.get('imagens')), None)
        if not post:
            sys.exit(f'Nº {n} não está no fila.json com imagens.')
        pasta = (RAIZ / post['imagens'][0]).parent
        gerar([RAIZ / i for i in post['imagens']], n, pasta / 'reel.mp4')


if __name__ == '__main__':
    main()
