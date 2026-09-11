"""Primitivas de desenho em pixel art reaproveitadas pelos cenários."""
import math
import random

import pygame

from config import COR

GRAMA = {
    "Primavera": ((106, 190, 48), (78, 158, 42), (150, 220, 80)),
    "Verão": ((96, 180, 44), (66, 142, 40), (140, 210, 70)),
    "Outono": ((178, 165, 72), (148, 120, 52), (210, 190, 100)),
    "Inverno": ((234, 240, 250), (196, 210, 230), (255, 255, 255)),
}
MORROS = {
    "Primavera": ((150, 205, 150), (100, 175, 90)),
    "Verão": ((130, 190, 130), (80, 160, 75)),
    "Outono": ((205, 170, 120), (185, 130, 80)),
    "Inverno": ((200, 212, 232), (170, 185, 210)),
}
FOLHAS = {
    "Primavera": ((78, 165, 60), (52, 125, 50), COR["rosa"]),
    "Verão": ((58, 150, 50), (38, 108, 42), None),
    "Outono": ((228, 128, 40), (180, 72, 40), COR["amarelo"]),
}


def lerp(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def cores_ceu(frac, noite, clima):
    dia = [(80, 170, 230), (110, 195, 240), (150, 215, 245), (200, 236, 250)]
    tarde = [(80, 90, 170), (170, 110, 150), (240, 150, 110), (255, 200, 130)]
    noturno = [(15, 20, 50), (25, 32, 70), (38, 48, 95), (55, 65, 120)]
    if noite:
        return noturno
    t = max(0.0, (frac - 0.45) / 0.55)
    base = [lerp(d, a, t * 0.9) for d, a in zip(dia, tarde)]
    if clima in ("chuva", "tempestade", "nublado", "neve"):
        cinza = [(115, 125, 145), (135, 145, 162), (158, 166, 180), (185, 190, 202)]
        k = {"tempestade": 0.75, "chuva": 0.55, "neve": 0.45, "nublado": 0.35}[clima]
        base = [lerp(b, c, k) for b, c in zip(base, cinza)]
    return base


def gradiente(s, cores, y0, y1):
    """Faixas de cor com uma transição pontilhada (dithering), bem pixel art."""
    w = s.get_width()
    n = len(cores)
    for i, cor in enumerate(cores):
        a = y0 + (y1 - y0) * i // n
        b = y0 + (y1 - y0) * (i + 1) // n
        s.fill(cor, (0, a, w, b - a))
        if i:
            ant = cores[i - 1]
            for x in range(0, w, 2):
                s.set_at((x, a), ant)
            for x in range(0, w, 4):
                s.set_at((x + 1, a + 1), ant)


def morro(s, cor, base_y, amp, freq, fase, ate_y):
    for x in range(s.get_width()):
        h = base_y - amp * (math.sin(x * freq + fase) * 0.6 + math.sin(x * freq * 2.3 + fase * 1.7) * 0.4)
        s.fill(cor, (x, int(h), 1, ate_y - int(h)))


def chao(s, estacao, y0, semente=3):
    base, escura, clara = GRAMA[estacao]
    s.fill(base, (0, y0, s.get_width(), s.get_height() - y0))
    rnd = random.Random(semente)
    for _ in range(140):
        x = rnd.randrange(s.get_width())
        y = rnd.randrange(y0 + 2, s.get_height())
        cor = escura if rnd.random() < 0.6 else clara
        s.set_at((x, y), cor)
        s.set_at((x + 1, y - 1), cor)
    if estacao in ("Primavera", "Verão"):
        for _ in range(26):
            x, y = rnd.randrange(s.get_width()), rnd.randrange(y0 + 4, s.get_height())
            s.set_at((x, y), rnd.choice([COR["amarelo"], COR["branco"], COR["rosa"]]))
    elif estacao == "Outono":
        for _ in range(30):
            x, y = rnd.randrange(s.get_width()), rnd.randrange(y0 + 4, s.get_height())
            s.set_at((x, y), rnd.choice([COR["laranja"], COR["vermelho"], COR["dourado"]]))


def arvore(s, x, base, estacao, tam=1.0, semente=0):
    r = int(9 * tam)
    s.fill(COR["madeira_esc"], (x - 2, base - int(14 * tam), 4, int(14 * tam)))
    s.fill(COR["madeira"], (x - 1, base - int(14 * tam), 1, int(14 * tam)))
    topo = base - int(16 * tam)
    if estacao == "Inverno":
        for dx, dy in ((-6, -8), (5, -10), (-3, -13), (3, -5)):
            pygame.draw.line(s, COR["madeira_esc"], (x, topo + 4), (x + dx, topo + dy))
        for dx, dy in ((-6, -9), (5, -11), (-3, -14)):
            s.fill(COR["branco"], (x + dx - 1, topo + dy, 3, 1))
        return
    esc, clara, flor = FOLHAS[estacao]
    for dx, dy, rr in ((0, -4, r), (-r * 2 // 3, 1, r * 3 // 4), (r * 2 // 3, 1, r * 3 // 4)):
        pygame.draw.circle(s, clara, (x + dx, topo + dy), rr)
    for dx, dy, rr in ((0, -1, r - 2), (-r // 2, 3, r // 2), (r // 2, 3, r // 2)):
        pygame.draw.circle(s, esc, (x + dx + 1, topo + dy + 1), rr)
    pygame.draw.circle(s, clara, (x - 2, topo - 5), r // 2)
    if flor:
        rnd = random.Random(semente + x)
        for _ in range(int(8 * tam)):
            s.set_at((x + rnd.randint(-r, r), topo + rnd.randint(-r, r // 2 + 2)), flor)


def nuvem(s, x, y, cor=(255, 255, 255), sombra=(215, 228, 240)):
    for dx, dy, r in ((0, 0, 5), (6, -3, 6), (13, 0, 5), (7, 2, 5)):
        pygame.draw.circle(s, sombra, (int(x) + dx, int(y) + dy + 1), r)
    for dx, dy, r in ((0, 0, 4), (6, -3, 5), (13, 0, 4), (7, 1, 4)):
        pygame.draw.circle(s, cor, (int(x) + dx, int(y) + dy), r)


def contorno_rect(s, cor_fundo, rect, cor_borda=None):
    cor_borda = cor_borda or COR["contorno"]
    pygame.draw.rect(s, cor_fundo, rect)
    pygame.draw.rect(s, cor_borda, rect, 1)


def telhado(s, cor, pontos, neve=False):
    pygame.draw.polygon(s, cor, pontos)
    pygame.draw.polygon(s, COR["contorno"], pontos, 1)
    if neve:  # os pontos vão da base esquerda, passando pelo topo, até a base direita
        pygame.draw.lines(s, COR["branco"], False, pontos, 2)


def fumaca(s, x, y, t, cor=(225, 225, 230)):
    for i in range(3):
        fase = (t * 0.5 + i / 3) % 1
        pygame.draw.circle(s, cor, (int(x + math.sin(fase * 6 + i) * 2 + fase * 6), int(y - fase * 16)),
                           1 + int(fase * 3))


def cerca_horizontal(s, x0, x1, y):
    s.fill(COR["madeira_clara"], (x0, y - 3, x1 - x0, 1))
    s.fill(COR["madeira_clara"], (x0, y - 1, x1 - x0, 1))
    for x in range(x0, x1 + 1, 8):
        s.fill(COR["madeira"], (x, y - 5, 2, 6))
        s.set_at((x, y - 5), COR["madeira_brilho"])


class Particulas:
    """Chuva, neve e vaga-lumes."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        rnd = random.Random(7)
        self.pts = [[rnd.uniform(0, w), rnd.uniform(0, h), rnd.uniform(0.7, 1.3), rnd.uniform(0, 6)]
                    for _ in range(90)]

    def chuva(self, s, dt, forte=False):
        n = 90 if forte else 60
        for p in self.pts[:n]:
            p[1] += 150 * p[2] * dt
            p[0] -= 40 * dt
            if p[1] > self.h:
                p[1] -= self.h
            if p[0] < 0:
                p[0] += self.w
            pygame.draw.line(s, (185, 210, 255), (int(p[0]), int(p[1])), (int(p[0]) - 1, int(p[1]) + 3))

    def neve(self, s, dt, t):
        for p in self.pts[:60]:
            p[1] += 16 * p[2] * dt
            if p[1] > self.h:
                p[1] -= self.h
            x = int(p[0] + math.sin(t + p[3]) * 3) % self.w
            s.set_at((x, int(p[1])), COR["branco"])
            if p[2] > 1.1:
                s.set_at((x + 1, int(p[1])), COR["branco"])

    def vagalumes(self, s, t, y0=20):
        for p in self.pts[:18]:
            x = int(p[0] + math.sin(t * 0.7 + p[3]) * 10) % self.w
            y = int(y0 + (p[1] % (self.h - y0)) + math.cos(t * 0.9 + p[3]) * 6)
            if math.sin(t * 3 + p[3] * 5) > 0.2:
                s.set_at((x, y), COR["amarelo"])
