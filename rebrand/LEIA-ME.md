# Rebrand Verdades Atemporais (nov/2026)

Tudo do rebrand vive aqui, nunca só no espaço de uma conversa. Marca (logo, cores, assinatura) fica em `../marca/`.

## Formatos em teste

### 1. Carrossel METÁFORA (`carrossel_metafora.py`)
Inspiração: carrosséis de psicólogas que cruzam frase com objeto.
- Cada slide: uma frase que todo mundo já disse, entre aspas, sobre um objeto que mostra o que ela esconde.
- Imagens: Gemini, natureza-morta com luz de janela, paleta neutra, sem texto, terço de baixo livre.
- Texto: Poppins Bold 74, branco quente (#FCF9F3), centralizado, com uma faixa escura suave atrás para ler em fundo claro.
- Capa com gancho pequeno no topo; último slide fecha com a virada e o "manda pra quem".
- Exemplo pronto: `saida/metafora-limite/` (fotos em `fotos/metafora/`, va-meta-01 a 07).

### 1b. Carrossel METÁFORA ILUSTRADA (`carrossel_ilustrado.py`) — preferida do Levy
Mesmo roteiro da metáfora, mas em pintura de guache com cenas de casa brasileira do interior (paredes ocre e pêssego, portas azul cobalto, toalha florida, gente de pele marrom com rosto simples).
- Imagens: Gemini, `va-ilu-NN` (refeitas: `va-ilu-rNN` ou `va-ilu-NNb`, o script usa a mais nova).
- O terço de cima tem que ser parede ou céu pintado, vazio. Pedir sempre "fill the entire canvas, no blank band, no border", senão o Gemini deixa uma faixa branca.
- Título: letras à mão empilhadas (`letreiro`, fonte Amatic SC Bold engrossada, leve irregularidade por letra), tinta quase preta; em cena noturna, creme.
- Exemplo pronto: `saida/ilustrada-limite/`.

### 2. Carrossel LISTA COM VIRADA (`carrossel_lista.py`)
Inspiração: listas "Tema: resposta curta" sobre paisagem.
- Abre com pergunta, cada slide traz **Rótulo:** + resposta curta, fecha devolvendo a pergunta e com o "manda pra quem".
- Imagens: Unsplash, uma pessoa pequena numa paisagem ampla, céu livre em cima.
- Texto: Inter Bold + Regular 56, alinhado à esquerda no topo; cor escolhida pela luminosidade do céu (preto ou branco).
- Exemplo pronto: `saida/lista-esperando/` (fotos em `fotos/lista/`).

## Regras comuns
- 1080 x 1350 (4:5). Uma imagem diferente por slide.
- Assinatura em todo slide: carinha + @verdades_atemporais no canto inferior direito, branca ou preta conforme o fundo.
- Grão leve de filme em tudo, para unificar fontes diferentes de imagem.
- Sem palavrão, sem citação de autor, frases originais.
- Sem palavra sozinha na última linha (o `escrever` reequilibra).

## Como gerar imagens no Gemini
E-mail para levytikus@gmail.com com assunto `CTD GERAR: <nome>` e o prompt no corpo (regras gerais + lista numerada com nome de arquivo). A automação gera e salva no Drive com os nomes pedidos em cerca de 4 a 6 minutos.
Atenção: os nomes dos arquivos precisam começar exatamente com o nome do assunto (assunto `va-ilu-r` → arquivos `va-ilu-r01`...). Pedido com nomes fora desse padrão não volta.

## Fontes
Em `fontes/` (Inter e Poppins), para rodar igual em qualquer máquina.
