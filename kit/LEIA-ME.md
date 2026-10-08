# Kit Verdades Atemporais

Pasta usada pelo processo semanal para gerar os posts do @verdades_atemporais.

## Conteúdo

- `gerar2.py`: gerador atual. Uso: `python3 gerar2.py lote.json cenas.json pasta_das_fotos pasta_de_saida` (`--debug` mostra a área detectada). Estilos de escrita: marcador, caneta, mão, lápis, giz de cera, máquina, recibo, carimbo, impresso, serifa, tela, pincel, batom, letreiro, giz, feltro, neon, led.
- `reel.py`: transforma as imagens de um post num Reel vertical 1080×1920 com música (`python3 kit/reel.py 850` gera `posts/850-.../reel.mp4` a partir do fila.json). Requer ffmpeg, pillow e numpy.
- `story.py`: gera o Story das 20h05 a partir da primeira imagem do post do feed (`python3 kit/story.py 850`).
- `musicas/`: trilhas livres de direitos geradas para a página (o reel.py escolhe uma pelo número). Para acrescentar uma trilha: gerar no vidIQ e baixar com o workflow "Baixar trilha sonora".
- `gerar.py`: gerador antigo (cenas fixas), usado até o Nº 820. Gera as imagens a partir de um lote em JSON. Uso: `python3 gerar.py lote.json pasta_de_saida`.
  Requer Python com `playwright` (com Chromium instalado), `opencv-python-headless`, `numpy` e `pillow`.
- `bases/`: as 6 cenas limpas (placa, metro, placas, papel, outdoor, enter).
- `fonts/`: a fonte Archivo.
- `historico.md`: os posts já feitos, para não repetir frases.

## Regras da página

- **Numeração:** continua a contagem do Instagram. O último post pronto é o Nº 843.
- **Cor de destaque:** cada post tem uma cor, sempre nesta ordem: verde, laranja, azul, rosa, amarelo, vermelho, verde limão, azul bebê, roxo, amarelo trator, rosa choque, e depois recomeça. O 815 foi roxo, então o 821 é rosa, o 822 amarelo e o 823 vermelho. O `gerar.py` calcula a cor sozinho a partir do número.
- **Regra de ouro (desde o Nº 821):** nenhuma cena repetida entre posts. Cada post tem uma cena inédita, gerada no Canva, com um objeto do mundo real diferente (bilhete, lousa, neon, etiqueta, espelho, painel de aeroporto...).
- **Carrosséis (regra do Levy, desde 08/10/2026):** todos os slides usam a MESMA cena, mudando só o texto. Dá unidade ao carrossel e economiza a cota de IA do Canva (cerca de 200 gerações por mês no Pro). No `cenas-*.json`, os slides do mesmo post apontam para a mesma foto (copie o arquivo para `{numero}-01`, `{numero}-02`...) e repetem a mesma `caixa`. As fotos antigas de `bases/` servem só de inspiração. Use `gerar2.py` com um `cenas-*.json` (estilo de escrita por slide) e a pasta com as fotos exportadas do Canva.
- **Visual:** a frase aparece num objeto do mundo real (cena). Tipografia pesada em caixa alta, uma palavra marcada com a cor do post e uma linha de apoio menor. No topo aparece só o número (Nº 821), discreto.
- **Cenas:** alternar entre placa, metro, placas, papel, outdoor e enter, sem repetir a mesma cena em posts seguidos. O enter serve para posts de interação ("complete a frase").
- **Frases:** sempre originais. Nada de citações nem nome de autor nas imagens.
- **Estratégia (desde 07/10/2026): Reel primeiro.** A página tinha zero Reels e por isso não chegava a quem não segue. Agora são 2 publicações por dia:
  - **12h · Reel de frase:** uma frase forte, uma cena só, publicada como Reel (`"video"` no fila.json, gerado com `reel.py`). Frases de identificação e contraste, escritas para serem enviadas a alguém.
  - **20h · post do feed:** como sempre (posts únicos, carrosséis e interação), numerados, como imagem ou carrossel. Nunca como Reel.
  - **20h05 · Story:** a verdade da noite em 1080×1920 com a etiqueta "NOVA VERDADE NO FEED" na cor do post, gerada com `python3 kit/story.py <numero>` (fica em `posts/<pasta>/story.jpg`). Entra no fila.json logo depois do post do feed, com `"chave": "<numero>-story"`, hora "20:05" e `"story"`. Story pode mostrar o Nº, porque divulga o post numerado.
  - Cada lote semanal tem 14 itens: 7 Reels de frase (12h) + 7 posts do feed (20h), e cada post do feed ganha o seu Story.
- **Contagem (regra do Levy):** o "Nº" é exclusivo dos posts do feed (20h) e só eles avançam a numeração e a sequência de cores. Reels **não têm número**: o `reel.py` corta a faixa do Nº e o rodapé e escreve só o @verdades_atemporais embaixo da imagem. Os Reels saem só na aba Reels (não aparecem na grade do perfil): a grade é exclusiva das verdades numeradas. No fila.json, o Reel usa o `numero` do post do feed do mesmo dia (só para a cor e a pasta) e `"chave": "<numero>-reel"`; a legenda do Reel não cita número, a não ser que convide para o post da noite ("Hoje às 20h ela entra no feed como a verdade Nº X").
- **Temas da fase de teste:** tempo e finitude (25%), quem fica nas fases difíceis (20%), julgamento e empatia (15%), caráter e valores (15%), aprovação e autenticidade (15%), maturidade e perdão a si mesmo (10%). Ajustar toda semana pelo `metricas.json` (dobrar o que tem mais compartilhamentos e alcance).
- **Formatos da noite:** misturar carrosséis (4 a 6 slides) e posts únicos. Por semana, 2 ou 3 carrosséis e 1 ou 2 posts de interação.
- **Reels:** o reel.py corta sozinho o Nº (faixa de cima) e o rodapé de qualquer imagem; deixe a frase longe das bordas de cima e de baixo (pelo menos 110 px).
- **Legendas:** 3 a 6 linhas; nos Reels, a primeira linha é a própria frase (é o que aparece antes do "mais"), tom próximo e reflexivo, uma pergunta ou chamada para salvar, comentar ou enviar, e 5 ou 6 hashtags começando por #verdadesatemporais.

## Formato do lote (lote.json)

```json
[
 {"numero": 821, "cena": "papel", "slug": "coragem", "data": "2026-10-19",
  "slides": [{"linhas": ["Coragem", "não é não"], "destaque": "ter medo.", "apoio": "É ir mesmo assim."}],
  "legenda": "..."},
 {"numero": 822, "cena": "placas", "slug": "limites",
  "slides": [{"branca": ["Dizer não", "também é"], "preta": ["um jeito de", "se cuidar."]}]},
 {"numero": 823, "cena": "enter", "slug": "complete",
  "slides": [{"linhas": ["Hoje eu", "escolho"], "lacuna": true, "apoio": "Complete nos comentários|e aperte enter."}]}
]
```

Linhas curtas funcionam melhor (até uns 12 caracteres): o texto é ajustado para ocupar o espaço, e linhas longas deixam a letra pequena.
