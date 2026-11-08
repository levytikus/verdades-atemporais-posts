"""Importa imagens baixadas do Gemini (via Drive) para fotos/ilustrada/vb-<chave>NN.png.
Uso: python3 importar.py <chave> <titulo1> <titulo2> ...   (títulos na ordem dos slides)
Procura os arquivos salvos pelas ferramentas em /tmp/claude-tool-results/*/mcp-Google_Drive-download_file_content-*.txt"""
import base64, glob, io, json, os, sys
from PIL import Image
chave, titulos = sys.argv[1], sys.argv[2:]
achados = {}
for p in glob.glob('/tmp/claude-tool-results/*/mcp-Google_Drive-download_file_content-*.txt'):
    try:
        d = json.load(open(p))
    except Exception:
        continue
    if d.get('title') in titulos:
        achados[d['title']] = d['content']
for i, t in enumerate(titulos, 1):
    im = Image.open(io.BytesIO(base64.b64decode(achados[t]))).convert('RGB')
    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fotos', 'ilustrada', f'vb-{chave}{i:02d}.png')
    im.save(destino); print(os.path.basename(destino), im.size)
