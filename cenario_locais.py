"""Outros lugares do vale: cidade, floresta, lago e o sítio do Seu Zé."""
import math
import random

import pygame

import desenho as d
import sprites
from config import ARTE_A, ARTE_L, COR
from fonte import FontePixel

_cache = {}
_fonte = None


def _placa(s, texto, cx, y, fundo=COR["madeira_clara"]):
    global _fonte
    if _fonte is None:
        _fonte = FontePixel()
    w = _fonte.largura(texto) + 4
    d.contorno_rect(s, fundo, (cx - w // 2, y, w, 10))
    _fonte.desenhar(s, texto, cx - w // 2 + 2, y - 1, COR["contorno"])


def _camada(chave, func):
    """Guarda a parte estática (transparente onde fica o céu)."""
    if chave not in _cache:
        s = pygame.Surface((ARTE_L, ARTE_A), pygame.SRCALPHA)
        func(s)
        _cache[chave] = s
    return _cache[chave]


# ---------------------------------------------------------------- cidade
def _cidade_estatica(s, estacao):
    neve = estacao == "Inverno"
    longe, perto = d.MORROS[estacao]
    d.morro(s, longe, 36, 5, 0.035, 0.4, 60)
    d.morro(s, perto, 44, 3, 0.06, 1.2, 62)
    s.fill((205, 188, 160), (0, 62, ARTE_L, ARTE_A - 62))
    for i, y in enumerate(range(64, ARTE_A, 5)):
        s.fill((182, 165, 138), (0, y, ARTE_L, 1))
        for x in range((i % 2) * 5, ARTE_L, 10):
            s.fill((182, 165, 138), (x, y, 1, 5))
    if neve:
        rnd = random.Random(4)
        for _ in range(40):
            s.fill(COR["branco"], (rnd.randrange(ARTE_L), rnd.randrange(64, ARTE_A), 3, 1))
    # Mercado
    d.contorno_rect(s, (242, 222, 182), (6, 38, 68, 26))
    d.telhado(s, COR["vermelho"], [(3, 39), (40, 24), (77, 39)], neve)
    for i in range(0, 68, 6):
        s.fill(COR["vermelho_claro"] if i % 12 else COR["branco"], (6 + i, 46, 6, 5))
        pygame.draw.circle(s, COR["vermelho_claro"] if i % 12 else COR["branco"], (9 + i, 51), 3)
    d.contorno_rect(s, COR["madeira"], (10, 56, 60, 8))
    for i, item in enumerate(["tomate", "cenoura", "milho", "abobora", "morango", "ovo", "trigo"]):
        s.blit(sprites.icone_item(item), (11 + i * 8, 51))
    _placa(s, "MERCADO", 40, 29)
    # Carpintaria
    d.contorno_rect(s, COR["madeira_clara"], (82, 36, 58, 28))
    for y in range(40, 64, 4):
        s.fill(COR["madeira"], (83, y, 56, 1))
    d.telhado(s, COR["madeira_esc"], [(79, 37), (111, 22), (143, 37)], neve)
    d.contorno_rect(s, COR["madeira_esc"], (100, 46, 20, 18))
    for i in range(3):
        d.contorno_rect(s, COR["madeira"], (142, 58 - i * 4, 14 - i * 3, 4))
    _placa(s, "CARPINTARIA", 111, 27)
    # Prefeitura com torre do relógio
    d.contorno_rect(s, (200, 200, 210), (150, 38, 64, 26))
    d.telhado(s, (80, 90, 120), [(146, 39), (182, 28), (218, 39)], neve)
    d.contorno_rect(s, (210, 210, 220), (174, 12, 16, 22))
    d.telhado(s, (80, 90, 120), [(172, 13), (182, 4), (192, 13)], neve)
    pygame.draw.circle(s, COR["branco"], (182, 21), 5)
    pygame.draw.circle(s, COR["contorno"], (182, 21), 5, 1)
    pygame.draw.line(s, COR["contorno"], (182, 21), (182, 18))
    pygame.draw.line(s, COR["contorno"], (182, 21), (184, 21))
    for x in (156, 168, 196, 208):
        s.fill(COR["branco"], (x, 42, 3, 22))
    d.contorno_rect(s, COR["madeira_esc"], (177, 48, 10, 16))
    # Café
    d.contorno_rect(s, (245, 190, 200), (222, 40, 58, 24))
    d.telhado(s, (90, 120, 190), [(219, 41), (251, 29), (283, 41)], neve)
    for i in range(0, 58, 6):
        s.fill(COR["agua_clara"] if i % 12 else COR["branco"], (222 + i, 45, 6, 4))
    d.contorno_rect(s, COR["agua_clara"], (228, 52, 10, 7))
    d.contorno_rect(s, COR["agua_clara"], (264, 52, 10, 7))
    d.contorno_rect(s, COR["madeira"], (246, 50, 10, 14))
    _placa(s, "CAFÉ", 251, 32, COR["creme"])
    d.arvore(s, 302, 66, estacao, 1.0, 9)
    # chafariz
    pygame.draw.ellipse(s, COR["cinza"], (140, 82, 40, 14))
    pygame.draw.ellipse(s, COR["contorno"], (140, 82, 40, 14), 1)
    pygame.draw.ellipse(s, COR["agua"] if not neve else (220, 230, 245), (143, 84, 34, 9))
    s.fill(COR["cinza"], (158, 76, 4, 10))


def cidade(s, e, t, dt, luzes, part, festa=False):
    s.blit(_camada(("cidade", e.estacao), lambda c: _cidade_estatica(c, e.estacao)), (0, 0))
    # bandeirinhas balançando, presas nos telhados (por cima das placas)
    for trecho in ((44, 22, 104, 20), (190, 15, 250, 28), (254, 29, 300, 44)):
        x0, y0, x1, y1 = trecho
        for i, x in enumerate(range(x0, x1, 6)):
            k = (x - x0) / max(1, x1 - x0)
            y = int(y0 + (y1 - y0) * k + math.sin(k * math.pi) * 3 + math.sin(t * 2 + x) * 0.6)
            s.set_at((x, y - 1), COR["contorno"])
            cor = [COR["vermelho_claro"], COR["amarelo"], COR["agua_clara"], COR["verde_ui"]][i % 4]
            pygame.draw.polygon(s, cor, [(x, y), (x + 5, y), (x + 2, y + 4)])
    if e.estacao != "Inverno":
        for i in range(6):
            fase = (t * 1.3 + i / 6) % 1
            s.set_at((160 + int(math.sin(i * 2) * fase * 8), int(76 - math.sin(fase * math.pi) * 8)), COR["agua_clara"])
    gente = [((60, 30, 20), COR["vermelho_claro"], COR["azul"], 64, 98),
             (COR["laranja"], COR["verde_ui"], COR["madeira"], 124, 96),
             ((40, 30, 30), COR["amarelo"], COR["roxo"], 206, 100),
             ((210, 210, 210), COR["azul"], COR["cinza_esc"], 262, 94)]
    for i, (cab, roupa, calca, x, y) in enumerate(gente):
        pulo = 1 if int(t * 2 + i) % 3 == 0 else 0
        s.blit(sprites.pessoa(cab, roupa, calca), (x, y - 11 - pulo))
    luzes += [(230, 54, 6, 3), (266, 54, 6, 3), (40, 40, 6, 3), (180, 50, 4, 3)]
    if festa:
        for x in range(10, 320, 14):
            y = 44 + int(math.sin(x * 0.08) * 3)
            luzes.append((x, y, 2, 2))


# ---------------------------------------------------------------- floresta
def _pinheiro(s, x, base, alt, estacao, cor=(40, 100, 60)):
    s.fill(COR["madeira_esc"], (x - 1, base - 4, 3, 4))
    for i in range(3):
        topo = base - 4 - alt + i * alt // 3
        larg = 4 + i * 3
        pygame.draw.polygon(s, cor, [(x - larg, topo + alt // 3 + 2), (x, topo), (x + larg, topo + alt // 3 + 2)])
        if estacao == "Inverno":
            pygame.draw.line(s, COR["branco"], (x - larg + 2, topo + alt // 3), (x, topo + 1))


def _floresta_estatica(s, estacao):
    neve = estacao == "Inverno"
    rnd = random.Random(11)
    for x in range(-4, ARTE_L + 8, 9):
        _pinheiro(s, x + rnd.randint(-2, 2), 52, rnd.randint(18, 26), estacao, (60, 120, 80))
    chao_cor = (70, 130, 55) if not neve else (230, 236, 248)
    if estacao == "Outono":
        chao_cor = (150, 120, 60)
    s.fill(chao_cor, (0, 52, ARTE_L, ARTE_A - 52))
    pygame.draw.polygon(s, (205, 175, 125) if not neve else (210, 215, 228),
                        [(150, 52), (170, 52), (200, ARTE_A), (120, ARTE_A)])
    for x in range(0, ARTE_L, 16):
        _pinheiro(s, x + rnd.randint(-3, 3), 60 + rnd.randint(0, 4), rnd.randint(22, 30), estacao)
    for x in (18, 62, 262, 304):
        d.arvore(s, x, 96, estacao, 1.5, x)
    for x, y in ((40, 92), (100, 80), (228, 86), (284, 98), (130, 96)):
        if not neve:
            s.blit(sprites.sprite(sprites.ITEM_ICONES["cogumelo"]), (x, y))
    for x, y in ((80, 96), (214, 100)):
        pygame.draw.circle(s, COR["folha"], (x, y), 6)
        for k in range(5):
            s.set_at((x - 4 + k * 2, y - 2 + (k % 2) * 3), COR["roxo_claro"] if not neve else COR["branco"])


def floresta(s, e, t, dt, luzes, part):
    s.blit(_camada(("floresta", e.estacao), lambda c: _floresta_estatica(c, e.estacao)), (0, 0))
    for i in range(3):  # raios de luz entre as árvores
        x = 90 + i * 60
        for k in range(0, 50, 2):
            if (k // 2 + i) % 3 == 0:
                s.set_at((x + k // 2, 10 + k), (255, 250, 200))
    if e.clima not in ("chuva", "tempestade", "neve"):
        for i in range(3):  # borboletas
            x = int(140 + math.sin(t * 0.6 + i * 2) * 60)
            y = int(70 + math.cos(t * 0.9 + i) * 12)
            cor = [COR["amarelo"], COR["rosa"], COR["branco"]][i]
            if int(t * 8 + i) % 2:
                s.fill(cor, (x - 1, y, 3, 1))
            else:
                s.set_at((x - 1, y - 1), cor)
                s.set_at((x + 1, y - 1), cor)
    part.vagalumes(s, t + 5, 60)


# ---------------------------------------------------------------- lago
def _lago_estatico(s, estacao):
    gelo = estacao == "Inverno"
    longe, perto = d.MORROS[estacao]
    d.morro(s, longe, 38, 6, 0.04, 2.0, 50)
    d.chao(s, estacao, 48, semente=8)
    agua = [(90, 150, 230), (70, 125, 210), (55, 105, 190)] if not gelo else \
           [(215, 232, 248), (195, 218, 242), (180, 205, 235)]
    pygame.draw.ellipse(s, agua[0], (-40, 54, 400, 90))
    pygame.draw.ellipse(s, agua[1], (-20, 64, 360, 80))
    pygame.draw.ellipse(s, agua[2], (10, 78, 300, 60))
    if gelo:
        for x0, y0, x1, y1 in ((60, 70, 90, 80), (90, 80, 84, 92), (200, 66, 230, 76), (230, 76, 250, 72)):
            pygame.draw.line(s, COR["branco"], (x0, y0), (x1, y1))
    for x in range(260, 320, 3):  # juncos
        h = 10 + (x * 7) % 8
        pygame.draw.line(s, COR["folha"], (x, 70), (x + 1, 70 - h))
        s.fill(COR["madeira"], (x + 1, 70 - h, 1, 3))
    if not gelo:
        for x, y in ((210, 90), (236, 84), (120, 96)):
            pygame.draw.ellipse(s, COR["grama_esc"], (x, y, 10, 4))
            s.set_at((x + 4, y + 1), COR["rosa"])
    # píer
    s.fill(COR["madeira"], (0, 72, 96, 8))
    for x in range(0, 96, 6):
        s.fill(COR["madeira_esc"], (x, 72, 1, 8))
    s.fill(COR["madeira_brilho"], (0, 72, 96, 1))
    for x in (4, 40, 90):
        s.fill(COR["madeira_esc"], (x, 80, 3, 8))
    d.arvore(s, 18, 56, estacao, 1.0, 5)


def lago(s, e, t, dt, luzes, part):
    s.blit(_camada(("lago", e.estacao), lambda c: _lago_estatico(c, e.estacao)), (0, 0))
    if e.estacao == "Inverno":
        return
    for i in range(10):
        x = int((i * 37 + t * 6) % 280) + 20
        y = 70 + (i * 13) % 30
        s.fill((170, 210, 255), (x, y, 4 + i % 3, 1))
    fase = (t % 6) / 1.2
    if fase < 1:  # peixe pulando
        x = 170 + fase * 24
        y = 82 - math.sin(fase * math.pi) * 12
        s.blit(sprites.icone_item("tilapia"), (int(x), int(y)))
    # linha de pesca saindo do píer
    pygame.draw.line(s, COR["madeira_esc"], (84, 70), (104, 56))
    pygame.draw.line(s, (230, 230, 230), (104, 56), (118, 84 + int(math.sin(t * 2) * 1)))
    s.fill(COR["vermelho"], (117, 83 + int(math.sin(t * 2) * 1), 3, 2))


# ---------------------------------------------------------------- sítio do Seu Zé
def _vizinho_estatico(s, estacao):
    neve = estacao == "Inverno"
    longe, perto = d.MORROS[estacao]
    d.morro(s, longe, 36, 6, 0.03, 3.0, 50)
    d.morro(s, perto, 44, 3, 0.05, 0.5, 50)
    d.chao(s, estacao, 48, semente=12)
    d.contorno_rect(s, (120, 160, 220), (24, 42, 50, 24))
    for y in range(46, 66, 4):
        s.fill((100, 140, 200), (25, y, 48, 1))
    d.telhado(s, COR["madeira_esc"], [(20, 43), (49, 26), (78, 43)], neve)
    d.contorno_rect(s, COR["branco"], (32, 48, 10, 8))
    d.contorno_rect(s, COR["madeira"], (52, 50, 9, 16))
    s.fill(COR["madeira_clara"], (18, 65, 62, 2))
    d.cerca_horizontal(s, 0, ARTE_L, 100)


def vizinho(s, e, t, dt, luzes, part):
    s.blit(_camada(("vizinho", e.estacao), lambda c: _vizinho_estatico(c, e.estacao)), (0, 0))
    if e.estacao != "Inverno":
        seco = e.estacao == "Outono"
        for fila, y in enumerate((60, 74, 90)):
            for x in range(100 + fila * 5, 320, 14):
                balanco = int(math.sin(t * 1.5 + x * 0.1) * 1.5)
                alt = 12 + fila * 3
                pygame.draw.line(s, COR["folha"], (x, y), (x + balanco, y - alt))
                s.fill(COR["grama"], (x - 3, y - alt // 2, 3, 2))
                cx, cy = x + balanco, y - alt - 2
                petala = COR["dourado"] if seco else COR["amarelo"]
                pygame.draw.circle(s, petala, (cx, cy), 3 + fila // 2)
                pygame.draw.circle(s, COR["madeira_esc"], (cx, cy), 1 + fila // 2)
    s.blit(sprites.pessoa((215, 215, 220), COR["azul"], COR["madeira"]), (84, 56))
    s.fill(COR["amarelo"], (83, 55, 9, 2))
    luzes.append((34, 50, 6, 4))


def desenhar(local, s, e, t, dt, luzes, part):
    if local in ("cidade", "festa"):
        cidade(s, e, t, dt, luzes, part, festa=local == "festa")
    elif local == "floresta":
        floresta(s, e, t, dt, luzes, part)
    elif local == "lago":
        lago(s, e, t, dt, luzes, part)
    elif local == "vizinho":
        vizinho(s, e, t, dt, luzes, part)
