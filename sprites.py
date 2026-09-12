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
# comidas novas emprestam o icone de um parente: sem isso elas cairiam no
# icone da racao, que e o padrao de quem nao tem
for _novo, _parecido in (("sopa", "cenoura"), ("omelete", "ovo"), ("peixe_assado", "trufa"),
                         ("pao_de_milho", "pao"), ("torta", "bolo"),
                         ("manteiga", "queijo"), ("iogurte", "geleia"),
                         ("bolo_fuba", "bolo"), ("canjica", "leite")):
    ITEM_ICONES[_novo] = ITEM_ICONES[_parecido]
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


# ------------------------------------------------ o retrato de quem está jogando
# As opções que a tela de criação oferece. Cada lista é (chave, nome que aparece).
PELES = [("clara", COR["pele"]), ("morena", (225, 175, 140)),
         ("parda", (200, 150, 115)), ("negra", COR["pele_esc"]), ("retinta", (120, 80, 55))]
CABELOS = [("preto", (45, 32, 30)), ("castanho", COR["madeira"]), ("loiro", COR["madeira_clara"]),
           ("ruivo", COR["laranja"]), ("grisalho", CINZA_CLARO), ("rosa", COR["rosa"]),
           ("roxo", COR["roxo_claro"]), ("azul", COR["agua_clara"])]
ESTILOS_CABELO = [("curto", "curto"), ("longo", "comprido"), ("coque", "coque"), ("careca", "raspado")]
ROUPAS = [("verde", COR["verde_ui"]), ("azul", COR["azul"]), ("vermelha", COR["vermelho_claro"]),
          ("amarela", COR["dourado"]), ("roxa", COR["roxo"]), ("rosa", COR["rosa"]),
          ("branca", COR["creme"]), ("marrom", COR["madeira"])]
CHAPEUS = [("nenhum", None), ("laço", "laco"), ("tiara", "tiara"), ("flor", "flor"),
           ("palha", "palha"), ("bandana", "bandana"), ("dino", "dino")]
BRINCOS = [("nenhum", None), ("dourado", COR["dourado"]), ("prata", COR["cinza"]),
           ("pérola", COR["branco"]), ("rubi", COR["vermelho_claro"])]
COLARES = [("nenhum", None), ("dourado", COR["dourado"]), ("prata", COR["cinza"]),
           ("contas", COR["roxo_claro"]), ("girassol", COR["amarelo"])]

APARENCIA_PADRAO = {"pele": "clara", "cabelo": "castanho", "estilo": "longo",
                    "roupa": "verde", "chapeu": "nenhum", "oculos": False,
                    "brinco": "nenhum", "colar": "nenhum"}


def _escolha(lista, chave, reserva=0):
    for k, v in lista:
        if k == chave:
            return v
    return lista[reserva][1]


def definir_jogador(ap):
    """Monta o retrato de quem está jogando a partir das escolhas dela.

    O retrato de cada personagem nasce de atributos, não de um desenho pronto —
    era só o jogador que não tinha um. O cache é por chave, então precisa cair
    quando a aparência muda, senão a tela mostra o rosto antigo.
    """
    ap = {**APARENCIA_PADRAO, **(ap or {})}
    RETRATOS["jogador"] = {
        "pele": _escolha(PELES, ap["pele"]),
        "cabelo": _escolha(CABELOS, ap["cabelo"], 1),
        "estilo": ap["estilo"] if ap["estilo"] in ("curto", "longo", "coque", "careca") else "curto",
        "roupa": _escolha(ROUPAS, ap["roupa"]),
        "fundo": COR["ceu_claro"],
        "oculos": bool(ap.get("oculos")),
    }
    chapeu = _escolha(CHAPEUS, ap.get("chapeu", "nenhum"))
    if chapeu:
        RETRATOS["jogador"]["chapeu"] = chapeu
    brinco = _escolha(BRINCOS, ap.get("brinco", "nenhum"))
    if brinco:
        RETRATOS["jogador"]["brinco"] = brinco
        RETRATOS["jogador"]["brinco_longo"] = ap.get("brinco") in ("pérola", "rubi")
    colar = _escolha(COLARES, ap.get("colar", "nenhum"))
    if colar:
        RETRATOS["jogador"]["colar"] = colar
        if ap.get("colar") == "girassol":
            RETRATOS["jogador"]["pingente"] = COR["madeira_esc"]
        elif ap.get("colar") == "contas":
            RETRATOS["jogador"]["pingente"] = COR["roxo"]
    for k in [c for c in _cache if c[0] == "retrato" and c[1] == "jogador"]:
        del _cache[k]


def cores_do_jogador(ap):
    """As três cores do bonequinho de corpo inteiro (cabelo, roupa, calça)."""
    ap = {**APARENCIA_PADRAO, **(ap or {})}
    return (_escolha(CABELOS, ap["cabelo"], 1), _escolha(ROUPAS, ap["roupa"]), COR["madeira_esc"])


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
        # O bloco ia ate y=12 e cobria o pescoco: uma faixa de cabelo cheia logo
        # abaixo do queixo le como barba. Agora ele para no queixo e o cabelo
        # cai pelos lados, deixando o pescoco aparecer.
        px(3, 3, 10, 9, cab)
        px(2, 11, 2, 3, cab)
        px(12, 11, 2, 3, cab)
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
    elif chapeu == "laco":
        px(10, 1, 2, 2, COR["rosa"])
        px(13, 1, 2, 2, COR["rosa"])
        px(12, 1, 1, 2, COR["vermelho_claro"])
    elif chapeu == "tiara":
        px(4, 1, 8, 1, COR["dourado"])
        px(3, 2, 1, 2, COR["dourado"])
        px(12, 2, 1, 2, COR["dourado"])
        px(7, 0, 2, 1, COR["agua_clara"])
    elif chapeu == "flor":
        px(11, 1, 3, 3, COR["amarelo"])
        px(12, 0, 1, 1, COR["amarelo"])
        px(12, 4, 1, 1, COR["amarelo"])
        px(12, 2, 1, 1, COR["madeira_esc"])
    elif chapeu == "dino":
        px(3, 1, 10, 3, COR["grama_esc"])
        px(4, 0, 8, 1, COR["grama_esc"])
        px(5, 0, 1, 1, COR["grama_clara"])
        px(8, 0, 1, 1, COR["grama_clara"])
        px(11, 0, 1, 1, COR["grama_clara"])
        px(2, 3, 1, 1, COR["grama_esc"])
        px(13, 3, 1, 1, COR["grama_esc"])
    elif chapeu == "capuz":
        px(3, 1, 10, 3, d["roupa"])
        px(4, 4, 8, 2, (80, 45, 95))
        px(6, 7, 1, 1, COR["amarelo"])
        px(9, 7, 1, 1, COR["amarelo"])
    # brinco e colar vao por ultimo, para aparecerem por cima do cabelo e do chapeu
    brinco = d.get("brinco")
    if brinco:
        px(3, 8, 1, 1, brinco)
        px(12, 8, 1, 1, brinco)
        if d.get("brinco_longo"):
            px(3, 9, 1, 1, brinco)
            px(12, 9, 1, 1, brinco)
    colar = d.get("colar")
    if colar:
        px(5, 13, 6, 1, colar)
        px(4, 12, 1, 1, colar)
        px(11, 12, 1, 1, colar)
        if d.get("pingente"):
            px(7, 14, 2, 1, d["pingente"])
    img = pygame.transform.scale(s, (16 * escala, 16 * escala))
    _cache[ck] = img
    return img
