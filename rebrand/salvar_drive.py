"""Salva imagens baixadas do Drive (JSON com title + content base64) numa pasta. Uso: python3 salvar_drive.py <pasta> <json...>"""
import base64, json, os, sys
dest = sys.argv[1]
os.makedirs(dest, exist_ok=True)
for p in sys.argv[2:]:
    d = json.load(open(p))
    open(os.path.join(dest, d['title']), 'wb').write(base64.b64decode(d['content']))
    print(d['title'])
