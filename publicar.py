"""Publica no Instagram e no Facebook o post do dia do @verdades_atemporais.

Roda pelo GitHub Actions (.github/workflows/publicar.yml). Lê fila.json, acha o post com a
data de hoje (horário de Brasília), publica pela API oficial da Meta e anota em publicados.json.

Variáveis de ambiente:
  META_TOKEN   chave de acesso (segredo do repositório)          obrigatória
  PAGE_ID      id da página do Facebook                          opcional (descobre sozinho)
  IG_USER_ID   id da conta do Instagram                          opcional (descobre sozinho)
  NUMERO       publicar este número agora, ignorando a data      opcional
  VERIFICAR    "1" = só testa a chave e mostra o que faria       opcional
"""
import json, os, sys, time, datetime, pathlib
from zoneinfo import ZoneInfo
import requests

V = os.environ.get('GRAPH_VERSION', 'v24.0')
G = f'https://graph.facebook.com/{V}'
RAIZ = pathlib.Path(__file__).parent
TOKEN = os.environ.get('META_TOKEN', '').strip()
REPO = os.environ.get('GITHUB_REPOSITORY', 'levytikus/verdades-atemporais-posts')
REF = os.environ.get('GITHUB_SHA', 'main')
BR = ZoneInfo('America/Sao_Paulo')
AGORA = datetime.datetime.now(BR)
HOJE = AGORA.date().isoformat()
# Margem antes do horário do post. Execuções antes disso não publicam nada.
ANTECEDENCIA = datetime.timedelta(minutes=int(os.environ.get('ANTECEDENCIA_MIN', '15')))

def na_hora(post):
    """True se já chegou a hora do post (mesmo dia, a partir de hora - margem).
    Execuções atrasadas do GitHub que caem depois da meia-noite não adiantam o post do dia seguinte."""
    h, m = map(int, post.get('hora', '20:00').split(':'))
    quando = datetime.datetime.fromisoformat(post['data']).replace(hour=h, minute=m, tzinfo=BR)
    return AGORA >= quando - ANTECEDENCIA

def api(method, path, token, **params):
    params['access_token'] = token
    r = requests.request(method, f'{G}/{path}', data=params if method == 'POST' else None,
                         params=None if method == 'POST' else params, timeout=120)
    j = r.json()
    if r.status_code >= 400 or 'error' in j:
        raise RuntimeError(f'{method} {path}: {j.get("error", j)}')
    return j

def descobrir():
    page_id, ig_id = os.environ.get('PAGE_ID'), os.environ.get('IG_USER_ID')
    contas = api('GET', 'me/accounts', TOKEN, fields='id,name,access_token,instagram_business_account', limit=100).get('data', [])
    if not contas:
        raise RuntimeError('A chave não enxerga nenhuma página do Facebook. Confira se a página foi atribuída ao usuário do sistema.')
    escolha = None
    for c in contas:
        if (page_id and c['id'] == page_id) or (not page_id and 'verdades' in c['name'].lower()):
            escolha = c; break
    escolha = escolha or contas[0]
    ig_id = ig_id or (escolha.get('instagram_business_account') or {}).get('id')
    if not ig_id:
        raise RuntimeError(f'A página "{escolha["name"]}" não tem conta do Instagram profissional ligada.')
    return escolha['id'], escolha['name'], escolha.get('access_token') or TOKEN, ig_id

def url(caminho): return f'https://raw.githubusercontent.com/{REPO}/{REF}/{caminho}'

def esperar(container, token):
    for _ in range(60):
        st = api('GET', container, token, fields='status_code').get('status_code')
        if st == 'FINISHED': return
        if st in ('ERROR', 'EXPIRED'): raise RuntimeError(f'Instagram recusou a mídia {container}: {st}')
        time.sleep(5)
    raise RuntimeError(f'Tempo esgotado esperando a mídia {container}')

def publicar_instagram(ig, token, post):
    imgs = post['imagens']
    if len(imgs) == 1:
        c = api('POST', f'{ig}/media', token, image_url=url(imgs[0]), caption=post['legenda'])['id']
    else:
        filhos = []
        for im in imgs:
            f = api('POST', f'{ig}/media', token, image_url=url(im), is_carousel_item='true')['id']
            esperar(f, token); filhos.append(f)
        c = api('POST', f'{ig}/media', token, media_type='CAROUSEL', children=','.join(filhos), caption=post['legenda'])['id']
    esperar(c, token)
    return api('POST', f'{ig}/media_publish', token, creation_id=c)['id']

def publicar_facebook(page, token, post):
    imgs = post['imagens']
    if len(imgs) == 1:
        return api('POST', f'{page}/photos', token, url=url(imgs[0]), message=post['legenda'])['id']
    ids = [api('POST', f'{page}/photos', token, url=url(im), published='false')['id'] for im in imgs]
    extra = {f'attached_media[{i}]': json.dumps({'media_fbid': x}) for i, x in enumerate(ids)}
    return api('POST', f'{page}/feed', token, message=post['legenda'], **extra)['id']

def main():
    if not TOKEN: sys.exit('Falta o segredo META_TOKEN no repositório.')
    fila = json.loads((RAIZ/'fila.json').read_text())
    pub_f = RAIZ/'publicados.json'; publicados = json.loads(pub_f.read_text() or '{}')
    page, nome, page_token, ig = descobrir()
    print(f'Página: {nome} ({page}) · Instagram: {ig} · hoje: {HOJE}')
    numero = os.environ.get('NUMERO', '').strip()
    posts = [p for p in fila if str(p['numero']) == numero] if numero else [p for p in fila if p['data'] == HOJE]
    if not posts:
        print('Nenhum post para hoje na fila.'); return
    if not numero:
        cedo = [p for p in posts if not na_hora(p)]
        for p in cedo: print(f'Ainda não é hora do Nº {p["numero"]} ({p["data"]} {p.get("hora", "20:00")}); nada a fazer agora.')
        posts = [p for p in posts if p not in cedo]
        if not posts: return
    if os.environ.get('VERIFICAR') == '1':
        for p in posts: print(f'[teste] publicaria Nº {p["numero"]} ({len(p["imagens"])} imagem/ns) em {p["destinos"]}')
        print('Chave e contas OK.'); return
    erros = []
    for p in posts:
        for destino in p.get('destinos', ['instagram']):
            chave = f'{p["numero"]}:{destino}'
            if chave in publicados: print(f'Já publicado: {chave}'); continue
            try:
                pid = publicar_instagram(ig, TOKEN, p) if destino == 'instagram' else publicar_facebook(page, page_token, p)
                publicados[chave] = {'id': pid, 'quando': datetime.datetime.now(ZoneInfo('America/Sao_Paulo')).isoformat(timespec='minutes')}
                print(f'Publicado {chave} → {pid}')
            except Exception as e:
                erros.append(f'{chave}: {e}'); print(f'ERRO {chave}: {e}')
            pub_f.write_text(json.dumps(publicados, ensure_ascii=False, indent=1))
    if erros: sys.exit('Falhas:\n' + '\n'.join(erros))

if __name__ == '__main__':
    try:
        main()
    except SystemExit as e:
        if e.code not in (None, 0):
            print('::error::' + str(e.code).replace('\n', ' | ')); raise
    except Exception as e:
        print(f'::error::{type(e).__name__}: {e}'); raise
