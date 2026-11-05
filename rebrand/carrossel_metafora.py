"""Carrossel formato METÁFORA: frase que todo mundo já disse sobre um objeto que mostra o que ela esconde.
Imagens geradas no Gemini (va-meta-NN), sem texto; a escrita é aplicada aqui."""
import os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import *

AQUI = os.path.dirname(os.path.abspath(__file__))
FOTOS = os.path.join(AQUI, 'fotos', 'metafora')
SAIDA = os.path.join(AQUI, 'saida', 'metafora-limite')
os.makedirs(SAIDA, exist_ok=True)

# (imagem, frase principal, linha de apoio opcional, posição vertical do texto 0 a 1)
SLIDES = [
    ('va-meta-01', '“pode deixar comigo.”', 'Frases de quem já passou do limite:', 0.70),
    ('va-meta-02', '“tô de boa.”', None, 0.72),
    ('va-meta-03', '“não precisa, eu me viro.”', None, 0.72),
    ('va-meta-04', '“foi só um dia ruim.”', None, 0.74),
    ('va-meta-05', '“já me acostumei.”', None, 0.72),
    ('va-meta-06', '“eu dou conta.”', None, 0.72),
    ('va-meta-07', 'Pergunta de novo.', 'Quem sempre diz que está tudo bem\nquase nunca está.', 0.10),
]

LARGURA = {3: 600}

for i, (nome, frase, apoio, py) in enumerate(SLIDES, 1):
    arq = next(f for f in os.listdir(FOTOS) if f.startswith(nome))
    img = preencher(Image.open(os.path.join(FOTOS, arq)))
    img = grao(img, 3, seed=i)
    branco = (252, 249, 243)
    y = int(H * py)
    img = faixa_escura(img, y + 70)
    if i == 1 and apoio:
        img = faixa_escura(img, int(H * 0.09), altura=260, forca=0.3)
    if i == 1 and apoio:
        img, _ = escrever(img, [(apoio, fonte('poppins-semi', 44))], int(H * 0.075), branco,
                          largura=900, alinhamento='centro')
    img, yf = escrever(img, [(frase, fonte('poppins-bold', 74))], y, branco,
                       largura=LARGURA.get(i, 880), alinhamento='centro', entrelinha=1.18)
    if i == len(SLIDES) and apoio:
        for k, ln in enumerate(apoio.split('\n')):
            img, yf = escrever(img, [(ln, fonte('poppins-semi', 38))], yf + (22 if k == 0 else 0), branco,
                               largura=900, alinhamento='centro')
        img, _ = escrever(img, [('Manda pra quem sempre diz “tô bem”.', fonte('poppins-semi', 30))],
                          yf + 30, branco, largura=900, alinhamento='centro')
    img = assinatura(img)
    img.save(os.path.join(SAIDA, f'{i:02d}.jpg'), quality=93)
print('ok', SAIDA)
