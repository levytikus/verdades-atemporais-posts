"""Semana de 08 a 14/11/2026: 21 posts (12h, 18h, 21h), temas e formatos variados.
Uso:
  python3 semana_nov08.py email <chave>      imprime o pedido de imagens para o Gemini (assunto: CTD GERAR: va-<chave>)
  python3 semana_nov08.py gerar <chave...>   monta os slides em saida/semana/<chave>/
  python3 semana_nov08.py fila <chave...>    copia para posts/ e põe na fila.json
  python3 semana_nov08.py teste              prévia de encaixe dos textos (sem imagens)"""
import json, os, shutil, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import *

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, '..')
FOTOS = os.path.join(AQUI, 'fotos', 'ilustrada')
TINTA = (29, 26, 23)
CREME = (246, 237, 220)
_ = ('', 12)

ESTILO = ("vertical 4:5 (1080x1350), hand-painted gouache illustration, flat matte color shapes with visible dry brush "
          "texture, contemporary Brazilian editorial poster painted by hand, soft painted shadows, simplified figures "
          "with very simple expressive faces, diverse Brazilian people. The painting must fill the ENTIRE canvas "
          "edge to edge: NO blank band, NO white or plain border, NO paper margin anywhere. The scene sits in the lower two "
          "thirds; the upper third is simply the SAME wall or the SAME sky of the scene continuing upward to the top edge, same color, texture and wallpaper, free of objects, with NO horizontal line, NO edge, NO strip, NO band and NO separate block of color across the image. Any split-screen divider, window, curtain rod or flying object stays in the lower two thirds. "
          "NO text, NO letters, NO numbers, NO signature, NO watermark, NO readable screens or signs.")

# Cada categoria tem paleta, mundo, elenco e objetos próprios (pedido do Levy em 07/11/2026).
# A técnica (guache) é a assinatura comum da página; o resto muda de categoria pra categoria.
CAT = {
 'humor': dict(nome='Humor do dia a dia', tinta=(27, 24, 48),
   paleta='bold saturated pop colors: tomato red, sunflower yellow, turquoise, bubblegum pink and cobalt blue, crisp contrast',
   mundo='big Brazilian city life today: small rented apartments, crowded buses, offices, street corners, bakeries, convenience stores',
   elenco='young urban adults (20 to 35) with exaggerated comic expressions and lively body language, trendy everyday clothes',
   objetos='modern everyday things: phones, chargers, delivery bags, bills, snacks, sneakers'),
 'nostalgia': dict(nome='Nostalgia', tinta=(66, 42, 26),
   paleta='faded vintage tones like an old 1990s photograph: mustard, olive green, coffee brown, faded teal and yellowed cream, with soft film grain',
   mundo='1990s Brazilian homes: grandma\'s house, tiled floors, backyards with clotheslines, old kitchens',
   elenco='grandparents, aunts, uncles and children, people in 1990s clothes',
   objetos='tube TV, landline phone, clay water filter, crochet doilies, enamel mugs, photo albums'),
 'acolhimento': dict(nome='Acolhimento', tinta=(246, 237, 220),
   paleta='deep night blues, indigo and soft violet, with warm golden lamp or window light as the only warm color',
   mundo='bedrooms, windows, quiet streets and rooftops at night or at the first light of dawn',
   elenco='one person alone, introspective, in comfortable home clothes',
   objetos='bedside lamps, curtains, mugs, blankets, the moon'),
 'validacao': dict(nome='Limites e amadurecimento', tinta=(30, 52, 40),
   paleta='calm airy muted tones: sage green, sand, warm off-white, soft clay and pale sky blue, lots of breathing space',
   mundo='bright simple homes full of plants, morning light, quiet parks and verandas',
   elenco='adults between 30 and 50, serene and grounded, natural posture, linen and cotton clothes',
   objetos='plants, tea cups, books, hammocks, open windows'),
 'afeto': dict(nome='Afeto', tinta=(92, 28, 42),
   paleta='rosy warm tones: dusty pink, coral, wine red, peach and warm amber light',
   mundo='cozy kitchens, sofas, porches, small cafés and neighborhood stairs',
   elenco='couples, friends and neighbors interacting with tenderness and touch',
   objetos='shared food, coffee, radios, handwritten notes, string lights'),
 'motivacao': dict(nome='Seguir em frente', tinta=(22, 36, 72),
   paleta='open nature colors: emerald green, wide sky blue, sunrise orange and golden yellow',
   mundo='wide open spaces: red dirt roads, hills, valleys, open skies, big windows facing the horizon',
   elenco='small figures in a big space, travelers and students walking forward',
   objetos='backpacks, roads, sunrise, flowers by the road'),
 'causa': dict(nome='Novembro Azul', tinta=(16, 34, 78),
   paleta='shades of blue (navy, cobalt, sky blue) with white and warm skin tones',
   mundo='real everyday places: a clinic, a riverbank, a backyard, an old pickup truck',
   elenco='men of different ages, fathers and sons, friends',
   objetos='caps, fishing rods, appointment cards, blue shirts'),
}
CATEGORIA = {
 'enem': 'motivacao', 'familia': 'humor', 'domingo': 'acolhimento', 'pequenas': 'afeto', 'frescura': 'validacao',
 'completa': 'nostalgia', 'planos': 'humor', 'tempo': 'motivacao', 'amor': 'afeto', 'issoaquilo': 'humor',
 'azul': 'causa', 'some': 'acolhimento', 'avo': 'nostalgia', 'trabalho': 'humor', 'fase': 'acolhimento',
 'sexta13': 'humor', 'gente': 'afeto', 'dinheiro': 'humor', 'permissao': 'validacao', 'casal': 'humor', 'ano': 'acolhimento',
}
PREFIXO = 'vb'  # imagens novas (com categoria): vb-<chave>NN; as antigas va-<chave>NN ficam de reserva

# chave, número, data, hora, ideia, elenco, slides [(linhas, cena)], legenda
POSTS = [
 ('enem', 'rb-008', '2026-11-08', '12:00',
  'a short encouraging letter to a student on the day of the national university entrance exam (ENEM)',
  'Julia, 17, brown skin, curly black hair in a puff, big round glasses, white T-shirt, a transparent pencil case.', [
  ([('pra quem vai fazer', 85), ('o enem hoje:', 120)],
   'sunrise, Julia at the door of her simple house on a hill, backpack on, holding her transparent pencil case to her chest, looking at the wide orange sky, nervous but brave.'),
  ([('você não é', 112), ('uma nota.', 132)],
   'Julia walking up a road toward a school at the top of a green hill, many other students walking too, huge open blue sky, she breathes deeply.'),
  ([('respira, lê com calma', 72), ('e lembra do quanto', 72), ('você já chegou.', 96), _, ('manda pra quem vai fazer a prova', 40)],
   'classroom during an exam with a huge open window facing green hills and blue sky, Julia smiling calmly with her pen.'),
 ], "Hoje é dia de ENEM. Se você vai fazer a prova: respira, lê com calma e confia no que você estudou. Nenhuma nota diz quem você é.\n\n"
    "Manda pra alguém que vai fazer a prova hoje e deixa um \"boa prova\" aqui nos comentários. 🤍\n\n"
    "#enem2026 #enem #vestibular #boaprova #verdadesatemporais"),

 ('familia', 'rb-009', '2026-11-08', '18:00',
  'funny types of people in the family WhatsApp group; each image is an independent character',
  'different characters in each image, as described.', [
  ([('tipos de pessoa', 95), ('no grupo', 112), ('da família:', 112)],
   'family gathering on a veranda, everyone of all ages looking at their own phones, an old dog sleeping on the floor.'),
  ([('a tia do', 108), ('“bom dia” com', 86), ('flor e glitter.', 86)],
   'an aunt in her 60s in a floral dress, reading glasses on the tip of her nose, typing on her phone with one finger, smiling, a vase of plastic flowers beside her.'),
  ([('o tio que manda', 86), ('notícia sem', 96), ('conferir.', 122)],
   'an uncle in his 60s with a big belly and a football shirt lying in a hammock, pointing indignantly at his phone.'),
  ([('o primo que', 96), ('só aparece', 106), ('pra pedir pix.', 96)],
   'a young man cousin in a cap with a sheepish grin, scratching the back of his head while holding his phone.'),
  ([('e você, que lê tudo', 72), ('e não responde', 96), ('nada.', 150), _, ('marca o tio da notícia', 40)],
   'a young woman lying on the sofa reading her phone with a sly smile, a cat sleeping on her legs.'),
 ], "Todo grupo da família tem esse elenco fixo. E sempre tem alguém que lê tudo, ri sozinho e não responde nada.\n\n"
    "Qual desses é você? Conta aqui embaixo e marca a tia do bom dia. 😂\n\n"
    "#família #grupodafamília #humor #whatsapp #verdadesatemporais"),

 ('domingo', 'rb-010', '2026-11-08', '21:00', 'single image about Sunday night anxiety', 'one woman, about 30.', [
  ([('a ansiedade de', 86), ('domingo à noite', 100), ('não é preguiça.', 96), _, ('é o corpo lembrando', 62), ('de tudo o que você carrega.', 58)],
   'night, a woman sitting on the edge of her bed in a dim bedroom lit only by a bedside lamp, looking out of the window at the dark street, a backpack and a work badge on a chair; deep blue night tones.'),
 ], "Domingo à noite tem um peso que ninguém explica direito. Não é preguiça nem drama: é cansaço acumulado.\n\n"
    "Se hoje bateu, respira. Amanhã você resolve uma coisa de cada vez. 🤍\n\n"
    "#domingoànoite #ansiedade #saúdemental #reflexão #verdadesatemporais"),

 ('pequenas', 'rb-011', '2026-11-09', '12:00', 'small things that save a bad day; each image is an independent scene',
  'different people in each image, as described.', [
  ([('coisas pequenas', 100), ('que salvam', 112), ('um dia ruim:', 106)],
   'a cup of coffee steaming on a windowsill, rain outside, a small potted plant, cozy.'),
  ([('o ônibus', 122), ('chegar vazio.', 112)],
   'a tired man in a work uniform smiling with relief, sitting alone in an empty city bus, golden afternoon light through the windows.'),
  ([('alguém lembrar', 96), ('do seu nome.', 112)],
   'a small bakery counter, the baker handing bread to a young woman and greeting her warmly, she is surprised and touched.'),
  ([('banho quente', 112), ('e roupa limpa.', 100)],
   'a woman with a towel turban and soft pajamas, eyes closed, smelling a pile of clean folded clothes, light steam in the air.'),
  ([('e um áudio', 106), ('que começa com', 86), ('“lembrei de você”.', 96), _, ('manda esse áudio pra alguém hoje', 40)],
   'an older woman sitting on her porch listening to a voice message with the phone at her ear, smiling widely.'),
 ], "Nem todo dia ruim precisa de uma grande solução. Às vezes um ônibus vazio e alguém lembrando do seu nome já mudam tudo.\n\n"
    "Qual coisa pequena salva o seu dia? Conta aqui. E manda esse post pra quem anda precisando. 🤍\n\n"
    "#gratidão #coisaspequenas #autocuidado #reflexão #verdadesatemporais"),

 ('frescura', 'rb-012', '2026-11-09', '18:00', 'things that look like being dramatic but are just healthy limits; calm and firm',
  'different people in each image, as described.', [
  ([('não é', 122), ('frescura.', 160)],
   'a woman sitting alone on a park bench at dusk, hands clasped, serious and calm.'),
  ([('precisar de', 102), ('silêncio depois', 90), ('do trabalho.', 106)],
   'a man taking off his shoes at the door of his house, eyes closed, in a quiet dim living room.'),
  ([('não querer ir', 96), ('a todo', 112), ('aniversário.', 122)],
   'a woman in pajamas on the sofa with a cup of tea, a party invitation card on the coffee table, peaceful.'),
  ([('dizer que', 106), ('ficou chateado.', 100), _, ('é só você se respeitando.', 60), ('', 10), ('manda pra quem vive pedindo desculpa', 40)],
   'two friends sitting on the front steps of a house talking, one with a hand on the chest explaining honestly, the other listening attentively.'),
 ], "Tem coisa que a gente esconde por medo de parecer exagero. Mas cuidar do próprio limite não é frescura.\n\n"
    "Qual desses você já ouviu que era frescura? Conta aqui embaixo. 🤍\n\n"
    "#limites #autoestima #saúdemental #respeito #verdadesatemporais"),

 ('completa', 'rb-013', '2026-11-09', '21:00', 'interactive "complete the sentence" post about nostalgia',
  'Rosa, 35, light brown skin, long wavy black hair, mustard cardigan.', [
  ([('complete:', 122), _, ('“eu era mais', 96), ('feliz quando…”', 100)],
   'Rosa sitting at her grandmother\'s old kitchen table looking through a photo album of the 1990s, an enamel mug, a clay water filter and a tube TV in the background, nostalgic smile.'),
  ([('a gente lê', 92), ('todas as respostas.', 86), _, ('responde aqui embaixo', 50)],
   'a 1990s backyard memory: children playing with a garden hose under a clothesline full of sheets, a grandmother laughing on a plastic chair.'),
 ], "Completa a frase nos comentários: \"eu era mais feliz quando...\"\n\n"
    "A gente lê todas. E talvez a sua resposta seja o lembrete que alguém precisava. 🤍\n\n"
    "#completeafrase #nostalgia #reflexão #felicidade #verdadesatemporais"),

 ('planos', 'rb-014', '2026-11-10', '12:00', 'funny: New Year resolutions from January versus reality in November',
  'Rafa, 30, brown skin, short beard, green hoodie.', [
  ([('faltam 7 semanas', 86), ('pro ano acabar.', 96), _, ('e os planos de janeiro?', 60)],
   'Rafa looking worried at a wall calendar full of crossed-out days, holding a closed notebook, a few dry leaves on the floor.'),
  ([('janeiro:', 92), ('“vou na academia', 86), ('todo dia.”', 106), _, ('novembro: a esteira virou cabide.', 50)],
   'Rafa\'s bedroom, a treadmill completely covered with hanging clothes, Rafa shrugging with a sheepish smile.'),
  ([('janeiro:', 92), ('“vou ler', 106), ('um livro por mês.”', 86), _, ('novembro: página 23.', 52)],
   'Rafa asleep on the sofa with an open book lying on his face, a cat on the armrest.'),
  ([('mas você chegou', 92), ('até aqui.', 122), _, ('isso também conta.', 62), ('', 10), ('marca quem prometeu junto com você', 40)],
   'Rafa on a small balcony at sunset, relaxed, holding a cup, smiling peacefully.'),
 ], "Faltam poucas semanas pro ano acabar e a lista de janeiro ficou... do jeito que ficou. Tudo bem. Você atravessou o ano, e isso também conta.\n\n"
    "Qual promessa de janeiro ficou pelo caminho? Confessa aqui. 😅\n\n"
    "#fimdeano #metas #humor #2026 #verdadesatemporais"),

 ('tempo', 'rb-015', '2026-11-10', '18:00', 'two-slide turn: you are not late in life',
  'Clara, 27, light brown skin, long straight black hair in a low ponytail, mustard jacket, small backpack.', [
  ([('você não está', 96), ('atrasado.', 150)],
   'Clara walking alone on a red dirt road at sunrise, other people tiny and far ahead on the road.'),
  ([('o caminho', 112), ('é seu.', 140), _, ('e ele não é uma corrida.', 62), ('', 10), ('manda pra quem vive se comparando', 40)],
   'Clara sitting on a rock resting, looking at a beautiful green valley with wildflowers, smiling.'),
 ], "Tem gente que se forma aos 22, casa aos 25 e muda de vida aos 40. Não existe prazo certo pra nada que importa.\n\n"
    "Manda pra alguém que anda se comparando demais. 🤍\n\n"
    "#seutempo #comparação #ansiedade #reflexão #verdadesatemporais"),

 ('amor', 'rb-016', '2026-11-10', '21:00', 'real love is everyday, not like the movies',
  'Davi, 35, dark brown skin, shaved head, grey T-shirt; Marina, 33, brown skin, short wavy hair, red blouse.', [
  ([('amor de verdade', 98), ('não tem trilha', 92), ('sonora.', 132)],
   'Davi and Marina in a small kitchen at night washing and drying dishes side by side, laughing.'),
  ([('é guardar', 110), ('o último pedaço', 92), ('pro outro.', 116)],
   'Marina putting the last slice of pizza on a plate covered with a napkin into the fridge, smiling.'),
  ([('é ficar acordado', 88), ('até a pessoa', 98), ('chegar.', 140)],
   'night, Davi dozing on the sofa under a lamp, waiting, as Marina opens the front door and smiles at him.'),
  ([('é rir junto', 104), ('do boleto.', 126)],
   'Davi and Marina at the kitchen table looking at a pile of bills and laughing together, coffee mugs.'),
  ([('é escolher', 112), ('de novo', 122), ('todo dia.', 116), _, ('marca quem te escolhe todo dia', 40)],
   'Davi and Marina dancing slowly barefoot in the living room to an old radio, warm lamp light.'),
 ], "Amor de verdade é menos cena de filme e mais louça dividida, pedaço de pizza guardado e gente esperando acordado.\n\n"
    "Marca quem te escolhe todo dia. 🤍\n\n"
    "#amor #casal #relacionamento #amordeverdade #verdadesatemporais"),

 ('issoaquilo', 'rb-017', '2026-11-11', '12:00', 'interactive "this or that"; each image is a split composition with a painted vertical divider',
  'different people in each half, as described.', [
  ([('responde rápido,', 92), ('sem pensar:', 106), _, ('áudio ou texto?', 72)],
   'split composition with a painted vertical divider: left half a person happily recording a voice message, right half another person typing a long message with both thumbs, each in their own room.'),
  ([('chegar 1 hora', 96), ('antes ou', 102), ('5 minutos depois?', 86)],
   'split composition with a painted vertical divider: left half a woman waiting alone and very early at a bus stop with a coffee, right half a man running late with untied shoes and toast in his mouth.'),
  ([('feijão por cima', 92), ('ou do lado', 102), ('do arroz?', 116), _, ('responde nos comentários', 45)],
   'split composition with a painted vertical divider, two plates of Brazilian food seen from above on a flowered tablecloth: left plate with beans poured over the rice, right plate with beans beside the rice.'),
 ], "Sem pensar muito: áudio ou texto? Chegar cedo ou chegar atrasado? E o mais polêmico de todos: feijão por cima ou do lado?\n\n"
    "Responde as três nos comentários. 👇\n\n"
    "#issoouaquilo #enquete #humor #brasil #verdadesatemporais"),

 ('azul', 'rb-018', '2026-11-11', '18:00', 'Novembro Azul (men\'s health month): men also cry, fear and take care of themselves',
  'Antonio, 55, brown skin, grey beard, cap, light blue shirt; his son, 25, brown skin, short hair, white T-shirt.', [
  ([('homem também', 100), ('chora.', 162)],
   'dusk, Antonio sitting alone on the back of an old pickup truck, discreetly wiping a tear.'),
  ([('homem também', 100), ('tem medo.', 146)],
   'Antonio in a simple clinic waiting room, holding his cap with both hands, nervous.'),
  ([('homem também', 100), ('se cuida.', 146)],
   'Antonio in a doctor\'s office being attended by a friendly doctor, his son beside him with a hand on his shoulder.'),
  ([('novembro azul', 106), ('é sobre isso.', 112), _, ('cuidar não diminui ninguém.', 58), ('', 10), ('manda pro seu pai, tio ou amigo', 40)],
   'morning, Antonio and his son laughing together while fishing on a river bank, clear blue sky.'),
 ], "Muito homem cresceu ouvindo que não pode chorar, não pode ter medo e só vai ao médico quando não aguenta mais. Novembro Azul é um lembrete de que se cuidar é coragem.\n\n"
    "Manda pro seu pai, tio ou amigo e lembra ele de marcar aquele check-up. 💙\n\n"
    "#novembroazul #saúdedohomem #autocuidado #prevenção #verdadesatemporais"),

 ('some', 'rb-019', '2026-11-11', '21:00', 'single image about people who slowly disappear', 'one small distant figure.', [
  ([('nem toda', 106), ('despedida', 126), ('tem abraço.', 106), _, ('às vezes a pessoa', 62), ('só vai sumindo.', 62)],
   'night, a quiet street with a single streetlight, a small person walking away into the distance, a dog sitting on the sidewalk watching; deep blue night tones.'),
 ], "Tem gente que não vai embora de uma vez. Vai respondendo menos, aparecendo menos, até virar lembrança.\n\n"
    "Dói, mas também ensina: quem quer ficar, fica. 🤍\n\n"
    "#despedida #amizade #reflexão #sentimentos #verdadesatemporais"),

 ('avo', 'rb-020', '2026-11-12', '12:00', 'nostalgic things that only exist at grandma\'s house',
  'Grandma Lurdes, 80, dark brown skin, white hair in a bun, floral dress, beige cardigan; her adult grandchild, 30.', [
  ([('coisas que só', 92), ('existem na casa', 96), ('da vó:', 140)],
   'grandmother\'s living room with crochet doilies, an old TV with a cloth on top, plastic flowers and a wall clock, Grandma Lurdes smiling in her armchair.'),
  ([('o pote de sorvete', 86), ('que é feijão.', 112)],
   'Grandma Lurdes opening the freezer and showing an ice cream tub full of frozen beans, her grandchild disappointed behind her.'),
  ([('o “come mais”', 100), ('depois do', 106), ('terceiro prato.', 100)],
   'Grandma Lurdes serving another big spoonful of food onto the plate of her full grandchild, who protests with both hands.'),
  ([('o paninho', 106), ('de crochê', 112), ('em cima de tudo.', 90)],
   'a room where everything has a crochet doily on top: the TV, the phone, the gas cylinder, the fridge, and a cat sleeping on one.'),
  ([('e um abraço', 104), ('que cura', 122), ('qualquer coisa.', 100), _, ('marca seu primo de infância', 40)],
   'Grandma Lurdes hugging her adult grandchild at the front door, eyes closed, warm light.'),
 ], "Pote de sorvete com feijão, paninho de crochê em cima da TV e aquele \"come mais\" que não aceita não como resposta. Casa de vó é patrimônio.\n\n"
    "O que mais tinha na casa da sua vó? Conta aqui. 🤍\n\n"
    "#casadevó #vó #nostalgia #infância #verdadesatemporais"),

 ('trabalho', 'rb-021', '2026-11-12', '18:00', 'funny things every worker understands',
  'Bruno, 31, brown skin, curly black hair, light blue work shirt with a badge lanyard.', [
  ([('coisas que', 106), ('todo trabalhador', 92), ('entende:', 126)],
   'Bruno in a crowded city bus holding the bar with one hand and a lunchbox in the other, sleepy.'),
  ([('o “rapidinho”', 100), ('que dura', 106), ('duas horas.', 116)],
   'Bruno in a meeting room with exhausted coworkers, many empty coffee cups on the table, late afternoon light.'),
  ([('o ânimo', 112), ('de sexta', 116), ('às 17h59.', 116)],
   'Bruno already standing with his backpack on next to his desk, staring at the wall clock, ready to run.'),
  ([('a marmita', 112), ('que vazou', 116), ('na mochila.', 112)],
   'Bruno looking in horror into his open backpack full of spilled sauce, coworkers laughing behind him.'),
  ([('e o salário', 104), ('que entra e sai', 90), ('no mesmo dia.', 100), _, ('marca seu colega de trabalho', 40)],
   'Bruno sitting on his bed looking at his phone while paper bills fly out of the open window like birds, comic.'),
 ], "Reunião rapidinha que vira duas horas, marmita vazada e o salário que entra e sai no mesmo dia. Quem trabalha sabe.\n\n"
    "Marca aquele colega que vive isso com você. 😂\n\n"
    "#trabalho #clt #humor #vidaadulta #verdadesatemporais"),

 ('fase', 'rb-022', '2026-11-12', '21:00', 'a short letter for someone going through a hard phase',
  'a young man, 26, dark brown skin, short locs, white T-shirt.', [
  ([('pra você que está', 86), ('numa fase', 116), ('difícil:', 140)],
   'night, the young man sitting on the floor of a small room leaning against the bed, knees up, a window with the moon; deep blue night tones.'),
  ([('fase', 140), ('não é', 122), ('destino.', 132)],
   'dawn, the same young man opening the window curtains, the first warm light hitting his face.'),
  ([('ela passa.', 116), ('e você vai lembrar', 80), ('dela de longe.', 90), _, ('manda pra quem precisa ler hoje', 40)],
   'bright morning, the same young man walking down a street holding a small potted plant, light steps.'),
 ], "Se você está numa fase difícil, lembra: fase é fase. Ela tem começo, meio e fim, mesmo quando o meio parece não acabar.\n\n"
    "Manda pra alguém que precisa ler isso hoje. 🤍\n\n"
    "#fasedifícil #esperança #saúdemental #reflexão #verdadesatemporais"),

 ('sexta13', 'rb-023', '2026-11-13', '12:00', 'funny Friday the 13th: real bad luck is everyday stuff',
  'different people in each image, as described.', [
  ([('sexta-feira 13?', 106), ('azar mesmo', 112), ('é…', 150)],
   'a bored black cat sitting calmly on a sunny windowsill, a ladder leaning nearby and a cracked hand mirror on a table, humorous.'),
  ([('o carregador', 106), ('não alcançar', 100), ('a cama.', 132)],
   'a woman stretched across her bed reaching for her phone on a very short charger cable plugged into a faraway socket.'),
  ([('o “precisamos', 100), ('conversar”', 122), ('sem contexto.', 106)],
   'a man frozen in fear looking at his phone, a drop of sweat on his forehead, his coffee cup tipping over.'),
  ([('acabar o gás', 100), ('no meio', 116), ('do feijão.', 116), _, ('marca quem não acredita em azar', 40)],
   'a woman with hands on her head staring at a pressure cooker on a dead stove, the gas cylinder beside it, a cat watching.'),
 ], "Gato preto não faz mal a ninguém. Azar mesmo é carregador curto, gás acabando no feijão e mensagem de \"precisamos conversar\" sem contexto.\n\n"
    "Qual o maior azar do seu dia a dia? Conta aqui. 😂\n\n"
    "#sextafeira13 #azar #humor #brasil #verdadesatemporais"),

 ('gente', 'rb-024', '2026-11-13', '18:00', 'what good people are like; each image is an independent scene',
  'different people in each image, as described.', [
  ([('gente boa', 126), ('é aquela que…', 106)],
   'a sunny neighborhood street, a woman watering plants waves at a neighbor, kids playing.'),
  ([('pergunta', 122), ('“e você?”', 126), ('de volta.', 116)],
   'two friends at a small café table, one leaning forward listening attentively while the other talks.'),
  ([('lembra do que', 98), ('você contou', 108), ('semana passada.', 98)],
   'a man arriving at a friend\'s door with a small gift bag, the friend surprised and moved.'),
  ([('não te faz', 108), ('sentir pesado', 100), ('por pedir ajuda.', 96)],
   'a woman helping her neighbor carry heavy grocery bags up the stairs, both laughing.'),
  ([('fica perto', 112), ('dessas.', 140), _, ('marca uma pessoa assim', 42)],
   'a group of friends laughing at a backyard barbecue table under string lights at sunset.'),
 ], "Gente boa não é a que sabe tudo nem a que tem a melhor resposta. É a que pergunta \"e você?\", lembra do que você contou e não te faz sentir pesado.\n\n"
    "Marca alguém assim. Essa pessoa merece saber. 🤍\n\n"
    "#amizade #gentedobem #gratidão #reflexão #verdadesatemporais"),

 ('dinheiro', 'rb-025', '2026-11-13', '21:00', 'funny phrases of someone whose money ran out before the end of the month',
  'Tati, 28, brown skin, long curly hair, oversized purple T-shirt.', [
  ([('frases de quem', 96), ('o dinheiro acabou', 86), ('antes do mês:', 100)],
   'Tati sitting on her bed opening an empty wallet, a little moth flying out, comic.'),
  ([('“hoje eu', 116), ('não tô a fim', 106), ('de sair.”', 122)],
   'Tati in pajamas on the sofa declining a call from friends, a steaming bowl of instant noodles beside her.'),
  ([('“já jantei.”', 140), _, ('(comeu bolacha', 62), ('com café.)', 62)],
   'night, Tati standing in the kitchen dipping crackers into a cup of coffee, satisfied.'),
  ([('“mês que vem', 112), ('eu me organizo.”', 100), _, ('marca quem fala isso todo mês', 40)],
   'morning, Tati writing a budget in a notebook with determination, a piggy bank beside her.'),
 ], "\"Hoje eu não tô a fim de sair\" significa muita coisa. Principalmente que o dinheiro foi embora antes do dia 30.\n\n"
    "Qual dessas você mais fala? Confessa aqui. 😅\n\n"
    "#dinheiro #fimdomês #humor #vidaadulta #verdadesatemporais"),

 ('permissao', 'rb-026', '2026-11-14', '12:00', 'Saturday reminder: you are allowed to rest',
  'Lia, 40, brown skin, curly hair with grey streaks, loose white linen dress.', [
  ([('lembrete de', 100), ('sábado:', 140), _, ('você tem permissão', 70), ('para…', 92)],
   'Lia stretching her arms by an open window in a sunny morning bedroom.'),
  ([('não fazer', 116), ('nada hoje.', 126)],
   'Lia lying on a rug on the living room floor in a patch of sunlight, arms open, a cat beside her.'),
  ([('desmarcar', 122), ('sem inventar', 106), ('desculpa.', 126)],
   'Lia on a veranda with a glass of iced tea, texting on her phone with a relieved smile.'),
  ([('comer o doce', 106), ('sem culpa.', 126)],
   'Lia eating a slice of Brazilian pudding (pudim) at the kitchen table, eyes closed with pleasure.'),
  ([('descansar', 122), ('também é', 116), ('cuidar.', 140), _, ('manda pra quem não sabe parar', 40)],
   'Lia napping in a hammock in a backyard full of plants, soft afternoon light.'),
 ], "Lembrete de sábado: você não precisa merecer o descanso. Parar também é cuidar de você.\n\n"
    "Manda pra aquela pessoa que não sabe parar nem no fim de semana. 🤍\n\n"
    "#descanso #autocuidado #sábado #saúdemental #verdadesatemporais"),

 ('casal', 'rb-027', '2026-11-14', '18:00', 'funny: a couple at the beginning versus five years later',
  'Gui, 32, light brown skin, short black hair, glasses; Bel, 31, dark brown skin, long braids.', [
  ([('casal no começo', 96), ('vs. casal', 112), ('5 anos depois:', 100)],
   'split composition with a painted vertical divider: left half Gui and Bel dressed up at a candlelit dinner, right half Gui and Bel in pajamas eating on the sofa under a blanket.'),
  ([('antes:', 112), ('“o que você', 96), ('quer jantar?”', 100), _, ('agora: “descongela o frango.”', 50)],
   'Bel calling from the sofa while Gui stands at the open freezer holding a frozen chicken, amused.'),
  ([('antes:', 112), ('mensagem de', 100), ('bom dia.', 126), _, ('agora: “compra pão.”', 52)],
   'Gui at a bakery counter reading his phone and holding a paper bag of bread rolls, smiling.'),
  ([('e continua sendo', 92), ('a melhor parte', 96), ('do dia.', 122), _, ('marca seu “compra pão”', 40)],
   'Gui and Bel sharing coffee and bread at the breakfast table, laughing, morning light.'),
 ], "No começo era jantar à luz de vela. Depois de uns anos é \"descongela o frango\" e \"compra pão\". E continua sendo a melhor parte do dia.\n\n"
    "Marca o seu \"compra pão\". 😂🤍\n\n"
    "#casal #relacionamento #humor #amor #verdadesatemporais"),

 ('ano', 'rb-028', '2026-11-14', '21:00', 'single image: the year is not over yet', 'one woman, about 35.', [
  ([('o ano', 122), ('ainda não acabou.', 96), _, ('dá tempo de fazer', 66), ('as pazes com você.', 66)],
   'night, a woman on a small balcony looking at a starry sky over a small town, a loose calendar page flying away in the wind; deep blue night tones.'),
 ], "Ainda faltam algumas semanas. Não pra correr atrás de tudo que ficou pra trás, mas pra olhar com mais carinho pra quem chegou até aqui.\n\n"
    "Dá tempo de fazer as pazes com você. 🤍\n\n"
    "#fimdeano #recomeço #autoamor #reflexão #verdadesatemporais"),
]
P = {p[0]: p for p in POSTS}


def email(chave):
    k, num, data, hora, ideia, elenco, slides, leg = P[chave]
    c = CAT[CATEGORIA[k]]
    pre = f'{PREFIXO}-{k}'
    n = max(len(slides), 2)  # a automação falha com pedido de uma imagem só; o extra fica de reserva
    cenas = [cena for _t, cena in slides]
    if len(cenas) == 1:
        cenas.append(cenas[0] + ' Alternative composition, different angle.')
    linhas = [f'Generate {n} separate illustrations, one image per item below. '
              'Do not ask me anything. Save each with the exact file name given.', '',
              f'THE IDEA OF THIS POST: {ideia}.',
              f'CHARACTERS: {elenco} Keep the same look in every image where they appear.', '',
              f'STYLE (same for all): {ESTILO}',
              f'COLOR PALETTE (use only this palette, it defines this series): {c["paleta"]}.',
              f'WORLD: {c["mundo"]}.', f'TYPE OF CHARACTERS: {c["elenco"]}.', f'TYPICAL OBJECTS: {c["objetos"]}.', '']
    for i, cena in enumerate(cenas, 1):
        linhas.append(f'{pre}{i:02d}: {cena}')
    return '\n'.join(linhas)


def imagem(chave, n):
    for cand in (f'{PREFIXO}-{chave}{n:02d}b.png', f'{PREFIXO}-{chave}{n:02d}.png',
                 f'va-{chave}{n:02d}c.png', f'va-{chave}{n:02d}b.png', f'va-{chave}{n:02d}.png'):
        p = os.path.join(FOTOS, cand)
        if os.path.exists(p):
            return p


LIMITE = 455  # o título não passa do terço de cima


def escrever_titulo(img, linhas, seed, tinta=TINTA):
    """Escreve o letreiro e, se passar do LIMITE, reduz tudo proporcionalmente e tenta de novo."""
    fator = 1.0
    for _t in range(6):
        esc = [(t, round(a * fator)) for t, a in linhas]
        out, y = _titulo(img, esc, seed, tinta)
        if y <= LIMITE:
            return out, y
        fator *= (LIMITE - 70) / (y - 70) * 0.98
    return out, y


def _titulo(img, linhas, seed, tinta=TINTA):
    escura = sum(tinta) < 300
    cor = CREME if luminancia(img, (100, 60, W - 100, 400)) < 110 else (tinta if escura else TINTA)
    y, grupo = 70, []
    for txt, alt in linhas + [('', 0)]:
        if txt:
            grupo.append((txt, alt)); continue
        if grupo:
            img, y = letreiro(img, grupo, 90, y, W - 180, cor=cor, alinhamento='centro', espaco=8, seed=seed + int(y))
            grupo = []
        y += alt
    return img, y


def gerar(chave):
    k, num, data, hora, ideia, elenco, slides, leg = P[chave]
    saida = os.path.join(AQUI, 'saida', 'semana', chave)
    os.makedirs(saida, exist_ok=True)
    feitos = 0
    for i, (linhas, cena) in enumerate(slides, 1):
        p = imagem(chave, i)
        if not p:
            print('falta', f'va-{chave}{i:02d}'); continue
        img = grao(preencher(Image.open(p)), 3, seed=i)
        img, _y = escrever_titulo(img, linhas, i * 7, CAT[CATEGORIA[chave]]['tinta'])
        assinatura(img).save(os.path.join(saida, f'{i:02d}.jpg'), quality=93)
        feitos += 1
    print(chave, feitos, 'de', len(slides))
    return feitos == len(slides)


def fila(chave):
    k, num, data, hora, ideia, elenco, slides, leg = P[chave]
    origem = os.path.join(AQUI, 'saida', 'semana', chave)
    pasta = f'{num}-{chave}'
    destino = os.path.join(RAIZ, 'posts', pasta)
    os.makedirs(destino, exist_ok=True)
    imgs = []
    for f in sorted(os.listdir(origem)):
        if f.endswith('.jpg'):
            shutil.copy(os.path.join(origem, f), os.path.join(destino, f))
            imgs.append(f'posts/{pasta}/{f}')
    assert len(imgs) == len(slides), f'{chave}: {len(imgs)} de {len(slides)}'
    caminho = os.path.join(RAIZ, 'fila.json')
    itens = [p for p in json.load(open(caminho)) if p.get('chave') != num]
    itens.append({'numero': num, 'chave': num, 'data': data, 'hora': hora,
                  'destinos': ['instagram', 'facebook'], 'imagens': imgs, 'legenda': leg})
    json.dump(itens, open(caminho, 'w'), ensure_ascii=False, indent=1)
    print('na fila:', num, data, hora)


def teste():
    base = Image.new('RGB', (W, H), (240, 200, 170))
    thumbs = []
    for k, *_r in POSTS:
        for i, (linhas, cena) in enumerate(P[k][6], 1):
            img, y = escrever_titulo(base.copy(), linhas, i)
            d = ImageDraw.Draw(img)
            d.line((0, 450, W, 450), fill=(255, 0, 0), width=5)
            d.text((20, H - 60), f'{k} {i}', fill=(0, 0, 0))
            thumbs.append(img.crop((0, 0, W, 600)).resize((270, 150)))
    cols = 8
    S = Image.new('RGB', (270 * cols, 150 * ((len(thumbs) + cols - 1) // cols)), 'white')
    for n, t in enumerate(thumbs):
        S.paste(t, ((n % cols) * 270, (n // cols) * 150))
    S.save('/home/claude/teste-semana.jpg', quality=85)


if __name__ == '__main__':
    acao, *chaves = sys.argv[1:]
    if acao == 'email':
        print(email(chaves[0]))
    elif acao == 'gerar':
        for c in chaves: gerar(c)
    elif acao == 'fila':
        for c in chaves: fila(c)
    elif acao == 'teste':
        teste()
