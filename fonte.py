"""Fonte bitmap 5x7 feita à mão, com acentos do português e ícones embutidos.

Ícones no meio do texto: ¢ = moeda, ♥ = coração, ★ = estrela (XP), ⚡ = energia.
"""
import pygame

import sprites

_G = {
    "A": ".###. #...# #...# ##### #...# #...# #...#",
    "B": "####. #...# #...# ####. #...# #...# ####.",
    "C": ".###. #...# #.... #.... #.... #...# .###.",
    "D": "####. #...# #...# #...# #...# #...# ####.",
    "E": "##### #.... #.... ####. #.... #.... #####",
    "F": "##### #.... #.... ####. #.... #.... #....",
    "G": ".###. #...# #.... #.### #...# #...# .####",
    "H": "#...# #...# #...# ##### #...# #...# #...#",
    "I": "###.. .#... .#... .#... .#... .#... ###..",
    "J": "..### ...#. ...#. ...#. ...#. #..#. .##..",
    "K": "#...# #..#. #.#.. ##... #.#.. #..#. #...#",
    "L": "#.... #.... #.... #.... #.... #.... #####",
    "M": "#...# ##.## #.#.# #.#.# #...# #...# #...#",
    "N": "#...# #...# ##..# #.#.# #..## #...# #...#",
    "O": ".###. #...# #...# #...# #...# #...# .###.",
    "P": "####. #...# #...# ####. #.... #.... #....",
    "Q": ".###. #...# #...# #...# #.#.# #..#. .##.#",
    "R": "####. #...# #...# ####. #.#.. #..#. #...#",
    "S": ".#### #.... #.... .###. ....# ....# ####.",
    "T": "##### ..#.. ..#.. ..#.. ..#.. ..#.. ..#..",
    "U": "#...# #...# #...# #...# #...# #...# .###.",
    "V": "#...# #...# #...# #...# #...# .#.#. ..#..",
    "W": "#...# #...# #...# #.#.# #.#.# #.#.# .#.#.",
    "X": "#...# #...# .#.#. ..#.. .#.#. #...# #...#",
    "Y": "#...# #...# .#.#. ..#.. ..#.. ..#.. ..#..",
    "Z": "##### ....# ...#. ..#.. .#... #.... #####",
    "a": "..... ..... .###. ....# .#### #...# .####",
    "b": "#.... #.... ####. #...# #...# #...# ####.",
    "c": "..... ..... .#### #.... #.... #.... .####",
    "d": "....# ....# .#### #...# #...# #...# .####",
    "e": "..... ..... .###. #...# ##### #.... .###.",
    "f": "..##. .#... ###.. .#... .#... .#... .#...",
    "g": "..... ..... .#### #...# #...# .#### ....# .###.",
    "h": "#.... #.... ####. #...# #...# #...# #...#",
    "i": ".#... ..... ##... .#... .#... .#... ###..",
    "j": "...#. ..... ..##. ...#. ...#. ...#. #..#. .##..",
    "k": "#.... #.... #..#. #.#.. ##... #.#.. #..#.",
    "l": "##... .#... .#... .#... .#... .#... ###..",
    "m": "..... ..... ##.#. #.#.# #.#.# #.#.# #.#.#",
    "n": "..... ..... ####. #...# #...# #...# #...#",
    "o": "..... ..... .###. #...# #...# #...# .###.",
    "p": "..... ..... ####. #...# #...# ####. #.... #....",
    "q": "..... ..... .#### #...# #...# .#### ....# ....#",
    "r": "..... ..... #.##. ##..# #.... #.... #....",
    "s": "..... ..... .#### #.... .###. ....# ####.",
    "t": ".#... .#... ###.. .#... .#... .#... ..##.",
    "u": "..... ..... #...# #...# #...# #..## .##.#",
    "v": "..... ..... #...# #...# #...# .#.#. ..#..",
    "w": "..... ..... #...# #...# #.#.# #.#.# .#.#.",
    "x": "..... ..... #...# .#.#. ..#.. .#.#. #...#",
    "y": "..... ..... #...# #...# #...# .#### ....# .###.",
    "z": "..... ..... ##### ...#. ..#.. .#... #####",
    "0": ".###. #...# #..## #.#.# ##..# #...# .###.",
    "1": ".#... ##... .#... .#... .#... .#... ###..",
    "2": ".###. #...# ....# ...#. ..#.. .#... #####",
    "3": "####. ....# ....# .###. ....# ....# ####.",
    "4": "...#. ..##. .#.#. #..#. ##### ...#. ...#.",
    "5": "##### #.... ####. ....# ....# #...# .###.",
    "6": ".###. #.... #.... ####. #...# #...# .###.",
    "7": "##### ....# ...#. ..#.. .#... .#... .#...",
    "8": ".###. #...# #...# .###. #...# #...# .###.",
    "9": ".###. #...# #...# .#### ....# ....# .###.",
    ".": "..... ..... ..... ..... ..... ..... #....",
    ",": "..... ..... ..... ..... ..... .#... .#... #....",
    "!": "#.... #.... #.... #.... #.... ..... #....",
    "?": ".###. #...# ....# ...#. ..#.. ..... ..#..",
    ":": "..... ..... #.... ..... ..... #.... .....",
    ";": "..... ..... .#... ..... ..... .#... .#... #....",
    "-": "..... ..... ..... ###.. ..... ..... .....",
    "+": "..... ..#.. ..#.. ##### ..#.. ..#.. .....",
    "=": "..... ..... ####. ..... ####. ..... .....",
    "/": "....# ...#. ...#. ..#.. .#... .#... #....",
    "(": ".#... #.... #.... #.... #.... #.... .#...",
    ")": "#.... .#... .#... .#... .#... .#... #....",
    "'": "#.... #.... ..... ..... ..... ..... .....",
    '"': "#.#.. #.#.. ..... ..... ..... ..... .....",
    "%": "##..# ##..# ...#. ..#.. .#... #..## #..##",
    "*": "..... #.#.# .###. ##### .###. #.#.# .....",
    ">": "#.... .#... ..#.. ...#. ..#.. .#... #....",
    "<": "...#. ..#.. .#... #.... .#... ..#.. ...#.",
    "_": "..... ..... ..... ..... ..... ..... #####",
    "x": "..... ..... #...# .#.#. ..#.. .#.#. #...#",
    "·": "..... ..... ..... #.... ..... ..... .....",
    "º": ".#... #.#.. .#... ..... ..... ..... .....",
    "▶": "#.... ##... ###.. ####. ###.. ##... #....",
    "▼": "..... ..... ##### .###. ..#.. ..... .....",
    "■": "..... ####. ####. ####. ####. ..... .....",
    "□": "..... ####. #..#. #..#. ####. ..... .....",
}

_ACENTOS = {
    "agudo": ["...#.", "..#.."],
    "grave": [".#...", "..#.."],
    "circ": ["..#..", ".#.#."],
    "til": [".##.#", "#.##."],
}
_COMPOSTOS = {
    "á": ("a", "agudo"), "à": ("a", "grave"), "â": ("a", "circ"), "ã": ("a", "til"),
    "é": ("e", "agudo"), "ê": ("e", "circ"), "í": ("i", "agudo"),
    "ó": ("o", "agudo"), "ô": ("o", "circ"), "õ": ("o", "til"), "ú": ("u", "agudo"),
    "Á": ("A", "agudo"), "À": ("A", "grave"), "Â": ("A", "circ"), "Ã": ("A", "til"),
    "É": ("E", "agudo"), "Ê": ("E", "circ"), "Í": ("I", "agudo"),
    "Ó": ("O", "agudo"), "Ô": ("O", "circ"), "Õ": ("O", "til"), "Ú": ("U", "agudo"),
}

ICONES = {"¢": sprites.MOEDA, "♥": sprites.CORACAO, "★": sprites.ESTRELA, "⚡": sprites.RAIO}
TOPO = 2          # linhas reservadas para acentos de maiúsculas
ALTURA_LINHA = 12  # altura de uma linha de texto (escala 1)


def _montar():
    """Gera {char: (lista de pixels (x, y), largura)}; y já inclui o deslocamento TOPO."""
    brutos = {}
    for ch, s in _G.items():
        brutos[ch] = [list(linha) for linha in s.split()]
    for ch, (base, acento) in _COMPOSTOS.items():
        linhas = [list(l) for l in _G[base].split()]
        marca = [list(l) for l in _ACENTOS[acento]]
        if base in "iI" and acento == "agudo":
            marca = [list("..#.."), list(".#...")]  # o "i" é mais estreito
        if base.islower():
            linhas[0], linhas[1] = marca  # as 2 linhas de cima das minúsculas ficam livres
            brutos[ch] = linhas
        else:
            brutos[ch] = ("topo", marca + linhas)
    brutos["ç"] = [list(l) for l in "..... ..... .#### #.... #.... #.... .#### ..##.".split()]
    brutos["Ç"] = [list(l) for l in (_G["C"] + " ..#..").split()]

    glifos = {}
    for ch, linhas in brutos.items():
        desloc = TOPO
        if isinstance(linhas, tuple):
            linhas = linhas[1]
            desloc = 0
        pts = [(x, y + desloc) for y, l in enumerate(linhas) for x, c in enumerate(l) if c == "#"]
        if not pts:
            glifos[ch] = ([], 3)
            continue
        minx = min(p[0] for p in pts)
        maxx = max(p[0] for p in pts)
        if ch in "0123456789":
            minx, maxx = 0, 4  # números com largura fixa (bom para dinheiro)
        glifos[ch] = ([(x - minx, y) for x, y in pts], maxx - minx + 1)
    glifos[" "] = ([], 3)
    return glifos


class FontePixel:
    def __init__(self):
        self.glifos = _montar()
        self._cache = {}

    def _glifo(self, ch, cor, escala):
        chave = (ch, cor, escala)
        if chave not in self._cache:
            if ch in ICONES:
                img = sprites.sprite(ICONES[ch], escala=escala)
            else:
                pts, larg = self.glifos.get(ch, self.glifos["?"])
                img = pygame.Surface((larg * escala, ALTURA_LINHA * escala), pygame.SRCALPHA)
                for x, y in pts:
                    img.fill(cor, (x * escala, y * escala, escala, escala))
            self._cache[chave] = img
        return self._cache[chave]

    def largura_char(self, ch, escala=1):
        if ch in ICONES:
            return (len(ICONES[ch][0]) + 1) * escala
        return (self.glifos.get(ch, self.glifos["?"])[1] + 1) * escala

    def largura(self, texto, escala=1):
        return sum(self.largura_char(c, escala) for c in texto) - (escala if texto else 0)

    def desenhar(self, surf, texto, x, y, cor=(74, 44, 36), escala=1, sombra=None, centro=False, direita=False):
        if centro:
            x -= self.largura(texto, escala) // 2
        elif direita:
            x -= self.largura(texto, escala)
        if sombra:
            self.desenhar(surf, texto, x + escala, y + escala, sombra, escala)
        cx = x
        for ch in texto:
            img = self._glifo(ch, cor, escala)
            if ch in ICONES:
                surf.blit(img, (cx, y + (TOPO + 1) * escala + (7 - len(ICONES[ch])) * escala // 2))
            else:
                surf.blit(img, (cx, y))
            cx += self.largura_char(ch, escala)
        return cx

    def quebrar(self, texto, largura_max, escala=1):
        """Quebra o texto em linhas que caibam em largura_max (respeita \\n)."""
        linhas = []
        for paragrafo in texto.split("\n"):
            atual = ""
            for palavra in paragrafo.split(" "):
                teste = palavra if not atual else atual + " " + palavra
                if self.largura(teste, escala) <= largura_max:
                    atual = teste
                else:
                    if atual:
                        linhas.append(atual)
                    atual = palavra
            linhas.append(atual)
        return linhas
