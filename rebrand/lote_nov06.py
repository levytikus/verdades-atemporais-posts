"""Agenda do lote de 6 carrosséis de 06/11/2026 (legendas, datas, horários).
Uso: python3 lote_nov06.py <nome>   copia os slides prontos para posts/ e põe o item na fila.json."""
import json, os, shutil, sys

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

AGENDA = {
    'mae': ('rb-002', 'rb-002-virei-minha-mae', '2026-11-06', '15:45',
            "Ninguém avisa que um dia você vai abrir a boca e sair a voz da sua mãe. E o pior: ela tinha razão em quase tudo.\n\n"
            "Qual dessas você já disse essa semana? Conta aqui embaixo. E manda pra sua mãe, ela vai rir. 😂\n\n"
            "#mãe #frasesdemãe #nostalgia #humor #verdadesatemporais"),
    'sorte': ('rb-003', 'rb-003-parece-sorte', '2026-11-06', '18:00',
              "De fora, sempre parece sorte. Ninguém vê as madrugadas, as receitas que deram errado nem o almoço de domingo cheio de dúvida.\n\n"
              "Se você está na fase que ninguém vê, continua. Quem hoje parece ter sorte também já esteve aí.\n\n"
              "Manda pra quem precisa ler isso hoje. 🤍\n\n"
              "#motivação #empreender #persistência #reflexão #verdadesatemporais"),
    'pai': ('rb-004', 'rb-004-outra-lingua', '2026-11-06', '21:00',
            "Tem pai que nunca disse \"eu te amo\". Mas calibrou o pneu, cortou a manga e esperou no ponto de ônibus de madrugada.\n\n"
            "Amor também tem sotaque. Às vezes a gente só demora pra aprender a língua.\n\n"
            "Qual era a frase do seu pai? Conta nos comentários. 🤍\n\n"
            "#pai #amordepai #família #reflexão #verdadesatemporais"),
    'amizade': ('rb-005', 'rb-005-amizade-adulta', '2026-11-07', '12:00',
                "Amizade adulta não é se ver toda semana. É saber que a pessoa continua ali, mesmo no meio da correria.\n\n"
                "Marca aquele amigo que você não vê faz tempo e diz que lembrou dele. 🤍\n\n"
                "#amizade #amigos #saudade #vidaadulta #verdadesatemporais"),
    'simmas': ('rb-006', 'rb-006-sim-mas', '2026-11-07', '18:00',
               "Ser adulto é ótimo. Sim, mas ninguém leu as letras miúdas do contrato.\n\n"
               "Qual \"sim, mas\" você colocaria nessa lista? Escreve aqui embaixo. 😅\n\n"
               "#vidaadulta #humor #adultar #boletos #verdadesatemporais"),
    'sinais': ('rb-007', 'rb-007-amadureceu', '2026-11-07', '21:00',
               "Amadurecer quase nunca vem com festa. Vem num \"não\" dito sem culpa, numa saída cedo, numa tarde sem plano.\n\n"
               "Qual desses sinais você já percebeu em você? Manda pra quem está crescendo calado. 🤍\n\n"
               "#amadurecimento #autoconhecimento #pazinterior #reflexão #verdadesatemporais"),
}


def enfileirar(nome):
    numero, pasta, data, hora, legenda = AGENDA[nome]
    origem = os.path.join(RAIZ, 'rebrand', 'saida', f'lote-{nome}')
    destino = os.path.join(RAIZ, 'posts', pasta)
    os.makedirs(destino, exist_ok=True)
    imagens = []
    for f in sorted(os.listdir(origem)):
        if f.endswith('.jpg'):
            shutil.copy(os.path.join(origem, f), os.path.join(destino, f))
            imagens.append(f'posts/{pasta}/{f}')
    assert len(imagens) == 6, f'{nome}: só {len(imagens)} slides'
    caminho = os.path.join(RAIZ, 'fila.json')
    fila = [p for p in json.load(open(caminho)) if p.get('chave') != numero]
    fila.append({'numero': numero, 'chave': numero, 'data': data, 'hora': hora,
                 'destinos': ['instagram', 'facebook'], 'imagens': imagens, 'legenda': legenda})
    json.dump(fila, open(caminho, 'w'), ensure_ascii=False, indent=1)
    print('na fila:', numero, data, hora)


if __name__ == '__main__':
    for n in sys.argv[1:]:
        enfileirar(n)
