"""Cenário principal: a fazenda (de dia, de noite e na tela de título)."""
import math
import random

import pygame

import cenario_locais as locais
import desenho as d
import sprites
from config import ANIMAIS, ARTE_A, ARTE_L, COR, CULTURAS, ESCALA_ARTE

HORIZONTE = 46
PLOTS = [(74 + (i % 4) * 28, 64 + (i // 4) * 18) for i in range(8)]
CURRAL = (196, 60, 258, 100)  # x0, y0, x1, y1


# ---------------------------------------------------------------- construções da fazenda
def casa(s, x, base, neve, reformada):
    d.contorno_rect(s, COR["creme"], (x, base - 18, 38, 18))
    for y in range(base - 14, base, 4):
        s.fill(COR["pergaminho_esc"], (x + 1, y, 36, 1))
    d.telhado(s, COR["vermelho"], [(x - 4, base - 17), (x + 19, base - 34), (x + 42, base - 17)], neve)
    for i in range(3):
        pygame.draw.line(s, COR["vermelho_claro"], (x + 4 + i * 5, base - 20 - i * 4), (x + 34 - i * 5, base - 20 - i * 4))
    d.contorno_rect(s, (150, 110, 100), (x + 28, base - 34, 5, 10))
    d.contorno_rect(s, COR["madeira"] if not reformada else COR["azul"], (x + 6, base - 13, 8, 13))
    s.set_at((x + 12, base - 6), COR["amarelo"])
    if reformada:
        s.fill(COR["madeira_clara"], (x - 3, base - 1, 44, 2))
        for i in range(4):
            s.set_at((x + 22 + i * 3, base - 4), [COR["rosa"], COR["amarelo"], COR["vermelho_claro"], COR["branco"]][i])
        s.fill(COR["verde_ui_esc"], (x + 21, base - 3, 12, 2))


def celeiro(s, x, base, neve):
    d.contorno_rect(s, COR["vermelho"], (x, base - 24, 48, 24))
    for xx in range(x + 4, x + 48, 6):
        s.fill((150, 38, 42), (xx, base - 23, 1, 22))
    pts = [(x - 3, base - 23), (x + 6, base - 35), (x + 24, base - 42), (x + 42, base - 35), (x + 51, base - 23)]
    d.telhado(s, (120, 36, 40), pts, neve)
    pygame.draw.lines(s, COR["branco"] if not neve else COR["cinza"], False, pts, 1)
    porta = pygame.Rect(x + 14, base - 17, 20, 17)
    s.fill((150, 38, 42), porta)
    pygame.draw.rect(s, COR["branco"], porta, 1)
    pygame.draw.line(s, COR["branco"], porta.topleft, (porta.right - 1, porta.bottom - 1))
    pygame.draw.line(s, COR["branco"], (porta.right - 1, porta.top), (porta.left, porta.bottom - 1))
    s.fill(COR["branco"], (x + 20, base - 34, 9, 7))
    s.fill(COR["amarelo"], (x + 21, base - 33, 7, 5))
    s.fill(COR["dourado"], (x + 21, base - 30, 7, 2))


def caixa_dagua(s, x, base):
    for dx in (1, 8):
        s.fill(COR["madeira_esc"], (x + dx, base - 14, 1, 14))
    pygame.draw.line(s, COR["madeira"], (x + 1, base - 12), (x + 8, base - 2))
    d.contorno_rect(s, COR["azul"], (x - 1, base - 24, 12, 10))
    s.fill(COR["agua_clara"], (x + 1, base - 22, 3, 6))


def moinho_torre(s, x, base, neve):
    pygame.draw.polygon(s, COR["pergaminho"], [(x - 6, base), (x - 3, base - 26), (x + 3, base - 26), (x + 6, base)])
    pygame.draw.polygon(s, COR["contorno"], [(x - 6, base), (x - 3, base - 26), (x + 3, base - 26), (x + 6, base)], 1)
    s.fill(COR["madeira"], (x - 1, base - 6, 3, 6))
    d.telhado(s, COR["madeira"], [(x - 5, base - 25), (x, base - 32), (x + 5, base - 25)], neve)


def moinho_pas(s, x, base, t):
    cx, cy = x, base - 27
    for i in range(4):
        ang = t * 1.4 + i * math.pi / 2
        fx, fy = cx + math.cos(ang) * 15, cy + math.sin(ang) * 15
        pygame.draw.line(s, COR["madeira_esc"], (cx, cy), (fx, fy), 1)
        px, py = cx + math.cos(ang) * 9, cy + math.sin(ang) * 9
        qx, qy = math.cos(ang + 1.57) * 2.5, math.sin(ang + 1.57) * 2.5
        pygame.draw.polygon(s, COR["creme"], [(px, py), (fx, fy), (fx + qx, fy + qy), (px + qx, py + qy)])
    s.fill(COR["contorno"], (cx - 1, cy - 1, 3, 3))


def padaria(s, x, base, neve):
    d.contorno_rect(s, COR["madeira_brilho"], (x, base - 14, 22, 14))
    d.telhado(s, COR["laranja"], [(x - 2, base - 13), (x + 11, base - 22), (x + 24, base - 13)], neve)
    for i in range(0, 22, 4):
        s.fill(COR["vermelho_claro"] if i % 8 else COR["branco"], (x + i, base - 12, 4, 3))
    d.contorno_rect(s, COR["madeira"], (x + 8, base - 8, 6, 8))
    s.fill(COR["amarelo"], (x + 2, base - 7, 4, 3))
    d.contorno_rect(s, (150, 110, 100), (x + 16, base - 24, 4, 7))


def estabulo(s, x, base, neve):
    d.contorno_rect(s, COR["madeira"], (x, base - 16, 32, 16))
    for xx in range(x + 3, x + 32, 4):
        s.fill(COR["madeira_esc"], (xx, base - 15, 1, 14))
    d.telhado(s, COR["madeira_esc"], [(x - 3, base - 15), (x + 16, base - 25), (x + 35, base - 15)], neve)
    d.contorno_rect(s, (60, 35, 30), (x + 11, base - 11, 10, 11))
    s.fill(COR["amarelo"], (x + 13, base - 3, 6, 3))


def laticinio(s, x, base, neve):
    d.contorno_rect(s, COR["branco"], (x, base - 14, 20, 14))
    d.telhado(s, COR["azul"], [(x - 2, base - 13), (x + 10, base - 21), (x + 22, base - 13)], neve)
    d.contorno_rect(s, COR["agua_clara"], (x + 3, base - 9, 5, 5))
    d.contorno_rect(s, COR["azul"], (x + 12, base - 9, 5, 9))
    s.blit(sprites.icone_item("leite"), (x + 6, base - 21))


def estufa(s, x, base, neve):
    pontos = [(x, base), (x, base - 12), (x + 12, base - 20), (x + 24, base - 12), (x + 24, base)]
    pygame.draw.polygon(s, (175, 225, 235), pontos)
    for xx in range(x + 4, x + 24, 5):
        s.fill(COR["grama"], (xx, base - 5, 3, 4))
        s.set_at((xx + 1, base - 6), COR["vermelho_claro"])
    pygame.draw.polygon(s, COR["branco"], pontos, 1)
    for xx in range(x + 6, x + 24, 6):
        pygame.draw.line(s, COR["branco"], (xx, base), (xx, base - 12 - min(xx - x, x + 24 - xx) * 8 // 12))
    s.fill((215, 245, 250), (x + 3, base - 12, 2, 5))
    if neve:
        pygame.draw.lines(s, COR["branco"], False, pontos[1:4], 2)


def galinheiro(s, x, base, grande, neve):
    w = 22 if grande else 15
    d.contorno_rect(s, COR["madeira_clara"], (x, base - 9, w, 9))
    d.telhado(s, COR["vermelho"], [(x - 2, base - 8), (x + w // 2, base - 15), (x + w + 1, base - 8)], neve)
    s.fill(COR["contorno"], (x + 3, base - 6, 4, 6))
    pygame.draw.line(s, COR["madeira"], (x + 3, base), (x - 2, base + 4))


# ---------------------------------------------------------------- canteiros e animais
def enfeites(s, e, t):
    """Os enfeites comprados na carpintaria.

    Ficam na parte animada e nao no fundo em cache: assim o enfeite novo aparece
    na hora, sem depender de a chave do cache mudar.
    """
    tem = e.decoracoes
    if "flores" in tem:
        # y abaixo de ~100 fica atras da caixa de dialogo e nao se ve
        for i, x in enumerate(range(6, 42, 5)):
            y = 88 + (i % 2)
            s.fill(COR["folha"], (x + 1, y + 2, 1, 3))
            cor = (COR["vermelho_claro"], COR["amarelo"], COR["rosa"], COR["roxo_claro"])[i % 4]
            s.fill(cor, (x, y, 3, 2))
            s.fill(COR["creme"], (x + 1, y, 1, 1))
    if "correio" in tem:
        s.fill(COR["madeira_esc"], (48, 96, 2, 10))
        s.fill(COR["contorno"], (43, 89, 12, 8))
        s.fill(COR["verde_ui"], (44, 90, 10, 6))
        s.fill(COR["dourado"], (48, 92, 2, 2))
        s.fill(COR["madeira_esc"], (48, 92, 1, 1))
    if "lampiao" in tem:
        s.fill(COR["contorno"], (68, 88, 2, 16))
        s.fill(COR["contorno"], (65, 82, 8, 7))
        aceso = COR["amarelo"] if int(t * 2) % 8 else COR["dourado"]
        s.fill(aceso, (66, 83, 6, 5))
        s.fill(COR["creme"], (67, 84, 2, 2))
    if "espantalho" in tem:
        s.fill(COR["madeira_esc"], (183, 80, 2, 14))
        s.fill(COR["madeira_esc"], (176, 84, 16, 2))
        s.fill(COR["pergaminho_esc"], (179, 74, 10, 7))
        s.fill(COR["contorno"], (181, 76, 1, 1))
        s.fill(COR["contorno"], (186, 76, 1, 1))
        s.fill(COR["vermelho"], (182, 78, 4, 1))
        s.fill(COR["dourado"], (177, 70, 14, 4))
        s.fill(COR["vermelho_claro"], (177, 72, 14, 1))
    if "balanco" in tem:
        balanca = int(t * 1.5) % 2
        x = 44 + balanca
        s.fill(COR["madeira_clara"], (x, 56, 1, 8))
        s.fill(COR["madeira_clara"], (x + 8, 56, 1, 8))
        s.fill(COR["madeira"], (x - 1, 64, 11, 2))


def canteiro(s, i, c, e, t):
    x, y = PLOTS[i]
    congelado = e.estacao == "Inverno" and not e.tem("estufa")
    if c is None:  # canteiro ainda não comprado
        for k in range(0, 24, 4):
            s.set_at((x + k, y), d.GRAMA[e.estacao][1])
            s.set_at((x + k, y + 12), d.GRAMA[e.estacao][1])
        return
    solo = COR["terra_molhada"] if c["regado"] else COR["terra"]
    d.contorno_rect(s, solo, (x, y, 24, 13), COR["terra_esc"])
    for k in (3, 7, 10):
        s.fill(COR["terra_esc"], (x + 2, y + k, 20, 1))
    if congelado and not c["cultura"]:
        s.fill((235, 240, 250), (x + 1, y + 1, 22, 5))
        return
    if not c["cultura"]:
        return
    total = CULTURAS[c["cultura"]]["dias"]
    for px in (x + 7, x + 17):
        if c["morto"]:
            g = sprites.MURCHA
        elif c["dias"] >= total:
            g = sprites.MADURA[c["cultura"]]
        elif c["dias"] == 0:
            s.fill(COR["madeira_esc"], (px - 1, y + 6, 1, 1))
            s.fill(COR["madeira_esc"], (px + 1, y + 8, 1, 1))
            continue
        elif c["dias"] / total < 0.5:
            g = sprites.BROTO
        else:
            g = sprites.MUDA
        img = sprites.sprite(g)
        s.blit(img, (px - img.get_width() // 2, y + 11 - img.get_height()))
    if e.maduro(c) and int(t * 3 + i) % 3 == 0:
        s.set_at((x + 3 + (i * 7) % 18, y + 1), COR["branco"])
    elif not c["regado"] and not c["morto"] and not e.maduro(c) and int(t * 2) % 2 == 0:
        s.fill(COR["agua_clara"], (x + 11, y - 5, 2, 3))
        s.set_at((x + 11, y - 6), COR["agua_clara"])


class Rebanho:
    """Faz os animais passearem pelo curral."""

    def __init__(self):
        self.pos = {}

    def atualizar(self, e, dt):
        x0, y0, x1, y1 = CURRAL
        vivos = set()
        for i, a in enumerate(e.animais):
            chave = (i, a["tipo"])
            vivos.add(chave)
            w = len(sprites.ANIMAL_SPRITES[a["tipo"]][0])
            if chave not in self.pos:
                self.pos[chave] = {"x": random.uniform(x0 + 22, x1 - w), "y": random.uniform(y0 + 16, y1 - 3),
                                   "tx": None, "ty": None, "espera": random.uniform(0, 2), "dir": 1}
            p = self.pos[chave]
            if p["tx"] is None:
                p["espera"] -= dt
                if p["espera"] <= 0:
                    p["tx"] = random.uniform(x0 + 6 + w / 2, x1 - w / 2 - 2)
                    p["ty"] = random.uniform(y0 + 16, y1 - 3)
            else:
                vel = 14 if a["tipo"] == "galinha" else 7
                dx, dy = p["tx"] - p["x"], p["ty"] - p["y"]
                dist = math.hypot(dx, dy)
                if dist < 1:
                    p["tx"] = None
                    p["espera"] = random.uniform(1, 4)
                else:
                    p["x"] += dx / dist * vel * dt
                    p["y"] += dy / dist * vel * dt
                    p["dir"] = 1 if dx > 0 else -1
        for k in list(self.pos):
            if k not in vivos:
                del self.pos[k]

    def desenhar(self, s, e, t):
        ordem = sorted(((self.pos[(i, a["tipo"])], a) for i, a in enumerate(e.animais)
                        if (i, a["tipo"]) in self.pos), key=lambda pa: pa[0]["y"])
        for p, a in ordem:
            img = sprites.sprite(sprites.ANIMAL_SPRITES[a["tipo"]], espelhar=p["dir"] < 0)
            pulo = 1 if p["tx"] is not None and int(t * 8) % 2 else 0
            x = int(p["x"] - img.get_width() / 2)
            y = int(p["y"] - img.get_height()) - pulo
            s.blit(img, (x, y))
            if a["pronto"]:
                by = y - 12 + int(math.sin(t * 4) * 1.5)
                bx = int(p["x"]) - 5
                pygame.draw.rect(s, COR["branco"], (bx, by, 11, 10))
                pygame.draw.rect(s, COR["contorno"], (bx, by, 11, 10), 1)
                s.set_at((bx + 5, by + 10), COR["contorno"])
                s.blit(sprites.icone_item(ANIMAIS[a["tipo"]]["produto"]), (bx + 1, by + 1))


# ---------------------------------------------------------------- a cena completa
class Cenario:
    def __init__(self):
        self.surf = pygame.Surface((ARTE_L, ARTE_A))
        self.cache = {}
        self.rebanho = Rebanho()
        self.part = d.Particulas(ARTE_L, ARTE_A)
        rnd = random.Random(1)
        self.nuvens = [[rnd.uniform(0, ARTE_L), rnd.uniform(6, 26), rnd.uniform(2, 5)] for _ in range(5)]
        self.estrelas = [(rnd.randrange(ARTE_L), rnd.randrange(0, 34), rnd.uniform(0, 6)) for _ in range(40)]
        self.relampago = 0.0
        self.fogos = []

    def _ceu(self, s, e, frac, noite, com_sol=True):
        d.gradiente(s, d.cores_ceu(frac, noite, e.clima), 0, HORIZONTE + 4)
        if noite:
            pygame.draw.circle(s, (250, 245, 215), (262, 16), 6)
            pygame.draw.circle(s, d.cores_ceu(0, True, "sol")[0], (265, 14), 5)
        elif com_sol and e.clima in ("sol", "nublado"):
            sx = int(30 + frac * 250)
            sy = int(12 + (frac - 0.5) ** 2 * 50)
            cor = d.lerp((255, 240, 120), (255, 170, 90), frac)
            pygame.draw.circle(s, d.lerp(cor, (255, 255, 255), 0.4), (sx, sy), 8)
            pygame.draw.circle(s, cor, (sx, sy), 6)

    def _fundo_fazenda(self, e, frac, noite):
        chave = ("fazenda", e.estacao, e.clima, round(frac, 2), noite, tuple(sorted(e.construcoes)))
        if chave in self.cache:
            return self.cache[chave]
        if len(self.cache) > 40:
            self.cache.clear()
        s = pygame.Surface((ARTE_L, ARTE_A))
        neve = e.estacao == "Inverno"
        self._ceu(s, e, frac, noite)
        longe, perto = d.MORROS[e.estacao]
        d.morro(s, longe, 34, 6, 0.03, 1.0, HORIZONTE + 2)
        d.morro(s, perto, 42, 4, 0.05, 2.5, HORIZONTE + 4)
        d.chao(s, e.estacao, HORIZONTE)
        # trilha de terra saindo da casa
        cor_trilha = (215, 190, 140) if not neve else (220, 225, 235)
        pygame.draw.polygon(s, cor_trilha, [(18, 58), (28, 58), (44, ARTE_A), (22, ARTE_A)])
        d.arvore(s, 52, 52, e.estacao, 0.9, 1)
        d.arvore(s, 250, 50, e.estacao, 0.7, 2)
        d.arvore(s, 316, 60, e.estacao, 1.1, 3)
        if e.tem("irrigacao"):
            caixa_dagua(s, 60, 58)
        if e.tem("moinho"):
            moinho_torre(s, 84, 58, neve)
        if e.tem("padaria"):
            padaria(s, 100, 57, neve)
        if e.tem("estabulo"):
            estabulo(s, 128, 57, neve)
        if e.tem("laticinio"):
            laticinio(s, 166, 57, neve)
        if e.tem("estufa"):
            estufa(s, 218, 58, neve)
        casa(s, 4, 58, neve, e.tem("casa_reformada"))
        celeiro(s, 264, 64, neve)
        x0, y0, x1, y1 = CURRAL
        d.cerca_horizontal(s, x0, x1, y0 + 6)
        for x in (x0, x1):
            s.fill(COR["madeira"], (x, y0 + 1, 2, y1 - y0))
        galinheiro(s, x0 + 4, y0 + 17, e.tem("galinheiro_grande"), neve)
        self.cache[chave] = s
        return s

    def _fazenda(self, s, e, t, dt, frac, noite, luzes):
        s.blit(self._fundo_fazenda(e, frac, noite), (0, 0))
        if not noite:
            self._nuvens(s, e, dt)
        if e.tem("moinho"):
            moinho_pas(s, 84, 58, t)
        d.fumaca(s, 34, 22, t)
        if e.tem("padaria"):
            d.fumaca(s, 118, 32, t + 0.5)
        for i in range(8):
            canteiro(s, i, e.canteiros[i] if i < len(e.canteiros) else None, e, t)
        # depois dos canteiros: desenhados antes, o canteiro passava por cima e
        # cortava a cara do espantalho
        enfeites(s, e, t)
        self.rebanho.atualizar(e, dt)
        self.rebanho.desenhar(s, e, t)
        x0, _, x1, y1 = CURRAL
        d.cerca_horizontal(s, x0, x1 + 2, y1 + 1)
        if e.cachorro:
            olhar = int(t / 2.5) % 2 == 0
            s.blit(sprites.sprite(sprites.CACHORRO, espelhar=olhar), (44, 84 - (1 if int(t * 3) % 4 == 0 else 0)))
        luzes += [(24, 45, 6, 4), (275, 30, 7, 4)]

    def _nuvens(self, s, e, dt):
        n = 5 if e.clima in ("nublado", "chuva", "tempestade", "neve") else 3
        cor = (255, 255, 255) if e.clima in ("sol", "nublado") else (200, 205, 215)
        sombra = (215, 228, 240) if e.clima in ("sol", "nublado") else (160, 168, 180)
        for nv in self.nuvens[:n]:
            nv[0] += nv[2] * dt
            if nv[0] > ARTE_L + 10:
                nv[0] = -30
            d.nuvem(s, nv[0], nv[1], cor, sombra)

    def desenhar(self, destino, local, e, t, dt):
        s = self.surf
        noite = local in ("noite", "festa")
        frac = 0.82 if local == "titulo" else 1 - e.energia / max(1, e.energia_max)
        luzes = []
        if local in ("fazenda", "noite", "titulo"):
            self._fazenda(s, e, t, dt, frac, noite, luzes)
        else:
            self._ceu(s, e, frac, noite, com_sol=local != "floresta")
            if not noite and local != "floresta":
                self._nuvens(s, e, dt)
            locais.desenhar(local, s, e, t, dt, luzes, self.part)

        # clima
        if local != "titulo":
            if e.clima in ("chuva", "tempestade"):
                self.part.chuva(s, dt, e.clima == "tempestade")
            elif e.clima == "neve":
                self.part.neve(s, dt, t)
        if e.clima == "tempestade" and not noite:
            self.relampago -= dt
            if self.relampago < -random.uniform(3, 7):
                self.relampago = 0.12
            if self.relampago > 0:
                s.fill((90, 90, 90), special_flags=pygame.BLEND_ADD)

        # iluminação por hora do dia
        if noite:
            s.fill((70, 80, 150), special_flags=pygame.BLEND_MULT)
            for x, y, fase in self.estrelas:
                if s.get_at((x, y))[2] < 90 and math.sin(t * 2 + fase) > -0.3:
                    s.set_at((x, y), (255, 250, 220))
            for r in luzes:
                s.fill(COR["amarelo"], r)
            if local == "festa":
                self._fogos(s, dt)
            elif local == "noite":
                self.part.vagalumes(s, t, 50)
        elif frac > 0.55:
            k = (frac - 0.55) / 0.45
            s.fill(d.lerp((255, 255, 255), (255, 205, 170), k), special_flags=pygame.BLEND_MULT)

        pygame.transform.scale(s, (ARTE_L * ESCALA_ARTE, ARTE_A * ESCALA_ARTE), destino)

    def _fogos(self, s, dt):
        if random.random() < dt * 1.5:
            cor = random.choice([COR["amarelo"], COR["rosa"], COR["agua_clara"], COR["vermelho_claro"], COR["branco"]])
            self.fogos.append([random.uniform(40, 280), random.uniform(8, 30), 0.0, cor])
        for f in self.fogos:
            f[2] += dt
            r = f[2] * 30
            for k in range(10):
                ang = k * math.pi / 5
                s.set_at((int(f[0] + math.cos(ang) * r), int(f[1] + math.sin(ang) * r + f[2] * 6)), f[3])
        self.fogos = [f for f in self.fogos if f[2] < 0.7]
