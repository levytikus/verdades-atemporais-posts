"""Gera as mensagens para pedir uma série ao Gemini, uma imagem por mensagem.
Uso: python3 serie_gemini.py <chave>  -> imprime JSON com a lista de mensagens."""
import json, sys
from semana_nov08 import P, CAT, CATEGORIA, ESTILO
k = sys.argv[1]
_, num, data, hora, ideia, elenco, slides, leg = P[k]
c = CAT[CATEGORIA[k]]
cenas = [cena for _t, cena in slides]
estilo = ESTILO.replace('vertical 4:5 (1080x1350)', 'vertical 4:5 portrait format')
msgs = [(f"I will ask you for {len(cenas)} illustrations of one series, ONE image per message. Generate only ONE image now. "
         f"IDEA: {ideia}. CHARACTERS: {elenco} Keep the same look in every image where they appear. "
         f"STYLE for the whole series: {estilo} COLOR PALETTE for the whole series (use only this): {c['paleta']}. "
         f"WORLD: {c['mundo']}. TYPE OF CHARACTERS: {c['elenco']}. TYPICAL OBJECTS: {c['objetos']}. "
         f"IMAGE 1: {cenas[0]}")]
for i, cena in enumerate(cenas[1:], 2):
    msgs.append(f"IMAGE {i} (same style, palette, characters and rules; only one image, upper third plain and empty): {cena}")
print(json.dumps(msgs, ensure_ascii=False))
