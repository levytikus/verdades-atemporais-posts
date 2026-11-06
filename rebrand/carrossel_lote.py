"""Lote de carrosséis ilustrados (guache + letreiro à mão), nov/2026.
Uso: python3 carrossel_lote.py [nome ...]   (sem nome, gera todos que já têm imagens)
Imagens em fotos/ilustrada/<prefixo>NN.png; uma refeita vira <prefixo>NNb.png e passa a valer."""
import os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import *

AQUI = os.path.dirname(os.path.abspath(__file__))
FOTOS = os.path.join(AQUI, 'fotos', 'ilustrada')
TINTA = (29, 26, 23)
CREME = (246, 237, 220)
_ = ('', 12)  # respiro entre blocos

LOTE = {
    # 1. Humor nostálgico: você virou a sua mãe
    'mae': ('va-mae', [
        [('frases que você jurou', 44), ('que nunca ia dizer:', 44), _, ('“fecha essa', 95), ('geladeira!”', 112)],
        [('“isso aqui', 120), ('não é hotel!”', 135)],
        [('“leva um casaco,', 100), ('vai esfriar.”', 135)],
        [('“apaga essa', 120), ('luz!”', 175)],
        [('“leva um', 120), ('pouquinho?”', 140)],
        [('você não virou', 92), ('a sua mãe.', 125), _, ('você entendeu ela.', 72), ('', 16),
         ('manda pra ela. ela vai rir.', 42)],
    ]),
    # 2. Virada honesta: de fora parece sorte
    'sorte': ('va-sorte', [
        [('“ela tem', 130), ('sorte.”', 180)],
        [('a sorte acordava', 92), ('às 5h.', 165)],
        [('a sorte errou', 105), ('a receita', 95), ('40 vezes.', 125)],
        [('a sorte ouviu', 70), ('“isso não vai', 95), ('dar certo”', 100), ('no almoço de domingo.', 50)],
        [('a sorte vendeu', 98), ('na porta de casa', 82), ('por dois anos.', 102)],
        [('sorte é o nome', 92), ('que dão pro esforço', 72), ('que ninguém viu.', 88), ('', 16),
         ('manda pra quem tá na fase que ninguém vê', 40)],
    ]),
    # 3. Narrativa afetiva: o pai que fala outra língua
    'pai': ('va-pai', [
        [('meu pai nunca', 98), ('disse', 80), ('“eu te amo”.', 145)],
        [('ele dizia:', 62), ('“calibrou', 125), ('o pneu?”', 145)],
        [('ele dizia:', 62), ('“já comeu?”', 155)],
        [('ele dizia:', 62), ('“vai chover,', 115), ('leva o guarda-chuva.”', 82)],
        [('ele dizia:', 62), ('“deixa que', 118), ('eu te busco.”', 118)],
        [('demorei pra entender:', 62), ('ele sempre disse.', 102), ('só que em outra língua.', 72), ('', 16),
         ('manda pro seu pai. ou pra quem fala assim com você', 38)],
    ]),
    # 4. Afeto leve: amizade adulta
    'amizade': ('va-amizade', [
        [('amizade', 155), ('adulta é…', 145)],
        [('ficar três meses', 88), ('sem se falar e voltar', 72), ('como se fosse ontem.', 88)],
        [('marcar,', 112), ('desmarcar', 122), ('e ninguém ficar chateado.', 60)],
        [('responder um áudio', 82), ('de 7 minutos', 108), ('com outro de 9.', 92)],
        [('saber que pode ligar', 80), ('às 3 da manhã.', 112)],
        [('e nunca precisar', 88), ('explicar a saudade.', 88), ('', 16),
         ('manda pro amigo que você não vê faz tempo', 40)],
    ]),
    # 5. Humor agridoce: ser adulto é ótimo. sim, mas…
    'simmas': ('va-simmas', [
        [('ser adulto', 135), ('é ótimo.', 135), ('', 8), ('sim, mas…', 62)],
        [('pode comer bolo', 88), ('no café da manhã.', 76), ('', 8), ('sim, mas a louça de ontem', 50),
         ('continua lá.', 50)],
        [('dorme a hora', 98), ('que quiser.', 108), ('', 8), ('sim, mas acorda às 6', 52), ('do mesmo jeito.', 52)],
        [('ninguém manda', 98), ('em você.', 125), ('', 8), ('sim, mas o boleto manda.', 55)],
        [('a casa é', 100), ('sua.', 135), ('', 8), ('sim, mas o papel higiênico', 50), ('não se troca sozinho.', 50)],
        [('ninguém avisou', 98), ('que liberdade', 98), ('vinha com louça.', 92), ('', 16),
         ('manda pro amigo que tá adultando junto', 40)],
    ]),
    # 6. Validação calma: sinais de que você amadureceu
    'sinais': ('va-sinais', [
        [('sinais de que você', 76), ('amadureceu', 118), ('e ninguém percebeu:', 74)],
        [('você não discute', 88), ('com quem só quer', 76), ('ganhar a discussão.', 76)],
        [('você sai cedo', 102), ('da festa', 112), ('e não pede desculpa.', 66)],
        [('uma tarde', 112), ('sem plano', 122), ('virou presente.', 82)],
        [('“não”', 165), ('virou uma frase', 82), ('completa.', 102)],
        [('ninguém aplaude', 92), ('essas vitórias.', 92), ('então aplaude você.', 82), ('', 16),
         ('manda pra quem tá crescendo calado', 40)],
    ]),
}


def imagem(prefixo, n):
    for cand in (f'{prefixo}{n:02d}c.png', f'{prefixo}{n:02d}b.png', f'{prefixo}{n:02d}.png'):
        p = os.path.join(FOTOS, cand)
        if os.path.exists(p):
            return p
    return None


def gerar(nome):
    prefixo, slides = LOTE[nome]
    saida = os.path.join(AQUI, 'saida', f'lote-{nome}')
    os.makedirs(saida, exist_ok=True)
    feitos = 0
    for i, linhas in enumerate(slides, 1):
        p = imagem(prefixo, i)
        if not p:
            print('falta', f'{prefixo}{i:02d}')
            continue
        img = grao(preencher(Image.open(p)), 3, seed=i)
        cor = CREME if luminancia(img, (100, 60, W - 100, 400)) < 110 else TINTA
        y, grupo = 70, []
        for txt, alt in linhas + [('', 0)]:
            if txt:
                grupo.append((txt, alt))
                continue
            if grupo:
                img, y = letreiro(img, grupo, 90, y, W - 180, cor=cor, alinhamento='centro', espaco=8,
                                  seed=i * 7 + int(y))
                grupo = []
            y += alt
        assinatura(img).save(os.path.join(saida, f'{i:02d}.jpg'), quality=93)
        feitos += 1
    print(nome, feitos, 'de', len(slides), '->', saida)


if __name__ == '__main__':
    for nome in (sys.argv[1:] or LOTE):
        gerar(nome)
