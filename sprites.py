"""Pixel art feita em código: cada sprite é uma grade de caracteres.

Cada caractere vira uma cor da paleta ('.' é transparente). Assim o jogo
não depende de nenhuma imagem externa.
"""
import pygame

from config import COR

PALETA = {
    "o": COR["contorno"], "w": COR["branco"], "c": COR["creme"], "y": COR["amarelo"],
    "g": COR["dourado"], "r": COR["vermelho"], "R": COR["vermelho_claro"],
    "G": COR["grama"], "l": COR["grama_clara"], "d": COR["folha"], "O": COR["laranja"],
    "b": COR["madeira"], "B": COR["madeira_esc"], "n": COR["madeira_clara"],
    "p": COR["rosa"], "q": (215, 115, 145), "k": COR["cinza_esc"], "s": COR["cinza"],
    "v": COR["roxo"], "u": COR["agua_clara"], "P": COR["pele"],
}

_cache = {}


def sprite(grade, extra=None, escala=1, espelhar=False):
    """Converte uma grade de texto numa Surface (com cache)."""
    chave = (tuple(grade), tuple(sorted(extra.items())) if extra else None, escala, espelhar)
    if chave in _cache:
        return _cache[chave]
    pal = dict(PALETA)
    if extra:
        pal.update(extra)
    alt, larg = len(grade), max(len(linha) for linha in grade)
    surf = pygame.Surface((larg * escala, alt * escala), pygame.SRCALPHA)
    for y, linha in enumerate(grade):
        for x, ch in enumerate(linha):
            if ch != "." and ch in pal:
                surf.fill(pal[ch], (x * escala, y * escala, escala, escala))
    if espelhar:
        surf = pygame.transform.flip(surf, True, False)
    _cache[chave] = surf
    return surf


def desenhar(surf, grade, x, y, extra=None, escala=1, espelhar=False):
    surf.blit(sprite(grade, extra, escala, espelhar), (int(x), int(y)))


# ---------------------------------------------------------------- ícones da interface
MOEDA = [
    "..ggg..",
    ".gyyyg.",
    "gywyyyg",
    "gyyyyyg",
    "gyyyygg",
    ".gyygg.",
    "..ggg..",
]
CORACAO = [
    ".rr.rr.",
    "rwRrRRr",
    "rRRRRRr",
    ".rRRRr.",
    "..rRr..",
    "...r...",
]
ESTRELA = [
    "...g...",
    "..gyg..",
    "gggyggg",
    "gyywyyg",
    ".gyyyg.",
    ".gygyg.",
    "gg...gg",
]
RAIO = [
    "...gy",
    "..gy.",
    ".gyy.",
    "gyyyy",
    "..yg.",
    ".yg..",
    "yg...",
]
SETA = [
    "o....",
    "oo...",
    "ooo..",
    "oooo.",
    "ooo..",
    "oo...",
    "o....",
]

# ---------------------------------------------------------------- itens (8x8)
ITEM_ICONES = {
    "trigo": ["...y.y..", "..yyyyy.", ".yygyyg.", "..ygyg..", "...gg...", "...gg...", "..g..g..", ".g....g."],
    "cenoura": [".....GG.", "....GdG.", "...OOG..", "..OOOO..", ".OOOO...", ".OOO....", "OOO.....", "O......."],
    "milho": ["...yy...", "..ywyy..", "..yyyy..", "G.yyyy.G", "GGyyyyGG", ".GGyyGG.", "..GGGG..", "...GG..."],
    "tomate": ["...dG...", "..GdGG..", ".rrGrrr.", "rRwRRRRr", "rRRRRRRr", "rRRRRRRr", ".rRRRRr.", "..rrrr.."],
    "morango": ["..GdGG..", ".GGdGGG.", ".rRRRRr.", "rRyRRyRr", "rRRRyRRr", ".rRyRRr.", "..rRRr..", "...rr..."],
    "abobora": ["....B...", "...Bd...", ".OOOOOO.", "OOgOOgOO", "OwgOOgOO", "OOgOOgOO", ".OgOOgO.", "..OOOO.."],
    "ovo": ["........", "...oo...", "..owco..", ".owccco.", ".occcco.", ".occcno.", "..onno..", "...oo..."],
    "leite": ["...oo...", "..oBBo..", "..owwo..", ".owwwwo.", ".owuuwo.", ".owuuwo.", ".owwwwo.", "..oooo.."],
    "la": ["..oooo..", ".owcccco", "occwwcco", "occccwco", "ocwcccco", "occcwcco", ".occcco.", "..oooo.."],
    "trufa": ["........", "...BB...", "..BkBB..", ".BBBkBB.", ".BkBBBB.", ".BBBBkB.", "..BBBB..", "........"],
    "pao": ["........", "..oooo..", ".onnnno.", "onbnbnbo", "onnnnnno", "obbbbbbo", ".oooooo.", "........"],
    "bolo": ["...R....", "..cccc..", ".cwcccc.", "OOOOOOOO", "cccccccc", "OOOOOOOO", "bbbbbbbb", "........"],
    "geleia": ["..kkkk..", "..ssss..", ".oRRRRo.", ".oRwRRo.", ".oRcRRo.", ".oRRRRo.", ".oRRRRo.", "..oooo.."],
    "queijo": ["........", "......yo", "....yyyo", "..yyyyyo", "oyyygyyo", "oyyyyygo", "oygyyyyo", "oooooooo"],
    "amora": ["...GG...", "..vvGv..", ".vvvvvv.", ".vwvvvv.", ".vvvvvv.", "..vvvv..", "...vv...", "........"],
    "cogumelo": ["..rrrr..", ".rRwRRr.", "rRRRRwRr", "rrrrrrrr", "..cccc..", "..cccc..", "..cccc..", "........"],
    "racao": ["..o..o..", "...oo...", "..onno..", ".onnnno.", ".onGnno.", ".onnnno.", ".onnnno.", "..oooo.."],
}
_PEIXE = ["........", "..sss..s", ".sssssss", "sksssss.", ".sssssss", "..sss..s", "........", "........"]
ITEM_ICONES["lambari"] = _PEIXE
ITEM_ICONES["tilapia"] = _PEIXE
ITEM_ICONES["peixe_dourado"] = _PEIXE
ITEM_ICONES["abobora_gigante"] = ITEM_ICONES["abobora"]
_COR_PEIXE = {"lambari": {"s": COR["cinza"]}, "tilapia": {"s": (120, 160, 110)},
              "peixe_dourado": {"s": COR["dourado"]}}


def icone_item(item, escala=1):
    extra = _COR_PEIXE.get(item)
    return sprite(ITEM_ICONES.get(item, ITEM_ICONES["racao"]), extra, escala)


# ---------------------------------------------------------------- plantas no canteiro
BROTO = ["..l.l.", ".lGlG.", "..GG..", "..G..."]
MUDA = ["..l..l..", ".lGl.lG.", ".GGlGG..", "..GGG...", "...G....", "...G...."]
MURCHA = ["..b..b..", ".bnb.bn.", "..bnbb..", "...b...."]
MADURA = {
    "trigo": ["y...y...y", "yy.yyy.yy", "ygy.g.ygy", ".g..g..g.", ".g.gg..g.", "..gg.gg..", "...ggg...", "...gg...."],
    "cenoura": ["..l.l.", ".lGlGl", "lGGlGG", ".GdGd.", "..dd..", ".OOOO."],
    "milho": ["...l....", "..lG..l.", ".lG..lG.", "..GyyG..", ".lGyyGl.", "lG.yy.Gl", "...GG...", "..lGGl..", "...GG...", "...GG..."],
    "tomate": ["..lGGl..", ".lGrGGl.", "lGRRGrRl", ".GRwGRRG", "lGrRGGrl", ".lGGRRG.", "..lGGl..", "...GG..."],
    "morango": ["..l..l..", ".lGllGl.", "lGRGGRGl", "GRwRGRRG", ".rRGGrR.", "..GGGG.."],
    "abobora": ["...B.l..", "..lBGGl.", ".OOBOOO.", "OOgOOgOO", "OwgOOgOO", "OOgOOgOO", ".OOOOOO."],
}

# ---------------------------------------------------------------- animais (virados à direita)
ANIMAL_SPRITES = {
    "galinha": ["......rR..", ".....wwww.", ".....wwoyO", "w....wwwr.", "ww..wwwww.",
                "wwwwwcwww.", ".wwwccww..", "..wwwww...", "...O.O....", "...O.O...."],
    "vaca": ["............s.s.", "...........wwwww", ".wwwkkwwwwwwwoww", "wwwkkkwwwkkwwwpp",
             "wwwwkwwwwkkkwwpp", "wkwwwwwwwwwkww..", "wkkwwwwkkwwwww..", ".wwwwwwkkwwwww..",
             ".ww.ww....ww.ww.", ".kk.kk....kk.kk."],
    "porco": ["..........p..", "q.pppppppppp.", ".qpppppppppop", "ppppppppppppR",
              "pppppppppppp.", ".pppppppppp..", ".pp.pp..pp.pp", ".qq.qq..qq.qq"],
    "ovelha": ["..cwcwcc......", ".cwcwcwcc.kkk.", "cwcwcwcwcckkok", "wcwcwcwcwckkkk",
               "cwcwcwcwcc.kk.", "wcwcwcwcwc....", ".cwcwcwcw.....", "..k.k..k.k....", "..k.k..k.k...."],
}
CACHORRO = [".......b...", "......bnnb.", "b.....nnonk", ".b....nnnn.",
            ".nnnnnnnn..", ".nnnnnnnb..", ".n.n..n.n..", ".b.b..b.b.."]

PESSOA = ["..hhh..", ".hhhhh.", ".hPPPh.", "..PPP..", ".ttttt.", "ttttttt",
          "PtttttP", ".ttttt.", ".aa.aa.", ".aa.aa.", ".BB.BB."]


def pessoa(cabelo, roupa, calca):
    return sprite(PESSOA, {"h": cabelo, "t": roupa, "a": calca})


# ---------------------------------------------------------------- retratos 16x16 (gerados)
CINZA_CLARO = (215, 215, 220)
RETRATOS = {
    "vovo":     {"cabelo": CINZA_CLARO, "estilo": "coque", "oculos": True, "roupa": COR["roxo_claro"], "fundo": COR["rosa"]},
    "ze":       {"pele": COR["pele_esc"], "cabelo": CINZA_CLARO, "estilo": "curto", "barba": True,
                 "chapeu": "palha", "roupa": COR["azul"], "fundo": COR["grama_clara"]},
    "lucia":    {"cabelo": COR["madeira"], "estilo": "longo", "roupa": COR["vermelho_claro"], "fundo": COR["creme"]},
    "rosa":     {"cabelo": COR["laranja"], "estilo": "curto", "chapeu": "bandana",
                 "roupa": COR["madeira"], "fundo": COR["madeira_brilho"]},
    "viajante": {"pele": (200, 160, 130), "chapeu": "capuz", "roupa": COR["roxo"], "fundo": COR["noite_clara"]},
    "prefeito": {"cabelo": CINZA_CLARO, "estilo": "careca", "bigode": True, "chapeu": "cartola",
                 "roupa": COR["noite"], "fundo": COR["amarelo"]},
    "bia":      {"pele": COR["pele_esc"], "cabelo": (50, 35, 30), "estilo": "longo",
                 "roupa": COR["amarelo"], "fundo": COR["ceu_claro"]},
}


def retrato(chave, escala=3):
    if chave == "cachorro":
        base = pygame.Surface((16, 16))
        base.fill(COR["ceu_claro"])
        base.blit(sprite(CACHORRO), (3, 5))
        return pygame.transform.scale(base, (16 * escala, 16 * escala))
    ck = ("retrato", chave, escala)
    if ck in _cache:
        return _cache[ck]
    d = RETRATOS[chave]
    pele = d.get("pele", COR["pele"])
    cab = d.get("cabelo", COR["madeira"])
    s = pygame.Surface((16, 16))
    s.fill(d["fundo"])

    def px(x, y, w, h, cor):
        s.fill(cor, (x, y, w, h))

    chapeu = d.get("chapeu")
    if chapeu == "capuz":
        px(2, 1, 12, 15, d["roupa"])
        px(1, 4, 14, 12, d["roupa"])
    # roupa e pescoço
    px(2, 12, 12, 4, d["roupa"])
    px(1, 13, 14, 3, d["roupa"])
    px(6, 11, 4, 2, pele)
    # cabelo de trás
    estilo = d.get("estilo")
    if estilo == "longo":
        px(3, 3, 10, 10, cab)
    # rosto
    px(4, 3, 8, 9, pele)
    px(4, 3, 1, 1, cab if estilo != "careca" else d["fundo"])
    px(11, 3, 1, 1, cab if estilo != "careca" else d["fundo"])
    px(4, 11, 1, 1, d["fundo"] if estilo != "longo" else cab)
    px(11, 11, 1, 1, d["fundo"] if estilo != "longo" else cab)
    # cabelo da frente
    if estilo == "coque":
        px(6, 0, 4, 3, cab)
        px(4, 2, 8, 2, cab)
        px(4, 4, 1, 3, cab)
        px(11, 4, 1, 3, cab)
    elif estilo in ("curto", "longo"):
        px(3, 2, 10, 2, cab)
        px(4, 4, 3, 1, cab)
        px(3, 4, 1, 3, cab)
        px(12, 4, 1, 3, cab)
    elif estilo == "careca":
        px(4, 6, 1, 2, cab)
        px(11, 6, 1, 2, cab)
    # olhos, bochechas e boca
    olho = COR["contorno"]
    px(6, 7, 1, 1, olho)
    px(9, 7, 1, 1, olho)
    px(5, 8, 1, 1, COR["rosa"])
    px(10, 8, 1, 1, COR["rosa"])
    px(7, 9, 2, 1, COR["vermelho"])
    if d.get("barba"):
        px(4, 9, 8, 3, cab)
        px(5, 12, 6, 1, cab)
        px(7, 9, 2, 1, COR["vermelho"])
    if d.get("bigode"):
        px(5, 9, 6, 1, cab)
        px(5, 10, 1, 1, cab)
        px(10, 10, 1, 1, cab)
    if d.get("oculos"):
        px(5, 6, 3, 1, olho)
        px(8, 6, 3, 1, olho)
        px(5, 7, 1, 1, olho)
        px(10, 7, 1, 1, olho)
    # chapéus
    if chapeu == "palha":
        px(4, 0, 8, 3, COR["amarelo"])
        px(4, 2, 8, 1, COR["vermelho"])
        px(1, 3, 14, 1, COR["dourado"])
    elif chapeu == "bandana":
        px(3, 2, 10, 2, COR["verde_ui"])
        px(13, 3, 2, 2, COR["verde_ui"])
    elif chapeu == "cartola":
        px(5, 0, 6, 3, COR["contorno"])
        px(5, 2, 6, 1, COR["vermelho"])
        px(3, 3, 10, 1, COR["contorno"])
    elif chapeu == "capuz":
        px(3, 1, 10, 3, d["roupa"])
        px(4, 4, 8, 2, (80, 45, 95))
        px(6, 7, 1, 1, COR["amarelo"])
        px(9, 7, 1, 1, COR["amarelo"])
    img = pygame.transform.scale(s, (16 * escala, 16 * escala))
    _cache[ck] = img
    return img
