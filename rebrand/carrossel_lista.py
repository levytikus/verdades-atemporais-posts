"""Carrossel formato LISTA COM VIRADA: pergunta, itens "Tema: resposta", fechamento.
Fotos de banco (Unsplash): uma pessoa pequena numa paisagem ampla, céu livre em cima para o texto."""
import os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import *

AQUI = os.path.dirname(os.path.abspath(__file__))
FOTOS = os.path.join(AQUI, 'fotos', 'lista')
SAIDA = os.path.join(AQUI, 'saida', 'lista-esperando')
os.makedirs(SAIDA, exist_ok=True)

# (foto, ponto focal vertical, tipo, rótulo, texto)
SLIDES = [
    ('1.jpg', 0.85, 'abre', None, 'O que você está esperando, de verdade?'),
    ('2.jpg', 0.45, 'item', 'Coragem:', 'ninguém sente antes de começar.'),
    ('3.jpg', 0.55, 'item', 'O momento certo:', 'ele não manda aviso.'),
    ('4.jpg', 0.55, 'item', 'Estar pronto:', 'você fica pronto fazendo.'),
    ('5.jpg', 0.55, 'item', 'Aprovação:', 'quem importa entende depois.'),
    ('6.jpg', 0.70, 'item', 'Garantia:', 'não existe nem pra quem espera.'),
    ('7.jpg', 0.60, 'fecha', None, 'Começa mal. Mas começa.'),
]

for i, (foto, fy, tipo, rot, txt) in enumerate(SLIDES, 1):
    img = preencher(Image.open(os.path.join(FOTOS, foto)), fy=fy)
    img = grao(img, 4, seed=i)
    topo = (60, 120, W - 60, 420)
    escuro = luminancia(img, topo) < 150
    cor = (255, 255, 255) if escuro else (18, 18, 18)
    if tipo == 'item':
        runs = [(rot, fonte('inter-bold', 56)), (txt, fonte('inter-reg', 56))]
        img, y = escrever(img, runs, 190, cor, largura=900, alinhamento='esq', x=90, sombra=escuro)
    else:
        runs = [(txt, fonte('inter-bold', 64))]
        img, y = escrever(img, runs, 190, cor, largura=860, alinhamento='centro', sombra=escuro)
        if tipo == 'fecha':
            img, _ = escrever(img, [('Manda pra quem está adiando há meses.', fonte('inter-reg', 36))],
                              y + 26, cor, largura=860, alinhamento='centro', sombra=escuro)
    img = assinatura(img)
    img.save(os.path.join(SAIDA, f'{i:02d}.jpg'), quality=93)
print('ok', SAIDA)
