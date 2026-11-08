"""Um pedido único para o modo Tarefas do Gemini cobrindo vários posts (cada um com sua paleta).
Uso: python3 tarefa_lote.py <chave> [<chave> ...]  -> texto em uma linha (JSON string)"""
import json, sys
from semana_nov08 import P, CAT, CATEGORIA, ESTILO
partes = []
total = 0
for k in sys.argv[1:]:
    _, num, data, hora, ideia, elenco, slides, leg = P[k]
    c = CAT[CATEGORIA[k]]
    cenas = [cena for _t, cena in slides]
    if len(cenas) == 1:
        cenas.append(cenas[0] + ' Alternative composition, different angle.')
    total += len(cenas)
    itens = ' '.join(f'vb-{k}{i:02d}.png: {cena}' for i, cena in enumerate(cenas, 1))
    partes.append(f'SERIES "{k}" ({len(cenas)} images). IDEA: {ideia}. CHARACTERS: {elenco} Keep the same look in every image of this series. '
                  f'COLOR PALETTE of this series (use only this): {c["paleta"]}. WORLD: {c["mundo"]}. TYPE OF CHARACTERS: {c["elenco"]}. '
                  f'TYPICAL OBJECTS: {c["objetos"]}. IMAGES: {itens}')
estilo = ESTILO.replace('vertical 4:5 (1080x1350)', 'vertical 4:5 portrait format')
texto = (f'Generate {total} separate illustrations, one at a time, in the order below, and save each one as a PNG file in the root folder '
         f'of my Google Drive (My Drive) with the exact file name given. Do not ask me anything. If one image fails, retry once and go on. '
         f'STYLE for ALL images: {estilo} Each series has its own color palette, world and characters, described below. ' + ' '.join(partes))
print(json.dumps(texto, ensure_ascii=False))
