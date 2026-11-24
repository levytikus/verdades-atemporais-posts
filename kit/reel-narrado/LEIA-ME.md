# Reel narrado (modelo aprovado "Encante-se", versão automática)

Decisão do Levy em 24/11/2026: narração com voz de IA (sem passo manual), texto original da página. A voz da Microsoft (gerar-voz.yml) foi REPROVADA por soar robótica: use sempre o Gemini.

1. Voz: no repositório levytikus/ctd-imagens, crie narracoes/verdades-<slug>/texto.txt e config.json (modelo gemini-3.8-flash-tts, voz Achird, ritmo_alvo 0, estilo de amigo falando baixo de madrugada; veja narracoes/verdades-caber). O push dispara o narrar.yml, que salva narr.wav. Copie para kit/voz/<nome>.wav aqui.
1b. Tempo das palavras: fluxo **Alinhar narração** (`alinhar-voz.yml`, faster-whisper medium) gera kit/voz/<nome>-palavras.json; o texto.py casa com o texto original (pra/para, pros/para os).
2. Clipes: fluxo **Baixar clipe** (`baixar-clipe.yml`) com o endereço direto do vídeo. Mixkit (licença livre, sem crédito): `https://assets.mixkit.co/videos/<id>/<id>-1080.mp4` (se der 403, tente `-720.mp4`; IDs acima de 100000 costumam falhar). Rode um de cada vez: a fila do GitHub só guarda um pendente.
3. `fundo.py`: corta cada clipe em 9:16, aproximação lenta, cor, vinheta, granulação e fusões de 0,35 s (edite CENAS e T).
4. `texto.py`: legenda palavra por palavra em Lora no centro, destaques em Lora itálico amarelo trator, assinatura com `marca/va-circulo-1080.png` e fechamento com a piscada (`marca/piscada.py`). Edite QUEBRAS (onde a tela troca de frase) e DESTAQUE.
5. Junte as partes, voz com 0,3 s de atraso e `kit/musicas/piano-reflexivo.mp3` baixinho, normalizado em -14 LUFS.

Primeiro exemplo: `posts/reel-caber-1124/reel.mp4` ("Você não precisa se diminuir pra caber").
