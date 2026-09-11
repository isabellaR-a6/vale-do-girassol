"""Constantes, paleta de cores e dados do jogo (culturas, animais, construções)."""
import sys

# True quando o jogo roda no navegador (versão web gerada pelo pygbag)
WEB = sys.platform == "emscripten"

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

ENERGIA_BASE = 5
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
    "abobora_gigante": ("Abóbora gigante", 900),
}

CONSTRUCOES = {
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

RECEITAS = {
    "racao_trigo": {"nome": "Ração de trigo", "precisa": {"trigo": 1}, "faz": ("racao", 5), "predio": "moinho"},
    "racao_milho": {"nome": "Ração de milho", "precisa": {"milho": 1}, "faz": ("racao", 8), "predio": "moinho"},
    "pao":    {"nome": "Pão caseiro", "precisa": {"trigo": 3}, "faz": ("pao", 1), "predio": "padaria"},
    "bolo":   {"nome": "Bolo de cenoura", "precisa": {"cenoura": 2, "ovo": 2}, "faz": ("bolo", 1), "predio": "padaria"},
    "geleia": {"nome": "Geleia de morango", "precisa": {"morango": 3}, "faz": ("geleia", 1), "predio": "padaria"},
    "queijo": {"nome": "Queijo", "precisa": {"leite": 2}, "faz": ("queijo", 1), "predio": "laticinio"},
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
