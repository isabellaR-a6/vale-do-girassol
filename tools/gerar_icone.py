"""Desenha o icone do app: um girassol em pixel art, na paleta do proprio jogo.

A fonte da verdade e a grade de 30x30 gerada aqui em codigo — nao existe
arquivo de arte "original" para abrir num programa de desenho. Mudou um numero
aqui, rodou o script, o icone novo sai pronto. E o mesmo principio do resto do
jogo, onde sprite, fonte e musica nascem em codigo.

Por que 30x30: 180 / 30 = 6 e 120 / 30 = 4, os dois inteiros exatos. Os dois
tamanhos que o iPhone usa saem com o pixel perfeitamente quadrado, sem borrao.
Com 32 nenhum dos dois fechava.

Rodar (na pasta do projeto):  python tools/gerar_icone.py
"""
import math
import os
import sys

import pygame

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import COR  # noqa: E402

N = 30                      # lado da grade
CX, CY = 14.5, 12.2         # centro da flor
DISC = 4.6                  # raio do miolo
NP, RC = 8, 7.4             # quantidade de petalas e a que distancia ficam
PA, PB = 4.0, 3.0           # semi-eixos da petala: radial e lateral
CAULE = (13, 16)            # colunas do caule: precisa de 4 para sobrar verde
                            # depois que o contorno come uma de cada lado

PAL = {
    "o": COR["contorno"], "y": COR["amarelo"], "g": COR["dourado"],
    "O": COR["laranja"], "c": COR["creme"],
    "B": COR["madeira_esc"], "t": COR["terra_esc"],
    "G": COR["grama"], "D": COR["grama_esc"],
    "S": COR["ceu"], "M": COR["ceu_claro"], "H": COR["ceu_horizonte"],
}
CEU = ("S", "M", "H")


def montar_grade():
    """Devolve a grade NxN de caracteres, cada um uma cor da paleta."""
    g = [[("S" if y < 10 else "M" if y < 20 else "H") for _ in range(N)] for y in range(N)]
    donos = [[set() for _ in range(N)] for _ in range(N)]

    # petalas: cada uma e uma elipse apontando para fora
    for k in range(NP):
        ang = k * 2 * math.pi / NP - math.pi / 2
        ca, sa = math.cos(ang), math.sin(ang)
        pcx, pcy = CX + RC * ca, CY + RC * sa
        for y in range(N):
            for x in range(N):
                dx, dy = x + 0.5 - pcx, y + 0.5 - pcy
                u, v = ca * dx + sa * dy, -sa * dx + ca * dy
                if u * u / (PA * PA) + v * v / (PB * PB) > 1:
                    continue
                donos[y][x].add(k)
                r = math.hypot(x + 0.5 - CX, y + 0.5 - CY)
                cor = "O" if r < DISC + 1.8 else "g" if r < DISC + 3.0 else "y"
                if -0.6 < u < 1.4 and -1.6 < v < -0.2:
                    cor = "c"      # o brilho da petala: e ele que da o charme
                g[y][x] = cor

    # contorno de CADA petala, inclusive onde uma encosta na outra. E daqui que
    # vem o recorte; so o contorno de fora faz as oito virarem uma bolha so.
    risco = set()
    for y in range(N):
        for x in range(N):
            for k in donos[y][x]:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < N and 0 <= ny < N) or k not in donos[ny][nx]:
                        risco.add((x, y))
                        break
    for x, y in risco:
        g[y][x] = "o"

    # caule reto e de 4 colunas. Na primeira versao ele era torto e de 3, e o
    # contorno comia uma de cada lado: sobrava 1 coluna e saia quebrado.
    for y in range(16, N):
        for x in range(CAULE[0], CAULE[1] + 1):
            g[y][x] = "G" if x == CAULE[0] + 1 else "D"

    # miolo por cima, com a textura em xadrez (tapa a base das petalas)
    for y in range(N):
        for x in range(N):
            r = math.hypot(x + 0.5 - CX, y + 0.5 - CY)
            if r <= DISC:
                trama = (x + y) % 3 == 0 or (x - y + 9) % 3 == 0
                g[y][x] = "t" if (trama or r > DISC - 1.2) else "B"

    # contorno geral: pixel de flor ou caule encostado no ceu vira contorno
    antes = [linha[:] for linha in g]
    for y in range(N):
        for x in range(N):
            if antes[y][x] in CEU:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < N and 0 <= ny < N and antes[ny][nx] in CEU:
                    g[y][x] = "o"
                    break
    return g


def desenhar(grade, lado):
    """Pinta a grade numa Surface quadrada de `lado` pixels.

    `lado` precisa ser multiplo de N, senao os pixels saem de tamanhos
    diferentes e a arte perde o alinhamento.
    """
    if lado % N:
        raise ValueError(f"{lado} nao e multiplo de {N}")
    escala = lado // N
    surf = pygame.Surface((lado, lado))          # sem alpha: o iOS exige opaco
    for y, linha in enumerate(grade):
        for x, ch in enumerate(linha):
            surf.fill(PAL[ch], (x * escala, y * escala, escala, escala))
    return surf


def main():
    pygame.init()
    grade = montar_grade()
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for nome, lado in (("icone.png", 480), ("icone_120.png", 120), ("icone_180.png", 180)):
        caminho = os.path.join(raiz, "web", nome)
        pygame.image.save(desenhar(grade, lado), caminho)
        print(f"{nome}: {lado}x{lado} ({lado // N}x por pixel da grade)")
    pygame.quit()


if __name__ == "__main__":
    main()
