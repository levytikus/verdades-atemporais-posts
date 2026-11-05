"""Carrossel METÁFORA na versão ILUSTRADA: pintura em guache de cenas de casa brasileira (Gemini, va-ilu-NN)
com o título em letras à mão empilhadas no topo, como cartaz pintado."""
import os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import *

AQUI = os.path.dirname(os.path.abspath(__file__))
FOTOS = os.path.join(AQUI, 'fotos', 'ilustrada')
SAIDA = os.path.join(AQUI, 'saida', 'ilustrada-limite')
os.makedirs(SAIDA, exist_ok=True)

TINTA = (29, 26, 23)
CREME = (246, 237, 220)

# imagem, linhas do título (texto, altura da letra), alinhamento
SLIDES = [
    ('va-ilu-01', [('frases de quem já', 44), ('passou do limite:', 44), ('', 14),
                   ('“pode deixar', 96), ('comigo.”', 120)], 'centro'),
    ('va-ilu-02', [('“tô de', 125), ('boa.”', 175)], 'centro'),
    ('va-ilu-03', [('“não precisa,', 96), ('eu me', 60), ('viro.”', 128)], 'centro'),
    ('va-ilu-04', [('“foi só um', 115), ('dia ruim.”', 145)], 'centro'),
    ('va-ilu-05', [('“já me', 115), ('acostumei.”', 145)], 'centro'),
    ('va-ilu-06', [('“eu dou', 125), ('conta.”', 165)], 'centro'),
    ('va-ilu-07', [('pergunta', 130), ('de novo.', 130), ('', 14),
                   ('quem sempre diz que está tudo bem', 54), ('quase nunca está.', 54), ('', 12),
                   ('manda pra quem sempre diz “tô bem”', 42)], 'centro'),
]


def escolher(nome):
    """Usa a versão refeita (sufixo b) quando existir."""
    n = nome.split('-')[-1]
    for cand in (f'va-ilu-r{n}.png', f'{nome}b.png', f'{nome}.png'):
        p = os.path.join(FOTOS, cand)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(nome)


for i, (nome, linhas, alin) in enumerate(SLIDES, 1):
    try:
        img = preencher(Image.open(escolher(nome)))
    except FileNotFoundError:
        print('falta', nome); continue
    img = grao(img, 3, seed=i)
    escuro = luminancia(img, (100, 60, W - 100, 380)) < 110
    cor = CREME if escuro else TINTA
    blocos = [l for l in linhas if l[0]]
    y = 70
    # linhas vazias viram espaço extra
    grupo = []
    for txt, alt in linhas + [('', 0)]:
        if txt:
            grupo.append((txt, alt))
            continue
        if grupo:
            img, y = letreiro(img, grupo, 90, y, W - 180, cor=cor, alinhamento=alin, espaco=8, seed=i * 7 + int(y))
            grupo = []
        y += alt
    img = assinatura(img)
    img.save(os.path.join(SAIDA, f'{i:02d}.jpg'), quality=93)
print('ok', SAIDA)
