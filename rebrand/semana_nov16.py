"""Quinzena de 16 a 30/11/2026: 42 posts (12h, 18h, 21h), temas mais profundos (pedido do Levy em 16/11/2026).
Mesmo visual do rebrand (guache, categorias com paleta própria). Imagens novas: vc-<chave>NN.png.
Uso:
  python3 semana_nov16.py emails                 grava os pedidos ao Gemini em saida/quinzena/emails.json (grupos de até 13 imagens)
  python3 semana_nov16.py gerar <chave...|todos> monta os slides em saida/quinzena/<chave>/
  python3 semana_nov16.py fila <chave...|todos>  copia para posts/ e põe na fila.json
  python3 semana_nov16.py teste                  prévia de encaixe dos textos (sem imagens)"""
import json, os, shutil, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import *
import semana_nov08 as base
from semana_nov08 import escrever_titulo, ESTILO

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, '..')
FOTOS = os.path.join(AQUI, 'fotos', 'ilustrada')
SAIDA = os.path.join(AQUI, 'saida', 'quinzena')
PREFIXO = 'vc'
_ = ('', 12)

CAT = dict(base.CAT)
CAT.update({
 'finitude': dict(nome='Tempo e finitude', tinta=(70, 38, 20),
   paleta='golden hour colors: honey amber, warm terracotta, soft olive green, peach and long violet shadows, late afternoon sunlight',
   mundo='simple Brazilian homes, porches, kitchens and quiet streets in the late afternoon light',
   elenco='aging parents and grandparents with their adult children, tender and unhurried',
   objetos='coffee cups, porch chairs, old photographs, reading glasses, slippers, plants in tin cans'),
 'luto': dict(nome='Saudade e perdas', tinta=(52, 40, 74),
   paleta='soft lilac, dusty lavender, grey blue and pale dawn pink, gentle and quiet',
   mundo='quiet rooms at early morning, gardens, windows with sheer curtains, empty chairs',
   elenco='one or two contemplative people, calm faces, simple clothes',
   objetos='an empty chair, a cardigan on a hook, letters, flowers, a cup left on the table'),
 'raizes': dict(nome='Raízes', tinta=(58, 30, 16),
   paleta='rich earthy tones: terracotta, ochre, deep forest green, warm brown and sunlit gold',
   mundo='Brazilian countryside and city outskirts: backyards, fields, simple houses, community gatherings',
   elenco='Black Brazilian families across generations, dignified and warm',
   objetos='hoes, notebooks, graduation gowns, patterned fabrics, plants, old photographs'),
})

# chave, número, data, hora, categoria, ideia, elenco, slides [(linhas, cena)], legenda
POSTS = [
 # ---------------- segunda 16/11
 ('peso', 'rb-029', '2026-11-30', '18:00', 'acolhimento', 'invisible weights people carry every day; each image an independent person',
  'different people in each image, as described.', [
  ([('o que a gente', 100), ('carrega e', 112), ('ninguém vê:', 112)],
   'a woman walking home at dusk on a quiet street carrying only a small handbag, but her long shadow on the wall behind her carries a huge heavy sack.'),
  ([('a conta que', 106), ('não fecha.', 122)],
   'a man sitting at a kitchen table at night with a few paper bills spread out and a small lamp, head resting on one hand, a sleeping child visible through a doorway.'),
  ([('a saudade', 112), ('de quem', 122), ('não volta.', 122)],
   'a woman sitting on the edge of a bed holding a folded old shirt against her chest, eyes closed, a window with night sky.'),
  ([('o medo de não', 96), ('dar conta.', 122)],
   'a young nurse sitting alone on the back steps of a building at night, still in her uniform, staring at her hands.'),
  ([('por isso,', 112), ('pega leve.', 122), _, ('todo mundo carrega alguma coisa.', 48), ('', 10), ('manda pra quem anda carregando muito', 38)],
   'two strangers at a night bus stop, one offering the other a seat on the bench, warm lamp light, the rest of the street quiet and blue.'),
 ], "Todo mundo que passa por você hoje está carregando alguma coisa que você não vê. Uma conta, uma saudade, um medo.\n\n"
    "Por isso, pega leve. Com os outros e com você.\n\n"
    "Manda pra quem anda carregando muito. 🤍\n\n"
    "#saúdemental #empatia #reflexão #acolhimento #verdadesatemporais"),

 ('perguntar', 'rb-030', '2026-11-30', '21:00', 'acolhimento', 'single image: the strongest person in the house also needs someone to ask how they are',
  'one woman around 45.', [
  ([('a pessoa mais', 96), ('forte da casa', 100), ('também precisa', 92), ('ouvir:', 112), ('“e você, tá bem?”', 92)],
   'night, a woman around 45 sitting alone at the kitchen table after everyone went to bed, a cup of tea in her hands, dishes done, a soft lamp, the rest of the house dark and blue.'),
 ], "A pessoa que resolve tudo, que segura a casa, que nunca reclama. Ela também cansa.\n\n"
    "Hoje, pergunta pra ela: e você, tá bem? E espera a resposta de verdade.\n\n"
    "Marca aqui a pessoa mais forte que você conhece. 🤍\n\n"
    "#família #mãe #cuidado #acolhimento #verdadesatemporais"),

 # ---------------- terça 17/11
 ('pais', 'rb-031', '2026-11-17', '12:00', 'finitude', 'the day you notice your parents got old; tender, not sad',
  'Dona Cida, 68, brown skin, short grey curly hair, glasses on a cord, floral blouse; Seu Zé, 71, light brown skin, white mustache, checkered shirt; their son Rafa, 38, dark beard.', [
  ([('um dia você percebe', 72), ('que seus pais', 92), ('envelheceram.', 92)],
   'late afternoon, Rafa arriving at the gate of his parents\' simple house, Dona Cida and Seu Zé waiting on the porch, both noticeably older and slower, golden light.'),
  ([('a mão que treme', 92), ('um pouco', 112), ('ao servir o café.', 92)],
   'close view of Dona Cida pouring coffee from an old thermos into a small glass cup, her hand slightly unsteady, Rafa watching with tenderness at the table.'),
  ([('o “me ajuda', 100), ('com o celular”', 96), ('que virou rotina.', 92)],
   'Seu Zé on the sofa holding a phone far from his face, squinting, Rafa sitting next to him leaning in to help, both smiling.'),
  ([('liga hoje.', 122), ('não precisa', 106), ('de motivo.', 112), _, ('manda pra quem ainda tem os pais por perto', 38)],
   'Rafa and his parents sitting together on the porch bench at sunset, his arm around his mother, his father laughing, long warm shadows.'),
 ], "Um dia você chega pra visitar e percebe: eles envelheceram. A mão treme um pouco, o passo ficou mais lento, o celular virou um desafio.\n\n"
    "Não precisa de data especial nem de motivo. Liga hoje.\n\n"
    "Manda pra quem ainda tem os pais por perto. 🤍\n\n"
    "#pais #família #tempo #amor #verdadesatemporais"),

 ('luto-vivo', 'rb-032', '2026-11-17', '18:00', 'luto', 'losses that nobody calls grief: a friendship that ended, a former self, a place that was home',
  'different people in each image, as described.', [
  ([('nem todo luto', 100), ('tem velório.', 112)],
   'a young woman standing at a window at dawn holding a cup, looking at an empty street, sheer curtains moving softly.'),
  ([('a amizade que', 100), ('acabou', 122), ('sem briga.', 122)],
   'two empty chairs facing each other at a small café table, two cups left behind, morning light, a single flower in a glass.'),
  ([('a casa', 122), ('que já não', 106), ('é sua.', 132)],
   'a man standing on the sidewalk in front of a small house with a new color and a new gate, looking at it quietly, holding his car keys.'),
  ([('a versão de você', 92), ('que ficou', 112), ('pra trás.', 122)],
   'a woman looking at an old photograph of her younger self in her hand, sitting on the floor of a calm bedroom, gentle smile with watery eyes.'),
  ([('também é perda.', 96), ('também', 122), ('merece tempo.', 106), _, ('manda pra quem está vivendo um luto calado', 38)],
   'a woman sitting on a garden bench at early morning, a cardigan around her shoulders, a friend arriving and sitting beside her with two cups of coffee.'),
 ], "Tem perda que ninguém chama de luto. A amizade que acabou sem briga, a casa que ficou pra trás, a pessoa que você era antes de tudo mudar.\n\n"
    "Também dói. Também merece tempo. Você não precisa se explicar por sentir.\n\n"
    "Manda pra quem está vivendo um luto calado. 🤍\n\n"
    "#luto #saudade #saúdemental #acolhimento #verdadesatemporais"),

 ('descansar', 'rb-033', '2026-11-17', '21:00', 'acolhimento', 'single image: resting is not giving up',
  'one man around 35.', [
  ([('descansar não', 100), ('é desistir.', 112), _, ('é lembrar que você', 64), ('também é gente.', 64)],
   'night, a man around 35 lying on a hammock on a small balcony, eyes closed, shoes off, a work backpack dropped on the floor, a big moon over the rooftops, deep blue tones.'),
 ], "Você não precisa estar destruído pra ter direito de parar. Descansar não é desistir de nada.\n\n"
    "Hoje, desliga um pouco. O mundo continua amanhã e você vai estar mais inteiro pra ele.\n\n"
    "Salva pra lembrar quando a culpa aparecer. 🤍\n\n"
    "#descanso #autocuidado #saúdemental #reflexão #verdadesatemporais"),

 # ---------------- quarta 18/11
 ('mesa', 'rb-034', '2026-11-18', '12:00', 'nostalgia', 'the Sunday table at grandma\'s house; one day the table stays and people are missing',
  'Vó Lurdes, 78, dark brown skin, white hair in a bun, apron; a big family of all ages.', [
  ([('a mesa de', 112), ('domingo', 132), ('na casa da vó.', 100)],
   '1990s Brazilian kitchen, a long table full of food, a big family squeezed around it, Vó Lurdes bringing a steaming pot, children under the table.'),
  ([('sempre cabia', 106), ('mais um.', 132)],
   'Vó Lurdes pulling an extra plastic chair to the crowded table for a neighbor arriving at the door, everyone shifting to make room.'),
  ([('a comida que', 100), ('ninguém sabe', 106), ('fazer igual.', 112)],
   'close view of the table: a pot of beans, rice, farofa in an enamel bowl, a pudding, many hands reaching for food.'),
  ([('um dia a mesa', 96), ('fica.', 140), ('falta gente.', 112), _, ('aproveita enquanto todo mundo cabe na mesa', 38)],
   'the same kitchen years later, quiet afternoon light, the long table with only three people sitting, one empty chair with an apron hanging on it.'),
 ], "Na casa da vó sempre cabia mais um. A comida ninguém sabe fazer igual, e o barulho era a melhor parte do domingo.\n\n"
    "Um dia a mesa continua lá, mas falta gente. Aproveita enquanto todo mundo cabe.\n\n"
    "Marca quem sentava com você nessa mesa. 🤍\n\n"
    "#família #vó #nostalgia #domingo #verdadesatemporais"),

 ('homem-sozinho', 'rb-035', '2026-11-18', '18:00', 'causa', 'men\'s loneliness and silence (Novembro Azul, mental health)',
  'Beto, 40, brown skin, short black hair, beard, blue work shirt; his friend Dudu, 42, light skin, cap.', [
  ([('homem também', 100), ('se sente', 112), ('sozinho.', 132)],
   'evening, Beto sitting alone on the bed of an old pickup truck parked by a riverbank, looking at the water, blue tones.'),
  ([('ele diz que', 106), ('tá tranquilo.', 112)],
   'Beto at a family barbecue giving a thumbs up and a forced smile while everyone talks around him.'),
  ([('resolve tudo', 106), ('calado.', 132)],
   'Beto fixing a sink under a kitchen counter late at night, alone, the house dark around him.'),
  ([('pergunta', 122), ('duas vezes:', 112), ('“e aí, como', 100), ('você tá', 112), ('de verdade?”', 106)],
   'Beto and Dudu sitting together on the riverbank with fishing rods, Dudu with a hand on Beto\'s shoulder, Beto finally talking.'),
  ([('às vezes', 112), ('é só isso', 112), ('que ele precisa.', 96), _, ('manda pro amigo que nunca reclama', 40)],
   'Beto and Dudu laughing together on the pickup truck at dusk, the river shining blue.'),
 ], "Muito homem cresceu aprendendo a resolver tudo calado e a dizer que está tranquilo quando não está.\n\n"
    "Pergunta duas vezes. Na segunda, a resposta costuma ser verdadeira. Novembro Azul também é sobre isso.\n\n"
    "Manda pro amigo que nunca reclama. 💙\n\n"
    "#novembroazul #saúdemental #saúdedohomem #amizade #verdadesatemporais"),

 ('bastidores', 'rb-036', '2026-11-18', '21:00', 'acolhimento', 'single image: nobody posts the part where they almost gave up',
  'one young woman around 25.', [
  ([('ninguém posta', 100), ('a parte em que', 96), ('quase desistiu.', 100), _, ('não se compara', 66), ('com o palco dos outros.', 62)],
   'night, a young woman sitting on her bedroom floor with her back against the bed, phone glowing face down on the floor beside her, looking up at the window with the moon, deep blue tones.'),
 ], "No feed todo mundo chega. Ninguém mostra as noites em que quase desistiu.\n\n"
    "Você está comparando os seus bastidores com o palco dos outros. Não é justo com você.\n\n"
    "Salva pra ler no dia em que bater a comparação. 🤍\n\n"
    "#comparação #saúdemental #autoestima #reflexão #verdadesatemporais"),

 # ---------------- quinta 19/11
 ('perdao', 'rb-037', '2026-11-19', '12:00', 'validacao', 'forgiving yourself for what you did when you did not know better',
  'Lia, 34, brown skin, curly hair tied up, linen shirt, appears in every image.', [
  ([('perdoa quem', 106), ('você foi.', 132)],
   'morning, Lia sitting on a veranda full of plants holding a cup of tea, looking calmly at the garden.'),
  ([('você fez o que', 96), ('deu com o que', 96), ('sabia na época.', 96)],
   'Lia looking through an old notebook at a wooden table by an open window, a gentle half smile.'),
  ([('a pessoa', 122), ('de antes tinha', 100), ('menos', 132), ('ferramentas.', 112)],
   'Lia kneeling in a small garden planting a seedling with her hands, a watering can beside her.'),
  ([('não precisa', 106), ('se defender.', 106), ('só se entender.', 96), _, ('seja gentil com quem você foi', 40)],
   'Lia lying in a hammock with a book on her chest, eyes closed, sun through the leaves, peaceful.'),
 ], "Tem coisa do passado que ainda pesa. Mas a pessoa que você era fez o que deu com o que sabia naquela época.\n\n"
    "Você não precisa se defender pra sempre. Só se entender.\n\n"
    "Qual versão sua precisa desse perdão? 🤍\n\n"
    "#perdão #autoperdão #amadurecimento #saúdemental #verdadesatemporais"),

 ('deixar-ir', 'rb-038', '2026-11-19', '18:00', 'afeto', 'not every love is meant to stay; letting go with gratitude',
  'Nina, 29, light brown skin, short wavy hair, red cardigan.', [
  ([('nem todo amor', 100), ('é pra ficar.', 112)],
   'Nina at a train station platform at sunset, holding a ticket, looking at the tracks, coral sky.'),
  ([('alguns vêm', 106), ('pra ensinar.', 112)],
   'memory scene: Nina and a young man laughing on neighborhood stairs, sharing a bag of popcorn, string lights.'),
  ([('e vão embora', 100), ('levando', 122), ('um pedaço.', 122)],
   'Nina alone in a small café, an empty chair in front of her, two cups, she smiles softly at the window.'),
  ([('tudo bem.', 132), ('o que foi bom', 100), ('continua sendo.', 96), _, ('manda pra quem está aprendendo a soltar', 38)],
   'Nina walking alone down a street lined with pink trees, wind blowing petals, her face calm and light.'),
 ], "Nem todo amor é pra ficar. Alguns vêm pra ensinar alguma coisa e vão embora levando um pedaço.\n\n"
    "Tudo bem. O que foi bom não deixa de ter sido bom só porque acabou.\n\n"
    "Manda pra quem está aprendendo a soltar. 🤍\n\n"
    "#amor #desapego #recomeço #reflexão #verdadesatemporais"),

 ('insonia', 'rb-039', '2026-11-19', '21:00', 'acolhimento', 'single image: the mind gets loud exactly when the room gets quiet',
  'one person around 30.', [
  ([('a cabeça faz', 100), ('barulho justo', 100), ('quando o quarto', 96), ('fica em silêncio.', 92)],
   'night, a young man lying awake in bed staring at the ceiling, the ceiling filled with soft painted swirls like thoughts, a phone glowing on the nightstand, deep blue and violet tones.'),
 ], "Durante o dia dá pra se distrair. É de noite, no silêncio, que tudo resolve aparecer.\n\n"
    "Não precisa resolver a vida hoje. Respira, larga o celular e deixa pra pensar amanhã, com mais luz.\n\n"
    "Quem mais está acordado agora? 🌙\n\n"
    "#insônia #ansiedade #saúdemental #noite #verdadesatemporais"),

 # ---------------- sexta 20/11 (Dia da Consciência Negra)
 ('raizes', 'rb-040', '2026-11-20', '12:00', 'raizes', 'you are the dream of those who came before you; honoring grandparents and ancestors',
  'a Black Brazilian family: the grandmother Dona Benedita, 80, white hair in a headscarf; the grandfather Seu Antônio, 83, straw hat; their granddaughter Ana, 23, braids.', [
  ([('você é o', 112), ('sonho de quem', 100), ('veio antes.', 112)],
   'Ana in a graduation gown standing in a sunny backyard, her grandparents beside her looking at her with pride, a mango tree behind.'),
  ([('a vó que', 112), ('não pôde', 112), ('estudar.', 132)],
   'memory scene: young Benedita washing clothes by a river with other women, looking at a group of children walking to school.'),
  ([('o vô que', 112), ('trabalhou de', 106), ('sol a sol.', 122)],
   'memory scene: young Antônio working in a green field with a hoe under a strong golden sun.'),
  ([('você é a', 112), ('continuação', 112), ('do que eles', 106), ('plantaram.', 122), _, ('honra quem veio antes de você', 40)],
   'Ana sitting between her grandparents on a wooden bench, holding both their hands, sunset light, plants around them.'),
 ], "Antes de você, teve gente que não pôde estudar, que trabalhou de sol a sol e que sonhou com um futuro que talvez nem fosse ver.\n\n"
    "Você é a continuação do que eles plantaram. Neste 20 de novembro, honra quem veio antes.\n\n"
    "Conta aqui o nome de alguém da sua família que abriu caminho pra você. 🤎\n\n"
    "#consciêncianegra #ancestralidade #família #raízes #verdadesatemporais"),

 ('ultima-vez', 'rb-041', '2026-11-20', '18:00', 'finitude', 'there was a last time for many things and we did not know it was the last',
  'different moments of one family, as described.', [
  ([('teve uma', 112), ('última vez', 112), ('e você não', 106), ('sabia.', 140)],
   'late afternoon, a quiet empty street with a kite caught on an electric wire, golden light, long shadows.'),
  ([('a última vez', 106), ('que você pegou', 96), ('seu filho no colo.', 92)],
   'a father carrying a sleepy boy of about 6 on his hip through the front door at dusk, the boy\'s shoes dangling.'),
  ([('a última vez', 106), ('que brincou na', 96), ('rua com os amigos.', 90)],
   'a group of children playing marbles on a dirt sidewalk at sunset, one of them looking back over his shoulder.'),
  ([('a última vez', 106), ('que sua mãe', 100), ('chamou pra jantar.', 92)],
   'a mother standing at a kitchen door calling out into the backyard, a towel over her shoulder, warm window light.'),
  ([('presta atenção', 96), ('nas vezes', 112), ('de hoje.', 122), _, ('manda pra quem você quer que preste atenção', 36)],
   'a grandmother and a small girl sitting on porch steps eating popsicles, golden hour, the moment feels eternal.'),
 ], "Teve uma última vez pra muita coisa, e ninguém avisou que era a última.\n\n"
    "Por isso, presta atenção nas vezes de hoje. Alguma delas também vai ser a última.\n\n"
    "Qual \"última vez\" você queria ter aproveitado mais? 🤍\n\n"
    "#tempo #nostalgia #família #reflexão #verdadesatemporais"),

 ('sorriso', 'rb-042', '2026-11-20', '21:00', 'acolhimento', 'single image: someone smiled at you today and cried on the way home',
  'one woman around 30 in a supermarket uniform.', [
  ([('tem gente que', 100), ('sorriu pra você', 96), ('hoje e chorou', 100), ('na volta pra casa.', 92), _, ('seja gentil.', 70)],
   'night, a woman around 30 in a supermarket cashier uniform sitting by the window of an almost empty bus, wiping a tear, city lights passing outside, deep blue tones.'),
 ], "A moça do caixa, o motorista, o colega que sempre brinca. Você não sabe o que cada um está enfrentando.\n\n"
    "Gentileza não custa nada e pode ser a única coisa boa do dia de alguém.\n\n"
    "Manda pra lembrar alguém de ser gentil amanhã. 🤍\n\n"
    "#gentileza #empatia #reflexão #acolhimento #verdadesatemporais"),

 # ---------------- sábado 21/11
 ('vida-adulta', 'rb-043', '2026-11-21', '12:00', 'validacao', 'things adult life teaches the hard way; each image an independent scene',
  'different adults in each image, as described.', [
  ([('o que a vida', 106), ('adulta ensina', 100), ('na marra:', 112)],
   'a woman around 35 carrying grocery bags up the stairs of a building, keys in her teeth, calm determined face.'),
  ([('nem todo mundo', 96), ('vai gostar', 112), ('de você.', 122)],
   'a man standing calmly at a party balcony while a small group whispers behind him, he looks at the view, unbothered.'),
  ([('silêncio', 122), ('também é', 112), ('resposta.', 122)],
   'a woman reading her phone on a park bench, then putting it face down in her lap and looking at the trees, serene.'),
  ([('dinheiro resolve', 92), ('muito, mas não', 96), ('resolve solidão.', 96)],
   'a man in a nice apartment eating dinner alone at a big table, a city view behind him.'),
  ([('e família às', 100), ('vezes é quem', 100), ('você escolhe.', 106), _, ('marca a família que você escolheu', 40)],
   'a group of friends of different ages sharing a meal around a small table on a veranda full of plants, laughing.'),
 ], "Ninguém avisa, mas a vida adulta ensina algumas coisas na marra. Silêncio também é resposta, dinheiro não resolve solidão e família às vezes é quem a gente escolhe.\n\n"
    "Qual dessas você aprendeu do jeito difícil?\n\n"
    "Marca a família que você escolheu. 🤍\n\n"
    "#vidaadulta #amadurecimento #amizade #reflexão #verdadesatemporais"),

 ('quem-fica', 'rb-044', '2026-11-21', '18:00', 'afeto', 'who stays when everything falls apart',
  'Clara, 33, dark brown skin, short natural hair, grey sweatshirt; her friend Gabi, 34, light skin, red hair, wine-colored coat.', [
  ([('quem fica', 122), ('quando tudo', 106), ('desaba', 132)],
   'a messy living room, Clara curled up on the sofa under a blanket, the curtains closed, a knock-like light from the door opening.'),
  ([('não é quem', 106), ('mais aparece', 106), ('nas fotos.', 122)],
   'a wall of photos of parties and trips slightly out of focus in a hallway, Clara walking past them without looking.'),
  ([('é quem leva', 106), ('comida sem', 112), ('perguntar.', 122)],
   'Gabi at Clara\'s door holding a pot wrapped in a dish towel and a bag of bread, warm smile.'),
  ([('e senta do lado', 96), ('sem exigir', 112), ('conversa.', 122), _, ('marca quem ficou', 44)],
   'Clara and Gabi sitting on the floor of the living room against the sofa, eating from the same pot, Gabi\'s head on Clara\'s shoulder, warm lamp light.'),
 ], "Quando tudo desaba, a gente descobre quem fica. E quase nunca é quem mais aparece nas fotos.\n\n"
    "É quem leva comida sem perguntar e senta do lado sem exigir conversa.\n\n"
    "Marca quem ficou. 🤍\n\n"
    "#amizade #amor #lealdade #reflexão #verdadesatemporais"),

 ('recomecar', 'rb-045', '2026-11-21', '21:00', 'motivacao', 'single image: starting over at any age is courage with experience',
  'one woman around 52.', [
  ([('recomeçar aos 30,', 90), ('aos 40, aos 60', 96), ('não é atraso.', 106), _, ('é coragem com experiência.', 60)],
   'a woman around 52 with grey streaks in her hair walking down a red dirt road with a small suitcase toward green hills and a sunrise, small figure in a wide landscape.'),
 ], "Não existe idade certa pra mudar de vida. Quem recomeça mais tarde leva uma coisa que ninguém tem aos 20: experiência.\n\n"
    "Se você está começando de novo, você não está atrasado. Está indo.\n\n"
    "Manda pra quem está recomeçando. 🤍\n\n"
    "#recomeço #coragem #motivação #reflexão #verdadesatemporais"),

 # ---------------- domingo 22/11
 ('mae-moca', 'rb-046', '2026-11-22', '12:00', 'nostalgia', 'before being your mother, she was a young woman full of dreams',
  'Dona Rosa, now 62, brown skin, short dyed hair, house dress; as a young woman of 19 in the 1980s, long black hair, yellow dress.', [
  ([('antes de ser', 106), ('sua mãe,', 122), ('ela era...', 122)],
   'Dona Rosa at 62 standing at the kitchen sink of a simple house, looking at an old photo stuck on the fridge.'),
  ([('uma moça cheia', 96), ('de planos.', 122)],
   'young Rosa at 19 in a yellow dress sitting on a bus with a notebook on her lap, looking out the window and dreaming.'),
  ([('que dançava', 106), ('na cozinha.', 112)],
   'young Rosa dancing alone in a 1980s kitchen with a radio on the counter, laughing, her hair flying.'),
  ([('e abriu mão de', 96), ('coisas que você', 96), ('nem sabe.', 122)],
   'young Rosa holding a baby in her arms at a window, a closed suitcase and a notebook on a chair behind her.'),
  ([('pergunta pra ela', 92), ('quais eram', 112), ('os sonhos dela.', 96), _, ('manda pra sua mãe', 44)],
   'Dona Rosa at 62 and her adult daughter sitting on the sofa looking at an old photo album together, laughing.'),
 ], "Antes de ser sua mãe, ela era uma moça com planos, que dançava na cozinha e tinha uma vida inteira pela frente.\n\n"
    "Muita coisa ela deixou pra trás sem contar pra ninguém. Pergunta pra ela quais eram os sonhos dela.\n\n"
    "Manda pra sua mãe. 🤍\n\n"
    "#mãe #família #nostalgia #amor #verdadesatemporais"),

 ('ansiedade', 'rb-047', '2026-11-22', '18:00', 'acolhimento', 'anxiety is living tomorrow with today\'s body',
  'Téo, 27, light brown skin, curly hair, glasses, appears in every image.', [
  ([('ansiedade é', 106), ('viver amanhã', 106), ('com o corpo', 106), ('de hoje.', 122)],
   'night, Téo sitting on the edge of his bed with his hand on his chest, the window showing a city skyline far away, blue tones.'),
  ([('seu corpo', 122), ('está aqui.', 122)],
   'Téo sitting on a chair in a small bedroom, his feet on the floor, his shadow on the wall running away toward the door.'),
  ([('sua cabeça está', 96), ('em daqui a', 112), ('dez anos.', 122)],
   'Téo at a window looking at a long winding road of city lights disappearing into the horizon.'),
  ([('volta.', 140), ('o agora também', 96), ('precisa de você.', 96), _, ('salva pra ler numa noite difícil', 40)],
   'Téo lying on the floor of his room with eyes closed, one hand on his belly, a warm lamp beside him, a plant, calm.'),
 ], "A ansiedade leva a cabeça pra daqui a dez anos e deixa o corpo aqui, sofrendo por coisas que ainda nem aconteceram.\n\n"
    "Volta. Pé no chão, respira devagar. O agora também precisa de você.\n\n"
    "Salva pra ler numa noite difícil. 🤍\n\n"
    "#ansiedade #saúdemental #respira #acolhimento #verdadesatemporais"),

 ('quem-voce-aceitava', 'rb-048', '2026-11-22', '21:00', 'validacao', 'single image: some people do not miss you, they miss who you accepted to be',
  'one woman around 32.', [
  ([('tem gente que', 100), ('não sente falta', 96), ('de você.', 122), _, ('sente falta de quem', 64), ('você aceitava ser.', 64)],
   'a woman around 32 standing tall on a veranda full of plants at morning, coffee in hand, a phone with a message ignored on the table, calm and firm expression.'),
 ], "Quando você começa a se respeitar, algumas pessoas dizem que você mudou. E mudou mesmo.\n\n"
    "Elas não sentem falta de você. Sentem falta de quem aceitava tudo calado.\n\n"
    "Manda pra quem está aprendendo a se colocar. 🤍\n\n"
    "#limites #autoestima #amorpróprio #reflexão #verdadesatemporais"),

 # ---------------- segunda 23/11
 ('amizade-silencio', 'rb-049', '2026-11-23', '12:00', 'afeto', 'some friendships do not end, they just go quiet waiting for us to come back',
  'Mari, 31, brown skin, long wavy hair; Ju, 31, light skin, short black bob.', [
  ([('tem amizade', 106), ('que não acaba.', 100), ('só fica em', 106), ('silêncio.', 132)],
   'Mari sitting on her sofa looking at a framed photo of her and Ju as teenagers, warm amber light.'),
  ([('a vida foi', 112), ('levando.', 132)],
   'split composition with a painted vertical divider: left Mari in an office at a computer, right Ju in a kitchen holding a baby, both busy.'),
  ([('mas se você', 106), ('ligar hoje,', 112), ('ela atende', 112), ('como se', 122), ('fosse ontem.', 112), _, ('manda pra ela', 46)],
   'Mari and Ju hugging tightly at the door of a small café, both laughing with tears in their eyes, string lights.'),
 ], "A gente parou de se falar sem briga nenhuma. A vida foi levando, cada uma pro seu lado.\n\n"
    "Mas tem amizade que só fica em silêncio. Se você ligar hoje, ela atende como se fosse ontem.\n\n"
    "Manda pra ela. 🤍\n\n"
    "#amizade #saudade #amigas #reflexão #verdadesatemporais"),

 ('heranca', 'rb-050', '2026-11-23', '18:00', 'validacao', 'things you inherited from your family that you do not need to pass on (breaking generational cycles)',
  'Caio, 36, brown skin, short beard, linen shirt, and his son Miguel, 5.', [
  ([('o que você', 106), ('herdou e não', 100), ('precisa passar', 100), ('adiante:', 122)],
   'Caio standing in the doorway of an old family house holding Miguel\'s hand, looking inside thoughtfully, soft morning light.'),
  ([('o grito como', 100), ('jeito de', 112), ('conversar.', 122)],
   'Caio kneeling down to Miguel\'s eye level in a bright living room, speaking calmly, a spilled cup of juice on the floor.'),
  ([('o medo de', 106), ('pedir ajuda.', 112)],
   'Caio on a veranda talking openly with an older friend, both on wooden chairs, cups of tea, plants around.'),
  ([('a ideia de que', 96), ('chorar é', 112), ('fraqueza.', 122)],
   'Miguel crying after scraping his knee in a garden and Caio hugging him on the grass, both calm.'),
  ([('você pode', 112), ('ser o fim', 112), ('desse ciclo.', 112), _, ('manda pra quem está quebrando um ciclo', 38)],
   'Caio and Miguel walking hand in hand on a path through a sunny park, away from the viewer, light and airy.'),
 ], "Tem coisa que passa de geração em geração sem ninguém perceber: o grito, o medo de pedir ajuda, a ideia de que chorar é fraqueza.\n\n"
    "Você não precisa repetir. Você pode ser o fim desse ciclo.\n\n"
    "Manda pra quem está quebrando um ciclo na própria família. 🤍\n\n"
    "#família #maternidade #paternidade #saúdemental #verdadesatemporais"),

 ('dia-dificil', 'rb-051', '2026-11-23', '21:00', 'acolhimento', 'single image: a hard day does not need to become a lesson, only rest',
  'one woman around 40.', [
  ([('se hoje foi', 106), ('difícil, não', 100), ('precisa virar', 100), ('lição.', 140), _, ('só precisa de descanso.', 62)],
   'night, a woman around 40 in a warm bath with only her face above the water, eyes closed, a candle and a small plant on the edge, a window with stars, deep blue tones and golden candle light.'),
 ], "Nem todo dia ruim precisa ensinar alguma coisa. Às vezes foi só difícil mesmo.\n\n"
    "Banho, comida, cama. Amanhã você olha com outros olhos.\n\n"
    "Manda pra quem teve um dia daqueles. 🤍\n\n"
    "#acolhimento #autocuidado #saúdemental #descanso #verdadesatemporais"),

 # ---------------- terça 24/11
 ('receita', 'rb-052', '2026-11-24', '12:00', 'nostalgia', 'ask grandma for her recipe while there is time',
  'Vó Ivone, 82, light brown skin, white curly hair, apron with flowers; her grandson Leo, 27.', [
  ([('pede a receita', 96), ('pra sua vó', 106), ('enquanto', 122), ('dá tempo.', 122)],
   'Vó Ivone stirring a big aluminum pot on an old stove in a 1990s kitchen, steam rising, tiled wall.'),
  ([('aquela', 132), ('sem medida.', 112)],
   'close view of Vó Ivone\'s hands throwing a pinch of salt and a handful of flour into a bowl, no measuring cups.'),
  ([('“põe um', 112), ('tanto assim.”', 106)],
   'Vó Ivone showing a handful of something to Leo, who laughs while trying to write in a small notebook.'),
  ([('anota.', 132), ('grava.', 132), ('pergunta', 122), ('de novo.', 122), _, ('algumas heranças cabem num caderno', 38)],
   'Leo and Vó Ivone at the kitchen table, he holds a phone recording her as she explains with her hands, both laughing, a cake cooling.'),
 ], "Aquela receita que não tem medida, só \"um tanto assim\". Um dia você vai querer aquele gosto de novo.\n\n"
    "Anota, grava um vídeo, pergunta de novo. Algumas heranças cabem num caderno.\n\n"
    "Qual receita da sua vó você queria ter? 🤍\n\n"
    "#vó #receitadevó #família #nostalgia #verdadesatemporais"),

 ('pedir-ajuda', 'rb-053', '2026-11-24', '18:00', 'validacao', 'asking for help does not make you less capable',
  'Sônia, 45, dark brown skin, glasses, braids in a bun, appears in every image.', [
  ([('você ajuda', 112), ('todo mundo.', 122)],
   'Sônia at a bright kitchen counter packing lunch boxes for others, a phone on her shoulder, plants by the window.'),
  ([('mas trava na', 100), ('hora de pedir.', 100)],
   'Sônia sitting alone on her veranda holding her phone with a message typed and not sent, hesitating.'),
  ([('deixar alguém', 100), ('cuidar de você', 96), ('também é', 112), ('coragem.', 132), _, ('manda pra quem nunca pede ajuda', 40)],
   'Sônia sitting on the sofa with her feet up while a friend puts a cup of tea in her hands and a blanket on her lap, Sônia smiling shyly.'),
 ], "Você é a primeira a ajudar todo mundo. Mas na hora de pedir, trava.\n\n"
    "Deixar alguém cuidar de você não te faz menos capaz. Também é coragem.\n\n"
    "Manda pra quem nunca pede ajuda. 🤍\n\n"
    "#pedirajuda #saúdemental #autocuidado #reflexão #verdadesatemporais"),

 ('casa-cheia', 'rb-054', '2026-11-24', '21:00', 'acolhimento', 'single image: there are houses full of people where everyone feels alone',
  'a family of four.', [
  ([('tem casa cheia', 96), ('de gente onde', 100), ('todo mundo', 112), ('se sente', 112), ('sozinho.', 132)],
   'night, cross-section of a small house seen from outside: four lit windows, in each one a family member alone in a different room (a father on the sofa, a mother in the kitchen, a teenager in bed with a phone, a child drawing on the floor), deep blue night around.'),
 ], "Todo mundo debaixo do mesmo teto, cada um no seu quarto, no seu celular, no seu silêncio.\n\n"
    "Às vezes o que falta não é gente. É conversa. Hoje, bate na porta do lado.\n\n"
    "Isso acontece na sua casa? 🤍\n\n"
    "#família #solidão #conversa #reflexão #verdadesatemporais"),

 # ---------------- quarta 25/11
 ('o-que-vale', 'rb-055', '2026-11-25', '12:00', 'finitude', 'things worth more than you imagine; each image an independent scene',
  'different people in each image, as described.', [
  ([('o que vale', 112), ('mais do que', 106), ('você imagina:', 106)],
   'a pair of worn slippers next to a porch chair with a cup of coffee on the floor, golden late afternoon light, a plant in a tin can.'),
  ([('uma tarde sem', 100), ('pressa com quem', 96), ('você ama.', 122)],
   'a couple in their sixties sitting on the porch watching the street, his hand over hers, golden light.'),
  ([('uma conversa', 106), ('sem celular', 112), ('na mesa.', 122)],
   'three adult siblings around a kitchen table laughing, their phones stacked face down in a fruit bowl.'),
  ([('ouvir a risada', 96), ('dos seus pais.', 106)],
   'an elderly mother and father laughing hard on a sofa while their adult daughter watches them smiling.'),
  ([('o tempo', 122), ('não volta.', 122), ('a lembrança', 112), ('fica.', 140), _, ('manda pra quem você quer perto', 40)],
   'a family photograph being taken in a backyard at sunset: grandparents, children and grandchildren squeezing together, laughing.'),
 ], "Uma tarde sem pressa, uma conversa sem celular, a risada dos seus pais. Parece pouco até a gente perceber que é tudo.\n\n"
    "O tempo não volta. A lembrança fica.\n\n"
    "Manda pra quem você quer perto. 🤍\n\n"
    "#tempo #família #gratidão #amor #verdadesatemporais"),

 ('transformou', 'rb-056', '2026-11-25', '18:00', 'motivacao', 'you do not need to go back to who you were; you transformed',
  'Jade, 30, brown skin, short curly hair, green jacket, backpack, appears in every image.', [
  ([('você não', 122), ('precisa voltar', 100), ('a ser quem era.', 96)],
   'Jade standing on top of a green hill at sunrise, looking at a wide valley, wind in her jacket.'),
  ([('depois de tudo', 100), ('que passou,', 112)],
   'Jade walking on a muddy red dirt road after a storm, puddles reflecting a clearing sky.'),
  ([('é natural', 112), ('ter mudado.', 112)],
   'Jade sitting on a rock by a river, her old torn sneakers beside her and new boots on her feet, looking at the water.'),
  ([('você não', 122), ('se perdeu.', 122), ('se transformou.', 100), _, ('manda pra quem sente falta de quem era', 38)],
   'Jade walking forward on a road through a field of yellow flowers toward a bright golden sky, small figure, open landscape.'),
 ], "Depois de tudo que você passou, é natural não ser mais a mesma pessoa. E tudo bem.\n\n"
    "Você não se perdeu. Você se transformou.\n\n"
    "Manda pra quem sente falta de quem era. 🤍\n\n"
    "#transformação #recomeço #amadurecimento #motivação #verdadesatemporais"),

 ('jeito', 'rb-057', '2026-11-25', '21:00', 'luto', 'single image: some people leave and their ways keep living in us',
  'one woman around 40.', [
  ([('tem gente que', 100), ('vai embora e', 100), ('deixa o jeito', 100), ('morando', 122), ('na gente.', 122)],
   'early morning, a woman around 40 in a quiet kitchen making coffee in an old cloth strainer the way her mother did, an old cardigan hanging on a hook, a photo of an older woman on the wall, soft lilac and pink light.'),
 ], "O jeito de passar o café, uma expressão que ela falava, a mania de guardar sacolinha. Quem a gente ama vai embora e deixa o jeito morando na gente.\n\n"
    "Que jeito de alguém que se foi ainda mora em você? 🤍\n\n"
    "#saudade #luto #amor #memória #verdadesatemporais"),

 # ---------------- quinta 26/11
 ('pai', 'rb-058', '2026-11-26', '12:00', 'causa', 'fathers who never say "I love you" but show it with care',
  'Seu Jorge, 64, dark brown skin, grey short hair, blue cap; his daughter Bia, 30.', [
  ([('seu pai pode', 100), ('não dizer', 112), ('“eu te amo”.', 112), ('mas ele...', 122)],
   'Seu Jorge standing at the gate of his house with arms crossed and a serious face as Bia\'s car arrives, a hint of a smile.'),
  ([('conferiu o óleo', 96), ('do seu carro.', 106)],
   'Seu Jorge with the hood of Bia\'s old car open, checking the oil stick carefully, a cloth on his shoulder.'),
  ([('esperou', 122), ('acordado você', 100), ('chegar.', 132)],
   'night, Seu Jorge sitting in an armchair by the window with the TV off, waiting, the door opening.'),
  ([('perguntou', 122), ('“já comeu?”', 112)],
   'Seu Jorge putting a plate of food on the table in front of Bia, who laughs.'),
  ([('tem pai que ama', 96), ('no idioma', 112), ('do cuidado.', 112), _, ('manda pro seu pai', 44)],
   'Bia hugging Seu Jorge from the side at the gate, he pretends to be annoyed but smiles, blue evening sky.'),
 ], "Ele não fala \"eu te amo\". Mas confere o óleo do seu carro, espera você chegar e pergunta se você já comeu.\n\n"
    "Tem pai que ama no idioma do cuidado. Neste Novembro Azul, cuida dele também: lembra ele de fazer os exames.\n\n"
    "Manda pro seu pai. 💙\n\n"
    "#pai #novembroazul #família #amor #verdadesatemporais"),

 ('limite-familia', 'rb-059', '2026-11-26', '18:00', 'validacao', 'loving your family does not oblige you to accept everything',
  'Lu, 35, light brown skin, long straight dark hair, beige linen shirt, appears in every image.', [
  ([('amar sua família', 92), ('não te obriga a', 96), ('aceitar tudo.', 106)],
   'Lu standing at the open door of a bright house with plants, calm and firm, holding the door handle.'),
  ([('dá pra amar', 112), ('e colocar', 112), ('limite.', 132)],
   'Lu at a family lunch table speaking calmly with her hand raised gently, the others listening.'),
  ([('dá pra amar', 112), ('de longe.', 122)],
   'Lu on her own veranda talking to her mother on a video call, smiling, sunlight.'),
  ([('dá pra perdoar', 96), ('sem voltar ao', 100), ('mesmo lugar.', 106), _, ('manda pra quem precisa ouvir isso', 40)],
   'Lu walking out of an old house through a garden gate, closing it gently behind her, a calm open path ahead.'),
 ], "Família é importante, mas laço de sangue não é autorização pra te machucar.\n\n"
    "Dá pra amar e colocar limite. Dá pra amar de longe. Dá pra perdoar sem voltar ao mesmo lugar.\n\n"
    "Manda pra quem precisa ouvir isso hoje. 🤍\n\n"
    "#limites #família #saúdemental #amorpróprio #verdadesatemporais"),

 ('chorar', 'rb-060', '2026-11-26', '21:00', 'acolhimento', 'single image: crying is not falling apart, it is the soul putting the weight down',
  'one young man around 25.', [
  ([('chorar não é', 106), ('desmoronar.', 122), _, ('é a alma tirando', 66), ('o peso das costas.', 66)],
   'night, a young man around 25 sitting on a rooftop at night, arms around his knees, crying quietly, a big heavy backpack set down beside him, a full moon and city lights, deep blue tones.'),
 ], "Chorar não é fraqueza nem desmoronar. É o corpo e a alma colocando no chão um peso que estava grande demais.\n\n"
    "Se precisar, chora. Depois respira. Você continua inteiro.\n\n"
    "Salva pra lembrar disso. 🤍\n\n"
    "#chorar #saúdemental #acolhimento #emoções #verdadesatemporais"),

 # ---------------- sexta 27/11 (Black Friday)
 ('carrinho', 'rb-061', '2026-11-27', '12:00', 'humor', 'not everything that is missing can be bought (Black Friday), gently ironic',
  'Duda, 28, light brown skin, curly hair in a high bun, yellow hoodie, appears in every image.', [
  ([('nem tudo', 122), ('que falta', 122), ('se compra.', 122)],
   'Duda sitting on the floor of a small apartment surrounded by delivery boxes, opening one, a lonely face.'),
  ([('o carrinho', 112), ('cheio.', 140)],
   'Duda on the sofa scrolling a shopping app on her phone at night, the screen glowing, many boxes stacked by the door.'),
  ([('e o peito', 112), ('vazio.', 140)],
   'Duda lying on the bed among shopping bags looking at the ceiling, the room full of things but cold.'),
  ([('às vezes falta', 96), ('tempo, abraço,', 100), ('sono.', 140)],
   'Duda on a video call with her grandmother, laughing, the boxes forgotten in the corner, warm light.'),
  ([('antes de comprar,', 90), ('pergunta o que', 100), ('você quer', 112), ('preencher.', 122), _, ('manda pra quem está com o carrinho cheio', 36)],
   'Duda closing her laptop and going out of the apartment door to meet friends waiting on the street, sunny day.'),
 ], "Black Friday é ótima pra comprar o que você precisa. Mas tem vazio que não cabe em carrinho.\n\n"
    "Às vezes o que falta é tempo, abraço, sono. Antes de comprar, pergunta o que você está tentando preencher.\n\n"
    "Manda pra quem está com o carrinho cheio. 😅🤍\n\n"
    "#blackfriday #consumo #saúdemental #reflexão #verdadesatemporais"),

 ('sozinha', 'rb-062', '2026-11-27', '18:00', 'validacao', 'learning to be alone changed everything',
  'Iara, 37, brown skin, long braids, terracotta dress, appears in every image.', [
  ([('aprender a', 112), ('ficar sozinha', 100), ('mudou tudo.', 112)],
   'Iara having breakfast alone at a sunny café table with a book, relaxed and happy.'),
  ([('parei de aceitar', 92), ('qualquer', 122), ('companhia.', 122)],
   'Iara leaving a noisy party early, walking calmly down an evening street, lights behind her.'),
  ([('descobri do', 106), ('que eu gosto.', 106)],
   'Iara painting on a small canvas on her veranda full of plants, wearing headphones, smiling.'),
  ([('e quem chega', 106), ('agora soma.', 112), ('não completa.', 106), _, ('manda pra quem está aprendendo a se bastar', 36)],
   'Iara walking in a park next to a friend, both carrying flowers, laughing, open light sky.'),
 ], "Ficar sozinha assusta no começo. Depois vira encontro: você descobre do que gosta, para de aceitar qualquer companhia e entende o próprio valor.\n\n"
    "Quem chega depois disso soma. Não completa.\n\n"
    "Manda pra quem está aprendendo a se bastar. 🤍\n\n"
    "#amorpróprio #solitude #autoestima #reflexão #verdadesatemporais"),

 ('forte', 'rb-063', '2026-11-27', '21:00', 'acolhimento', 'single image: being strong all the time keeps away the people who wanted to care for you',
  'one woman around 38.', [
  ([('ser forte o', 106), ('tempo todo', 112), ('afasta quem', 106), ('queria cuidar', 100), ('de você.', 122)],
   'night, a woman around 38 sitting on the stairs of a building, holding a heavy box on her lap alone, while through a lit doorway above her a friend looks at her wanting to help, deep blue tones and warm door light.'),
 ], "Quando você nunca mostra que precisa, as pessoas acreditam. E param de oferecer.\n\n"
    "Deixa alguém ver onde dói. Ser cuidada também é bom.\n\n"
    "Manda pra quem é forte demais. 🤍\n\n"
    "#força #vulnerabilidade #saúdemental #acolhimento #verdadesatemporais"),

 # ---------------- sábado 28/11
 ('crianca', 'rb-064', '2026-11-28', '12:00', 'nostalgia', 'your inner child remembers everything; today you can give her what she did not receive',
  'Vânia, 36, brown skin, short curly hair; herself as a girl of 7 in the 1990s, pigtails, yellow dress.', [
  ([('sua criança', 112), ('interior lembra', 96), ('de tudo.', 132)],
   'little Vânia at 7 sitting alone on the steps of a 1990s backyard, chin in her hands, a clothesline behind her.'),
  ([('do abraço', 112), ('que faltou.', 122)],
   'little Vânia standing at the door of a living room watching adults who do not notice her, holding a drawing.'),
  ([('do elogio', 112), ('que nunca veio.', 100)],
   'little Vânia holding a school notebook with a star sticker, showing it to a busy adult who keeps washing dishes.'),
  ([('hoje você pode', 96), ('dar pra ela o', 100), ('que não', 122), ('recebeu.', 132), _, ('manda pra quem está se cuidando por dentro', 36)],
   'adult Vânia sitting on the backyard steps hugging little Vânia, both smiling with eyes closed, faded warm light.'),
 ], "Aquele abraço que faltou, o elogio que nunca veio. A criança que você foi ainda lembra.\n\n"
    "Hoje você pode dar pra ela o que não recebeu: paciência, carinho, orgulho.\n\n"
    "O que a sua criança interior precisava ouvir? 🤍\n\n"
    "#criançainterior #autocuidado #saúdemental #infância #verdadesatemporais"),

 ('fim', 'rb-065', '2026-11-28', '18:00', 'afeto', 'the end of a relationship is not a failure',
  'Leo, 33, light brown skin, short hair, wine sweater; Rita, 32, dark brown skin, long braids.', [
  ([('fim de relação', 96), ('não é fracasso.', 96)],
   'Leo and Rita sitting at opposite ends of the same sofa in a cozy living room, calm sad faces, a box of books between them.'),
  ([('foi bom', 122), ('enquanto foi.', 112)],
   'memory scene: Leo and Rita dancing in a small kitchen with string lights, laughing.'),
  ([('vocês cresceram', 92), ('pra lados', 112), ('diferentes.', 122)],
   'Leo and Rita walking away from each other on a street corner at dusk, each toward a different street, both looking back once.'),
  ([('acabar também', 96), ('pode ser cuidado.', 92), _, ('manda pra quem está encerrando um ciclo', 38)],
   'Rita alone on her balcony at morning with a cup of coffee and new plants, calm and light, a peaceful smile.'),
 ], "Nem todo fim é fracasso. Às vezes vocês só cresceram pra lados diferentes, e foi bom enquanto foi.\n\n"
    "Acabar com respeito também é uma forma de cuidar.\n\n"
    "Manda pra quem está encerrando um ciclo. 🤍\n\n"
    "#relacionamento #fim #recomeço #amor #verdadesatemporais"),

 ('explicacao', 'rb-066', '2026-11-28', '21:00', 'validacao', 'single image: you owe no explanation to someone who decided not to understand you',
  'one man around 35.', [
  ([('você não deve', 100), ('explicação a', 106), ('quem decidiu', 106), ('não te entender.', 96)],
   'a man around 35 sitting calmly on a garden swing at dusk, a crumpled paper with long explanations dropped on the grass, a cup of tea in his hands, sage and sand tones.'),
 ], "Você já explicou, repetiu, desenhou. A pessoa não quis entender.\n\n"
    "Não é falta de clareza sua. É escolha dela. Guarda sua energia pra quem escuta.\n\n"
    "Manda pra quem vive se explicando. 🤍\n\n"
    "#limites #paz #autoestima #reflexão #verdadesatemporais"),

 # ---------------- domingo 29/11
 ('antes-dezembro', 'rb-067', '2026-11-29', '12:00', 'motivacao', 'before December arrives: thank, let go, carry only what is good',
  'Nando, 41, dark brown skin, bald, beard, orange shirt, appears in every image.', [
  ([('antes de', 122), ('dezembro', 132), ('chegar:', 132)],
   'Nando standing at a wide window looking at green hills under a sunrise, a cup of coffee in hand.'),
  ([('agradece', 122), ('o que deu', 112), ('certo.', 140)],
   'Nando kneeling in a vegetable garden at morning picking a tomato, smiling at it.'),
  ([('solta o que', 112), ('não deu.', 132)],
   'Nando on a hill letting go of a bunch of dry leaves into the wind, sky wide open.'),
  ([('e leva só o que', 96), ('te faz bem.', 112), _, ('manda pra quem quer fechar o ano em paz', 38)],
   'Nando walking down a red dirt road at golden hour carrying only a small backpack, flowers on the roadside.'),
 ], "Novembro está acabando. Antes de dezembro chegar com a correria, para um minuto.\n\n"
    "Agradece o que deu certo, solta o que não deu e leva pra frente só o que te faz bem.\n\n"
    "Manda pra quem quer fechar o ano em paz. 🤍\n\n"
    "#fimdeano #gratidão #recomeço #reflexão #verdadesatemporais"),

 ('presenca', 'rb-068', '2026-11-29', '18:00', 'finitude', 'nobody remembers the gift, they remember who was there',
  'a family across the years: Pedro as a boy of 7, his father Seu Mauro, his mother Dona Célia.', [
  ([('ninguém lembra', 96), ('do presente.', 112)],
   'a colorful birthday table in a simple backyard with a cake, balloons and wrapped gifts, golden afternoon light.'),
  ([('lembra de quem', 96), ('estava lá.', 122)],
   'little Pedro blowing out candles, his father lifting him up, his mother clapping, neighbors around, everyone laughing.'),
  ([('de quem cantou', 96), ('parabéns', 122), ('mais alto.', 122)],
   'Seu Mauro singing with his mouth wide open and eyes closed, arms up, everyone laughing at him.'),
  ([('esteja lá.', 132), ('é isso que fica.', 96), _, ('manda pra quem sempre esteve lá', 40)],
   'grown-up Pedro, now 35, sitting with his aging parents on the same backyard steps at sunset, looking at an old photo of that birthday.'),
 ], "Do aniversário de criança, quase ninguém lembra do presente. Lembra de quem estava lá e de quem cantou parabéns mais alto.\n\n"
    "Presença é o que fica. Esteja lá.\n\n"
    "Manda pra quem sempre esteve lá. 🤍\n\n"
    "#presença #família #memória #amor #verdadesatemporais"),

 ('escolhe', 'rb-069', '2026-11-29', '21:00', 'validacao', 'single image: you waited too long for someone to choose you, choose yourself',
  'one woman around 30.', [
  ([('você esperou', 100), ('muito tempo', 106), ('alguém', 132), ('te escolher.', 112), _, ('escolhe você.', 70)],
   'a woman around 30 standing in front of a mirror in a bright bedroom full of plants, adjusting her collar and smiling at herself, morning light, sage and sand tones.'),
 ], "Esperar alguém te escolher cansa. E faz você aceitar menos do que merece.\n\n"
    "Começa por você. O resto vem, ou não vem, e você fica bem do mesmo jeito.\n\n"
    "Manda pra quem precisa se escolher. 🤍\n\n"
    "#amorpróprio #autoestima #escolhas #reflexão #verdadesatemporais"),

 # ---------------- segunda 30/11
 ('novembro', 'rb-070', '2026-11-30', '12:00', 'acolhimento', 'single image: you reached the end of November with everything you carried, that is not little',
  'one man around 45.', [
  ([('você chegou', 112), ('ao fim de', 112), ('novembro.', 132), _, ('com tudo que carregou.', 62), ('isso não é pouco.', 62)],
   'dawn, a man around 45 sitting on the steps at the door of his house with a cup of coffee, the first light of morning coming over the rooftops, deep blue fading into warm gold.'),
 ], "Com tudo que você carregou este mês, chegar até aqui não é pouco.\n\n"
    "Respira. Dezembro começa amanhã e você não precisa entrar nele correndo.\n\n"
    "Manda pra quem chegou cansado ao fim do mês. 🤍\n\n"
    "#novembro #acolhimento #gratidão #saúdemental #verdadesatemporais"),
]
P = {p[0]: p for p in POSTS}


def cenas(chave):
    k, num, data, hora, cat, ideia, elenco, slides, leg = P[chave]
    c = [cena for _t, cena in slides]
    if len(c) == 1:
        c.append(c[0] + ' Alternative composition, different angle.')
    return c


def grupos(maximo=13):
    """Agrupa os posts em pedidos de até `maximo` imagens, na ordem da agenda."""
    gs, atual, n = [], [], 0
    for k, *_r in POSTS:
        q = len(cenas(k))
        if atual and n + q > maximo:
            gs.append(atual); atual, n = [], 0
        atual.append(k); n += q
    if atual:
        gs.append(atual)
    return gs


def email(gi, chaves):
    assunto = f'{PREFIXO}-q{gi:02d}'
    estilo = ESTILO.replace('vertical 4:5 (1080x1350)', 'vertical 4:5 portrait format')
    total = sum(len(cenas(k)) for k in chaves)
    L = [f'Generate {total} separate illustrations, one at a time, in the order below. Do not ask me anything. '
         'Before each image, write its file name. Save each one as a PNG file in the root folder of my Google Drive (My Drive), '
         'using exactly the file names below.', '',
         f'STYLE (apply to every image): {estilo}', '',
         'Each SERIES below has its own color palette, world and characters. Keep the same characters with the same look '
         'inside a series. Correct anatomy: every person has exactly two arms, two hands and two legs.', '']
    for k in chaves:
        _k, num, data, hora, cat, ideia, elenco, slides, leg = P[k]
        c = CAT[cat]
        L += [f'SERIES {k.upper()}. IDEA: {ideia}. CHARACTERS: {elenco}',
              f'COLOR PALETTE of this series (use only this): {c["paleta"]}. WORLD: {c["mundo"]}. '
              f'TYPE OF CHARACTERS: {c["elenco"]}. TYPICAL OBJECTS: {c["objetos"]}.', '']
        for i, cena in enumerate(cenas(k), 1):
            L.append(f'{assunto}-{k}{i:02d}: {cena} Upper third: plain continuous wall or sky, empty.')
        L.append('')
    return assunto, '\n'.join(L)


def imagem(chave, n):
    for cand in (f'{PREFIXO}-{chave}{n:02d}b.png', f'{PREFIXO}-{chave}{n:02d}.png'):
        p = os.path.join(FOTOS, cand)
        if os.path.exists(p):
            return p


def gerar(chave):
    k, num, data, hora, cat, ideia, elenco, slides, leg = P[chave]
    saida = os.path.join(SAIDA, chave)
    os.makedirs(saida, exist_ok=True)
    feitos = 0
    for i, (linhas, cena) in enumerate(slides, 1):
        p = imagem(chave, i)
        if not p:
            print('falta', f'{PREFIXO}-{chave}{i:02d}'); continue
        img = grao(preencher(Image.open(p)), 3, seed=i)
        img, _y = escrever_titulo(img, linhas, i * 7, CAT[cat]['tinta'])
        assinatura(img).save(os.path.join(saida, f'{i:02d}.jpg'), quality=93)
        feitos += 1
    print(chave, feitos, 'de', len(slides))
    return feitos == len(slides)


def fila(chave):
    k, num, data, hora, cat, ideia, elenco, slides, leg = P[chave]
    origem = os.path.join(SAIDA, chave)
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
    itens.sort(key=lambda p: (p['data'], p.get('hora', '20:00')))
    json.dump(itens, open(caminho, 'w'), ensure_ascii=False, indent=1)
    print('na fila:', num, data, hora)


def teste():
    fundo = Image.new('RGB', (W, H), (240, 200, 170))
    thumbs = []
    for k, *_r in POSTS:
        for i, (linhas, cena) in enumerate(P[k][7], 1):
            img, y = escrever_titulo(fundo.copy(), linhas, i)
            d = ImageDraw.Draw(img)
            d.line((0, 455, W, 455), fill=(255, 0, 0), width=5)
            d.text((20, 560), f'{k} {i}', fill=(0, 0, 0))
            thumbs.append(img.crop((0, 0, W, 600)).resize((270, 150)))
    cols = 8
    S = Image.new('RGB', (270 * cols, 150 * ((len(thumbs) + cols - 1) // cols)), 'white')
    for n, t in enumerate(thumbs):
        S.paste(t, ((n % cols) * 270, (n // cols) * 150))
    os.makedirs(SAIDA, exist_ok=True)
    S.save(os.path.join(SAIDA, 'teste.jpg'), quality=85)


def chaves_de(args):
    return [p[0] for p in POSTS] if args == ['todos'] else args


if __name__ == '__main__':
    acao, *args = sys.argv[1:]
    if acao == 'emails':
        os.makedirs(SAIDA, exist_ok=True)
        out = []
        for gi, ch in enumerate(grupos(), 1):
            a, corpo = email(gi, ch)
            out.append({'assunto': a, 'chaves': ch, 'imagens': sum(len(cenas(k)) for k in ch), 'corpo': corpo})
        json.dump(out, open(os.path.join(SAIDA, 'emails.json'), 'w'), ensure_ascii=False, indent=1)
        for o in out:
            print(o['assunto'], o['imagens'], o['chaves'])
    elif acao == 'gerar':
        for c in chaves_de(args): gerar(c)
    elif acao == 'fila':
        for c in chaves_de(args): fila(c)
    elif acao == 'teste':
        teste()
