# Reel narrado (modelo aprovado "Encante-se", versão automática)

Decisão do Levy em 24/11/2026: narração com voz de IA (sem passo manual), texto original da página. A voz da Microsoft (gerar-voz.yml) foi REPROVADA por soar robótica: use sempre o Gemini.

1. Voz: no repositório levytikus/ctd-imagens, crie narracoes/verdades-<slug>/texto.txt e config.json (modelo gemini-3.8-flash-tts, voz Achird, ritmo_alvo 0, estilo de amigo falando baixo de madrugada; veja narracoes/verdades-caber). O push dispara o narrar.yml, que salva narr.wav. Copie para kit/voz/<nome>.wav aqui.
1b. Tempo das palavras: fluxo **Alinhar narração** (`alinhar-voz.yml`, faster-whisper medium) gera kit/voz/<nome>-palavras.json; o texto.py casa com o texto original (pra/para, pros/para os).
2. Clipes: fluxo **Baixar clipe** (`baixar-clipe.yml`) com o endereço direto do vídeo. Mixkit (licença livre, sem crédito): `https://assets.mixkit.co/videos/<id>/<id>-1080.mp4` (se der 403, tente `-720.mp4`; IDs acima de 100000 costumam falhar). Rode um de cada vez: a fila do GitHub só guarda um pendente.
3. `fundo.py`: corta cada clipe em 9:16, aproximação lenta, cor, vinheta, granulação e fusões de 0,35 s (edite CENAS e T).
4. `texto.py`: legenda palavra por palavra em Lora no centro, destaques em Lora itálico amarelo trator, assinatura com `marca/va-circulo-1080.png` e fechamento com a piscada (`marca/piscada.py`). Edite QUEBRAS (onde a tela troca de frase) e DESTAQUE.
5. Junte as partes, voz com 0,3 s de atraso e `kit/musicas/piano-reflexivo.mp3` baixinho, normalizado em -14 LUFS.

Primeiro exemplo: `posts/reel-caber-1124/reel.mp4` ("Você não precisa se diminuir pra caber").

## Tom: rodízio alegre e reflexivo (pedido do Levy em 24/11/2026)

O Levy gostou da linha, mas os reflexivos quase caem no melancólico, e ele quer MAIS dos alegres. Regra: dois alegres, um reflexivo (nunca dois reflexivos seguidos). Veja o tom do último Reel em kit/historico.md e marque o novo ([alegre] ou [reflexivo]).

- **Alegre** (pra cima): como a vida é boa, o poder da amizade, da família, das conquistas, das pequenas alegrias, da gratidão. Clipes claros e quentes: gente sorrindo, rindo junto, abraço, festa em casa, criança brincando, sol, praia, estrada, comemoração. Cor: saturation 0.95 a 1.0 e brightness 0 a -0.02 no fundo.py (não lavar a cor). Trilha: kit/musicas/alegre-sorriso.mp3, alegre-parque.mp3 ou alegre-ponte.mp3 (violão leve do Mixkit; alterne), volume 0.12. Voz: mesmo homem, com sorriso na voz e um pouco mais de energia, sem virar locutor.
- **Reflexivo**: pode tocar na dor, mas termina sempre em luz (esperança, carinho, um convite). Nada de cena triste demais (choro, pessoa encolhida no chão, escuridão): prefira introspecção serena e luz. Trilha: piano-reflexivo.mp3 em 0.15.

Na instrução de estilo da voz NUNCA ponha frases do roteiro entre aspas: em 24/11 o Gemini leu a instrução em voz alta (65 s). Cite só palavras soltas para ganhar peso.

## Obrigatório desde 25/11/2026: capa e feed (pedido do Levy)

- A grade do perfil intercala 1 Reel, 1 carrossel. Todo Reel entra na fila com `"no_feed": true` (vai para o feed) e com `"capa": "posts/<pasta>/capa.jpg"`.
- A capa é feita com `capa.py` (veja o cabeçalho do script): quadro claro do clipe, a frase de abertura grande no centro da área 3:4 e a assinatura. Confira o recorte y 240 a 1680. Capa escura ou o 1º quadro do vídeo (sai preto) nunca mais.
- Reel de imagem parada não entra mais na fila.
