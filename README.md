# Verdades Atemporais · posts

Imagens e automação de publicação do Instagram [@verdades_atemporais](https://instagram.com/verdades_atemporais) e da página do Facebook.

- `posts/`: imagens de cada post (1080×1350, JPEG), uma pasta por número.
- `fila.json`: o que sai em cada dia (data, horário, imagens ou vídeo, legenda, destinos).
- `publicar.py` + `.github/workflows/publicar.yml`: todo dia publica o que estiver na fila para aquele horário (desde 23/11/2026, 1 post por dia às 20h de Brasília) pela API oficial da Meta. Itens com `"video"` saem como Reel; se o Reel falhar e houver imagens, sai a imagem no lugar.
- `metricas.py` + `.github/workflows/metricas.yml`: toda segunda e terça cedo grava em `metricas.json` os números dos posts (alcance, visualizações, salvamentos, compartilhamentos) e os seguidores.
- `publicados.json`: registro do que já foi publicado (a automação não repete).
- `kit/`: gerador das imagens, cenas, fonte, regras da página e histórico.

## Comandos manuais

Em **Actions → Publicar post do dia → Run workflow**:
- marque *Só testar a chave* para conferir se a ligação com a Meta está funcionando;
- ou preencha um número para publicar aquele post na hora;
- ou preencha um número (ou chave, ex.: `821-reel`) e marque *Testar Reel* para enviar o vídeo ao Instagram e conferir o processamento, sem publicar nada.

A chave da Meta fica em **Settings → Secrets and variables → Actions → META_TOKEN** e nunca aparece no código.

## Ritmo desde 23/11/2026

Decisão do Levy com base nos insights de 26/10 a 22/11: com 3 posts por dia, a mediana de alcance caiu para 17 a 23 contas por post e só cerca de 14% dos seguidores viam os posts. A página passou a ter **1 post por dia às 20h**, misturando Reels e carrosséis (pedido do Levy): os posts de imagem única saem como Reel (imagem inteira com música, `python3 kit/reel.py --inteira --imagens <img> --numero <n> --saida <pasta>/reel.mp4`) e os carrosséis seguem como carrossel. Em outubro os Reels de frase tiveram alcance mediano de 110, contra 12 a 21 dos posts do feed. Plano: 2 Reels por semana, um teste de impulso de R$ 20 por 3 dias no post com melhor reação orgânica da semana e balanço em 14 dias (meta: mediana de alcance acima de 60 por post).
