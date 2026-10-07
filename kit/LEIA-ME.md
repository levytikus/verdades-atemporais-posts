# Kit Verdades Atemporais

Pasta usada pelo processo semanal para gerar os posts do @verdades_atemporais.

## Conteúdo

- `gerar2.py`: gerador atual. Uso: `python3 gerar2.py lote.json cenas.json pasta_das_fotos pasta_de_saida` (`--debug` mostra a área detectada). Estilos de escrita: marcador, caneta, mão, lápis, giz de cera, máquina, recibo, carimbo, impresso, serifa, tela, pincel, batom, letreiro, giz, feltro, neon, led.
- `gerar.py`: gerador antigo (cenas fixas), usado até o Nº 820. Gera as imagens a partir de um lote em JSON. Uso: `python3 gerar.py lote.json pasta_de_saida`.
  Requer Python com `playwright` (com Chromium instalado), `opencv-python-headless`, `numpy` e `pillow`.
- `bases/`: as 6 cenas limpas (placa, metro, placas, papel, outdoor, enter).
- `fonts/`: a fonte Archivo.
- `historico.md`: os posts já feitos, para não repetir frases.

## Regras da página

- **Numeração:** continua a contagem do Instagram. O último post pronto é o Nº 843.
- **Cor de destaque:** cada post tem uma cor, sempre nesta ordem: verde, laranja, azul, rosa, amarelo, vermelho, verde limão, azul bebê, roxo, amarelo trator, rosa choque, e depois recomeça. O 815 foi roxo, então o 821 é rosa, o 822 amarelo e o 823 vermelho. O `gerar.py` calcula a cor sozinho a partir do número.
- **Regra de ouro (desde o Nº 821):** nenhuma imagem repetida. Cada slide tem uma cena inédita, gerada no Canva, com um objeto do mundo real diferente (bilhete, lousa, neon, etiqueta, espelho, painel de aeroporto...). As fotos antigas de `bases/` servem só de inspiração. Use `gerar2.py` com um `cenas-*.json` (estilo de escrita por slide) e a pasta com as fotos exportadas do Canva.
- **Visual:** a frase aparece num objeto do mundo real (cena). Tipografia pesada em caixa alta, uma palavra marcada com a cor do post e uma linha de apoio menor. No topo aparece só o número (Nº 821), discreto.
- **Cenas:** alternar entre placa, metro, placas, papel, outdoor e enter, sem repetir a mesma cena em posts seguidos. O enter serve para posts de interação ("complete a frase").
- **Frases:** sempre originais. Nada de citações nem nome de autor nas imagens.
- **Calendário:** 1 post por dia, todos os dias, às 20h (horário de Brasília). Cada lote semanal tem 7 posts.
- **Formatos:** misturar carrosséis (4 a 6 slides) e posts únicos. Por semana, 2 ou 3 carrosséis e 1 ou 2 posts de interação.
- **Legendas:** 3 a 6 linhas, tom próximo e reflexivo, uma pergunta ou chamada para salvar, comentar ou enviar, e 5 ou 6 hashtags começando por #verdadesatemporais.

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
