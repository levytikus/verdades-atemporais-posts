"""Coleta os números dos posts publicados (Instagram) e grava em metricas.json.

Roda pelo GitHub Actions (.github/workflows/metricas.yml), toda segunda de manhã, antes do lote semanal.
O lote semanal lê metricas.json para decidir quais temas e formatos dobrar.

Para cada post em publicados.json com chave "...:instagram", busca:
  tipo (REELS, CAROUSEL_ALBUM, IMAGE), alcance, visualizações, curtidas, comentários,
  salvamentos, compartilhamentos e interações totais.
Também grava seguidores e total de posts da conta, com a data, para acompanhar o crescimento.
"""
import json, os, datetime, pathlib
from zoneinfo import ZoneInfo
import requests

V = os.environ.get('GRAPH_VERSION', 'v24.0')
G = f'https://graph.facebook.com/{V}'
RAIZ = pathlib.Path(__file__).parent
TOKEN = os.environ.get('META_TOKEN', '').strip()
HOJE = datetime.datetime.now(ZoneInfo('America/Sao_Paulo')).date().isoformat()


def get(path, **params):
    params['access_token'] = TOKEN
    j = requests.get(f'{G}/{path}', params=params, timeout=60).json()
    if 'error' in j:
        raise RuntimeError(f'{path}: {j["error"].get("message")}')
    return j


def conta_instagram():
    ig = os.environ.get('IG_USER_ID')
    if ig: return ig
    for c in get('me/accounts', fields='name,instagram_business_account', limit=100).get('data', []):
        if 'verdades' in c['name'].lower() and c.get('instagram_business_account'):
            return c['instagram_business_account']['id']
    raise RuntimeError('Conta do Instagram não encontrada.')


def main():
    publicados = json.loads((RAIZ / 'publicados.json').read_text() or '{}')
    fila = {str(p.get('chave', p['numero'])): p for p in json.loads((RAIZ / 'fila.json').read_text())}
    arq = RAIZ / 'metricas.json'
    dados = json.loads(arq.read_text()) if arq.exists() else {'conta': [], 'posts': {}}

    ig = conta_instagram()
    c = get(ig, fields='followers_count,media_count')
    dados['conta'] = [x for x in dados['conta'] if x['data'] != HOJE] + [
        {'data': HOJE, 'seguidores': c.get('followers_count'), 'posts': c.get('media_count')}]

    for chave, info in publicados.items():
        if not chave.endswith(':instagram'): continue
        k = chave.rsplit(':', 1)[0]
        mid = info['id']
        try:
            m = get(mid, fields='media_type,media_product_type,timestamp,permalink')
            tipo = 'REELS' if m.get('media_product_type') == 'REELS' else m.get('media_type')
            for met in ('reach,views,likes,comments,saved,shares,total_interactions',
                        'reach,likes,comments,saved,shares'):
                try:
                    bruto = get(f'{mid}/insights', metric=met).get('data', []); break
                except RuntimeError:
                    bruto = []
            ins = {x['name']: (x.get('values') or [{}])[0].get('value', x.get('total_value', {}).get('value'))
                   for x in bruto}
        except Exception as e:
            print(f'Sem números para {k}: {e}'); continue
        p = fila.get(k, {})
        dados['posts'][k] = {'numero': p.get('numero'), 'data': p.get('data'), 'hora': p.get('hora'), 'tipo': tipo,
                             'link': m.get('permalink'), 'atualizado': HOJE, **ins}
        print(k, tipo, ins)

    arq.write_text(json.dumps(dados, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    if not TOKEN: raise SystemExit('Falta o segredo META_TOKEN.')
    main()
