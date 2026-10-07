# Verdades Atemporais · posts

Imagens e automação de publicação do Instagram [@verdades_atemporais](https://instagram.com/verdades_atemporais) e da página do Facebook.

- `posts/`: imagens de cada post (1080×1350, JPEG), uma pasta por número.
- `fila.json`: o que sai em cada dia (data, horário, imagens ou vídeo, legenda, destinos).
- `publicar.py` + `.github/workflows/publicar.yml`: todo dia, às 12h e às 20h de Brasília, publica o que estiver na fila para aquele horário pela API oficial da Meta. Itens com `"video"` saem como Reel; se o Reel falhar e houver imagens, sai a imagem no lugar.
- `metricas.py` + `.github/workflows/metricas.yml`: toda segunda e terça cedo grava em `metricas.json` os números dos posts (alcance, visualizações, salvamentos, compartilhamentos) e os seguidores.
- `publicados.json`: registro do que já foi publicado (a automação não repete).
- `kit/`: gerador das imagens, cenas, fonte, regras da página e histórico.

## Comandos manuais

Em **Actions → Publicar post do dia → Run workflow**:
- marque *Só testar a chave* para conferir se a ligação com a Meta está funcionando;
- ou preencha um número para publicar aquele post na hora;
- ou preencha um número (ou chave, ex.: `821-reel`) e marque *Testar Reel* para enviar o vídeo ao Instagram e conferir o processamento, sem publicar nada.

A chave da Meta fica em **Settings → Secrets and variables → Actions → META_TOKEN** e nunca aparece no código.
