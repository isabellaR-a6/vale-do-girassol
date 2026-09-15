"""Constantes, paleta de cores e dados do jogo (culturas, animais, construções)."""
import os
import sys

# True quando o jogo roda no navegador (versão web gerada pelo pygbag)
WEB = sys.platform == "emscripten"
# True quando o jogo roda como app Android (APK gerado pelo Buildozer / python-for-android)
ANDROID = "ANDROID_ARGUMENT" in os.environ
# True quando o jogo roda como app de iPhone (.ipa gerado pelo pygame-ios)
IOS = sys.platform == "ios"

# Resolução lógica (a janela é ampliada em pixels inteiros pelo pygame.SCALED)
LARGURA, ALTURA = 640, 360
# O cenário é desenhado em baixa resolução e ampliado 2x, para pixels "gordinhos"
ARTE_L, ARTE_A = 320, 104
ESCALA_ARTE = 2
CAIXA_Y = ARTE_A * ESCALA_ARTE  # onde começa a caixa de diálogo
FPS = 60

TITULO_JOGO = "Vale do Girassol"
ARQUIVO_SAVE = "save_fazenda.json"

# Paleta inspirada em Stardew Valley / Hay Day (tons quentes, verdes vivos, madeira)
COR = {
    "contorno": (63, 40, 50),
    "texto": (74, 44, 36),
    "texto_claro": (140, 100, 80),
    "madeira_esc": (102, 57, 49),
    "madeira": (143, 86, 59),
    "madeira_clara": (217, 160, 102),
    "madeira_brilho": (238, 195, 140),
    "pergaminho": (255, 241, 204),
    "pergaminho_esc": (240, 212, 160),
    "ceu": (99, 190, 235),
    "ceu_claro": (150, 215, 245),
    "ceu_horizonte": (205, 238, 248),
    "grama": (106, 190, 48),
    "grama_esc": (70, 145, 45),
    "grama_clara": (153, 229, 80),
    "folha": (55, 110, 40),
    "terra": (150, 98, 60),
    "terra_esc": (112, 70, 44),
    "terra_molhada": (92, 58, 38),
    "agua": (70, 120, 220),
    "agua_clara": (110, 170, 255),
    "amarelo": (251, 232, 70),
    "dourado": (230, 170, 30),
    "vermelho": (180, 50, 50),
    "vermelho_claro": (225, 90, 90),
    "laranja": (230, 120, 40),
    "rosa": (245, 160, 190),
    "branco": (255, 255, 255),
    "creme": (255, 246, 220),
    "cinza": (160, 170, 180),
    "cinza_esc": (100, 100, 110),
    "roxo": (118, 66, 138),
    "roxo_claro": (170, 120, 200),
    "azul": (60, 90, 170),
    "noite": (25, 35, 75),
    "noite_clara": (50, 60, 110),
    "pele": (245, 200, 160),
    "pele_esc": (190, 130, 90),
    "verde_ui": (90, 170, 60),
    "verde_ui_esc": (50, 110, 40),
}

ESTACOES = ["Primavera", "Verão", "Outono", "Inverno"]
DIAS_POR_ESTACAO = 7
DIAS_DO_ANO = DIAS_POR_ESTACAO * 4

ENERGIA_BASE = 7
CANTEIROS_INICIAIS = 4
CANTEIROS_MAX = 8
PACOTE_RACAO = (10, 40)  # (quantidade, preço)

# Culturas: preço da semente (por canteiro), dias para crescer, preço de venda, nível mínimo
CULTURAS = {
    "trigo":   {"nome": "Trigo",   "semente": 10, "dias": 2, "nivel": 1, "xp": 3},
    "cenoura": {"nome": "Cenoura", "semente": 15, "dias": 3, "nivel": 1, "xp": 4},
    "milho":   {"nome": "Milho",   "semente": 20, "dias": 3, "nivel": 2, "xp": 5},
    "tomate":  {"nome": "Tomate",  "semente": 30, "dias": 4, "nivel": 3, "xp": 7},
    "morango": {"nome": "Morango", "semente": 45, "dias": 4, "nivel": 4, "xp": 9},
    "abobora": {"nome": "Abóbora", "semente": 60, "dias": 5, "nivel": 5, "xp": 12},
}

# Animais: produto, a cada quantos dias produz, ração por dia, onde mora
ANIMAIS = {
    "galinha": {"nome": "Galinha", "preco": 80,  "produto": "ovo",   "intervalo": 1, "racao": 1, "nivel": 1, "casa": "galinheiro"},
    "pato":    {"nome": "Pato",    "preco": 110, "produto": "ovo",   "intervalo": 1, "racao": 1, "nivel": 1, "casa": "galinheiro"},
    "cabra":   {"nome": "Cabra",   "preco": 200, "produto": "leite", "intervalo": 2, "racao": 1, "nivel": 2, "casa": "estabulo"},
    "porco":   {"nome": "Porco",   "preco": 250, "produto": "trufa", "intervalo": 2, "racao": 2, "nivel": 2, "casa": "estabulo"},
    "vaca":    {"nome": "Vaca",    "preco": 350, "produto": "leite", "intervalo": 1, "racao": 3, "nivel": 3, "casa": "estabulo"},
    "ovelha":  {"nome": "Ovelha",  "preco": 450, "produto": "la",    "intervalo": 2, "racao": 3, "nivel": 4, "casa": "estabulo"},
}

# Todos os itens que podem ir para o celeiro, com preço base de venda
ITENS = {
    "trigo": ("Trigo", 28), "cenoura": ("Cenoura", 45), "milho": ("Milho", 55),
    "tomate": ("Tomate", 90), "morango": ("Morango", 125), "abobora": ("Abóbora", 200),
    "ovo": ("Ovo", 22), "trufa": ("Trufa", 120), "leite": ("Leite", 70), "la": ("Lã", 170),
    "pao": ("Pão caseiro", 110), "bolo": ("Bolo de cenoura", 260),
    "geleia": ("Geleia de morango", 480), "queijo": ("Queijo", 210),
    "amora": ("Amora", 15), "cogumelo": ("Cogumelo", 40),
    "lambari": ("Lambari", 20), "tilapia": ("Tilápia", 50), "peixe_dourado": ("Peixe dourado", 350),
    "sopa": ("Sopa de legumes", 240), "omelete": ("Omelete", 130),
    "peixe_assado": ("Peixe assado", 170), "pao_de_milho": ("Pão de milho", 270),
    "torta": ("Torta de abóbora", 500), "manteiga": ("Manteiga", 340),
    "iogurte": ("Iogurte de morango", 430),
    "bolo_fuba": ("Bolo de fubá", 300), "canjica": ("Canjica", 280),
    "abobora_gigante": ("Abóbora gigante", 900),
}

# Comer devolve energia, e comer nao gasta acao. E daqui que vem o folego do
# dia: o jogador troca colheita por tempo. Comida da roca devolve 1; comida
# feita nas oficinas devolve mais, que e o que faz o moinho e a padaria
# valerem a pena.
#
# O pao e de longe o mais eficiente: 3 trigos (¢84) viram ¢110 e +2 de energia.
# A geleia vale ¢480 e devolve so 2 de proposito — ela existe para vender.
COMIDA = {
    "amora": 1, "ovo": 1, "lambari": 1, "cogumelo": 1, "cenoura": 1,
    "tilapia": 1, "milho": 1, "leite": 1, "tomate": 1, "morango": 1,
    "abobora": 1, "trufa": 1,
    "pao": 2, "queijo": 2, "geleia": 2, "peixe_dourado": 2,
    "sopa": 2, "omelete": 2, "peixe_assado": 2, "pao_de_milho": 2,
    "manteiga": 1, "iogurte": 2, "canjica": 2,

    "bolo": 3, "torta": 3, "bolo_fuba": 3,
}

# Quem mora no vale. "adora" e "odeia" sao chutes de personalidade e podem ser
# trocados a vontade: sao sabor, nao equilibrio. "cliente" liga a pessoa ao nome
# que ela usa no quadro de pedidos (quem nao aparece la fica None).
PESSOAS = {
    "vovo":     {"nome": "Vovó Cida", "adora": "bolo", "odeia": "lambari", "cliente": None, "aniversario": 4},
    "ze":       {"nome": "Seu Zé", "adora": "queijo", "odeia": "geleia", "cliente": "Seu Zé", "aniversario": 9},
    "lucia":    {"nome": "Dona Lúcia", "adora": "morango", "odeia": "cogumelo", "cliente": "Dona Lúcia", "aniversario": 13},
    "rosa":     {"nome": "Rosa", "adora": "trufa", "odeia": "bolo", "cliente": "Rosa", "aniversario": 17},
    "bia":      {"nome": "Bia", "adora": "geleia", "odeia": "abobora", "cliente": "Bia", "aniversario": 21},
    "prefeito": {"nome": "Prefeito Otávio", "adora": "pao", "odeia": "milho", "cliente": "o Prefeito", "aniversario": 25},
    "viajante": {"nome": "O viajante", "adora": "peixe_dourado", "odeia": "trigo", "cliente": None, "aniversario": 27},
}
# O que a amizade destrava. Sem isso o medidor enche e nao entrega nada, que e
# pior do que nao ter medidor. O texto aparece na tela da pessoa: o jogador
# precisa VER o que esta perseguindo.
BONUS_AMIZADE = {
    "lucia":    {3: "Vende no mercado por +8%", 5: "Vende no mercado por +15%"},
    "rosa":     {3: "Construções 10% mais baratas", 5: "Construções 20% mais baratas"},
    "prefeito": {3: "Pedidos do quadro pagam +10%", 5: "Pedidos do quadro pagam +20%"},
    "vovo":     {3: "Ela manda comida: às vezes você acorda com um agrado",
                 5: "Come tão bem que rende mais: +1 de energia por dia"},
    "ze":       {3: "Ele reparte a ração dele de vez em quando",
                 5: "Rega seus canteiros quando você esquece"},
    "bia":      {3: "Ela te traz coisas que acha por aí", 5: "Traz coisas melhores, e mais vezes"},
    "viajante": {3: "Aparece com mercadoria diferente", 5: "Guarda as raridades para você"},
}
PONTOS_POR_CORACAO = 10
CORACOES_MAX = 5

CONSTRUCOES = {
    "cozinha":   {"nome": "Cozinha da casa", "preco": 180, "nivel": 1,
                  "desc": "Uma panela boa no fogão: dá para cozinhar o que vem da roça."},
    "galinheiro_grande": {"nome": "Galinheiro ampliado", "preco": 250, "nivel": 2,
                          "desc": "Cabem 5 galinhas em vez de 2."},
    "moinho":    {"nome": "Moinho de ração", "preco": 300, "nivel": 2,
                  "desc": "Transforma trigo e milho em ração para os animais."},
    "estabulo":  {"nome": "Estábulo", "preco": 500, "nivel": 2,
                  "desc": "Abriga até 4 animais grandes: porcos, vacas e ovelhas."},
    "padaria":   {"nome": "Padaria", "preco": 450, "nivel": 3,
                  "desc": "Faça pão, bolo de cenoura e geleia de morango."},
    "irrigacao": {"nome": "Irrigação", "preco": 700, "nivel": 3,
                  "desc": "Rega todos os canteiros sozinha, todo dia."},
    "casa_reformada": {"nome": "Reforma da casa", "preco": 800, "nivel": 3,
                       "desc": "Você dorme melhor: +1 de energia por dia."},
    "laticinio": {"nome": "Laticínio", "preco": 600, "nivel": 4,
                  "desc": "Transforma leite em queijo."},
    "estufa":    {"nome": "Estufa", "preco": 900, "nivel": 4,
                  "desc": "Permite plantar e colher mesmo no inverno."},
}

# Enfeites: nao dao lucro, dao gosto. E o sumidouro de dinheiro que faltava
# depois que tudo util esta construido. Cada um aparece no cenario da fazenda e
# entra no patrimonio, entao o Concurso do fim do ano nota o capricho.
DECORACOES = {
    "flores":     {"nome": "Canteiro de flores", "preco": 220,
                   "desc": "Um tapete de flores do lado da casa."},
    "correio":    {"nome": "Caixa de correio nova", "preco": 260,
                   "desc": "Pintada à mão, com um girassol na tampa."},
    "espantalho": {"nome": "Espantalho", "preco": 300,
                   "desc": "Chapéu velho, sorriso torto e nenhum pássaro por perto."},
    "lampiao":    {"nome": "Lampião no caminho", "preco": 380,
                   "desc": "A trilha acesa quando a noite cai."},
    "balanco":    {"nome": "Balanço na árvore", "preco": 450,
                   "desc": "Para sentar e olhar a fazenda de longe."},
}

RECEITAS = {
    "racao_trigo": {"nome": "Ração de trigo", "precisa": {"trigo": 1}, "faz": ("racao", 5), "predio": "moinho"},
    "racao_milho": {"nome": "Ração de milho", "precisa": {"milho": 1}, "faz": ("racao", 8), "predio": "moinho"},
    "pao":    {"nome": "Pão caseiro", "precisa": {"trigo": 3}, "faz": ("pao", 1), "predio": "padaria"},
    "bolo":   {"nome": "Bolo de cenoura", "precisa": {"cenoura": 2, "ovo": 2}, "faz": ("bolo", 1), "predio": "padaria"},
    "geleia": {"nome": "Geleia de morango", "precisa": {"morango": 3}, "faz": ("geleia", 1), "predio": "padaria"},
    "queijo": {"nome": "Queijo", "precisa": {"leite": 2}, "faz": ("queijo", 1), "predio": "laticinio"},
    "sopa":     {"nome": "Sopa de legumes", "precisa": {"cenoura": 2, "milho": 1}, "faz": ("sopa", 1), "predio": "cozinha"},
    # so ovo de proposito: e a unica comida cozida que da para fazer no dia 1,
    # com a galinha que o jogo ja te da. Com leite, dependeria de vaca (nivel 3)
    "omelete":  {"nome": "Omelete", "precisa": {"ovo": 3}, "faz": ("omelete", 1), "predio": "cozinha"},
    "peixe_assado": {"nome": "Peixe assado", "precisa": {"tilapia": 2}, "faz": ("peixe_assado", 1), "predio": "cozinha"},
    "pao_de_milho": {"nome": "Pão de milho", "precisa": {"milho": 3}, "faz": ("pao_de_milho", 1), "predio": "padaria"},
    "torta":    {"nome": "Torta de abóbora", "precisa": {"abobora": 1, "ovo": 2, "trigo": 2}, "faz": ("torta", 1), "predio": "padaria"},
    "manteiga": {"nome": "Manteiga", "precisa": {"leite": 3}, "faz": ("manteiga", 1), "predio": "laticinio"},
    "iogurte":  {"nome": "Iogurte de morango", "precisa": {"leite": 2, "morango": 1}, "faz": ("iogurte", 1), "predio": "laticinio"},
    # so no inverno: a estacao em que nada cresce ganha o que so ela tem.
    # O bolo de fuba e o da carta da Vovo Cida, que abre o jogo.
    "bolo_fuba": {"nome": "Bolo de fubá da Vovó", "precisa": {"milho": 2, "ovo": 1, "leite": 1},
                  "faz": ("bolo_fuba", 1), "predio": "cozinha", "estacao": "Inverno"},
    "canjica":   {"nome": "Canjica", "precisa": {"milho": 3, "leite": 2},
                  "faz": ("canjica", 1), "predio": "cozinha", "estacao": "Inverno"},
}
LOTES_POR_ACAO = 3  # quantas receitas você faz gastando 1 de energia

# XP acumulado necessário para cada nível (índice = nível - 1)
XP_NIVEIS = [0, 40, 110, 220, 380, 600, 900, 1300, 1800, 2400, 3100, 4000]

CLIMA_POR_ESTACAO = {
    "Primavera": [("sol", 50), ("chuva", 35), ("nublado", 15)],
    "Verão":     [("sol", 65), ("chuva", 15), ("nublado", 10), ("tempestade", 10)],
    "Outono":    [("sol", 40), ("chuva", 30), ("nublado", 30)],
    "Inverno":   [("neve", 50), ("nublado", 30), ("sol", 20)],
}
NOME_CLIMA = {"sol": "Ensolarado", "chuva": "Chuvoso", "nublado": "Nublado",
              "tempestade": "Tempestade", "neve": "Nevando"}


def canteiro_preco(qtd_atual):
    """Preço do próximo canteiro extra."""
    return 120 + 60 * (qtd_atual - CANTEIROS_INICIAIS)
