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

## Ritmo desde 24/11/2026

Decisão do Levy: **carrossel às 11h30 e Reel narrado às 19h50**, todo dia. Os Reels seguem o modelo aprovado em 24/11 (`kit/reel-narrado/`, voz do Gemini Achird pelo repositório ctd-imagens, clipes reais, legenda palavra por palavra). Os Reels de imagem parada (rb-057, 063, 066, 069, 070 e 030) saíram da fila e ficam de reserva em `posts/`. O disparo principal é a tarefa agendada do Claude (11h29 e 19h49); os crons do GitHub são reserva.

## Grade intercalada e capas (25/11/2026)

Pedido do Levy: a grade do perfil intercala perfeitamente 1 Reel, 1 carrossel, 1 Reel, 1 carrossel. Por isso:
- Todo Reel narrado vai também para o feed (`"no_feed": true` na fila, que liga o share_to_feed) e sai só no modelo aprovado (voz Gemini, clipes reais, legenda palavra por palavra). Reel de imagem parada não entra mais.
- A ordem de publicação nunca pode ter dois do mesmo tipo seguidos no feed. Em 25/11 o carrossel da manhã foi cancelado (só Reel no dia) porque o último post do feed era carrossel; os carrosséis andaram um dia. Daqui pra frente: carrossel 11h30, Reel 19h50.
- Capa: todo Reel leva `"capa": "posts/<pasta>/capa.jpg"`, feita com `kit/reel-narrado/capa.py` (quadro limpo do clipe, frase de abertura grande no centro da área 3:4 da grade, destaque em amarelo, assinatura). Sem capa, o publicador usa `capa_ms` (padrão 3000 ms), nunca o 1º quadro, que sai preto.
