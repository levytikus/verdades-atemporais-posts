"""Texto para o modo Tarefas do Gemini: gera as imagens e salva na raiz do Drive com o nome certo.
Uso: python3 tarefa_gemini.py <chave> [<chave> ...]  -> JSON {chave: texto}"""
import json, sys
from semana_nov08 import email
out = {}
for k in sys.argv[1:]:
    t = email(k).replace('Save each with the exact file name given.',
        'Save each one as a PNG file in the root folder of my Google Drive (My Drive) with the exact file name given plus ".png".')
    out[k] = ' '.join(l for l in t.splitlines() if l.strip())
print(json.dumps(out, ensure_ascii=False))
