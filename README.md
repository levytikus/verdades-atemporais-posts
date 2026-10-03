# Verdades Atemporais · posts

Imagens e automação de publicação do Instagram [@verdades_atemporais](https://instagram.com/verdades_atemporais) e da página do Facebook.

- `posts/`: imagens de cada post (1080×1350, JPEG), uma pasta por número.
- `fila.json`: o que sai em cada dia (data, horário, imagens, legenda, destinos).
- `publicar.py` + `.github/workflows/publicar.yml`: todo dia, por volta das 20h de Brasília, publica o post da data pela API oficial da Meta.
- `publicados.json`: registro do que já foi publicado (a automação não repete).
- `kit/`: gerador das imagens, cenas, fonte, regras da página e histórico.

## Comandos manuais

Em **Actions → Publicar post do dia → Run workflow**:
- marque *Só testar a chave* para conferir se a ligação com a Meta está funcionando;
- ou preencha um número para publicar aquele post na hora.

A chave da Meta fica em **Settings → Secrets and variables → Actions → META_TOKEN** e nunca aparece no código.
