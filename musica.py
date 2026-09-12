"""Música de fundo chiptune composta em código (nenhum arquivo de áudio).

Cada música tem acordes, uma melodia e um estilo. O áudio é sintetizado numa
thread em segundo plano e a trilha muda sozinha conforme o lugar do jogo.

Notação da melodia: cada item é uma colcheia (1/8). "E5" = nota, "-" = segura
a nota anterior, "." = pausa. Cada compasso tem 8 itens.
"""
import array
import math
import random
import threading
import time

import pygame

from config import WEB

NOTAS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

MUSICAS = {
    "fazenda": {
        "bpm": 112, "estilo": "alegre",
        "acordes": "C G Am F C G F C  F G Em Am F G C C",
        "melodia": [
            "E5 - G5 - C6 - G5 E5", "D5 - G5 - B5 - A5 G5", "C5 - E5 - A5 - G5 E5", "F5 - E5 - D5 - - .",
            "E5 - G5 - C6 - D6 E6", "D6 - B5 - G5 - A5 B5", "C6 - A5 - F5 - A5 B5", "C6 - - - G5 - E5 -",
            "A5 - - C6 A5 - F5 -", "G5 - - B5 G5 - D5 -", "E5 - G5 - B5 - G5 -", "A5 - - - C6 - B5 A5",
            "A5 - F5 - C5 - F5 A5", "B5 - G5 - D5 - G5 B5", "C6 - G5 - E5 - G5 -", "C5 - - - . . . .",
        ],
    },
    "cidade": {
        "bpm": 126, "estilo": "alegre",
        "acordes": "F Bb C F Dm Bb C F",
        "melodia": [
            "F5 . A5 . C6 A5 F5 .", "D5 . F5 . Bb5 A5 G5 .", "E5 . G5 . C6 - Bb5 A5", "A5 - F5 - . . C5 .",
            "D5 . F5 . A5 . F5 D5", "F5 - D5 - Bb4 - D5 F5", "E5 G5 C6 - Bb5 A5 G5 E5", "F5 - - - . . C5 .",
        ],
    },
    "calmo": {
        "bpm": 84, "estilo": "calmo",
        "acordes": "Am F C G Am F G Am",
        "melodia": [
            "A4 - C5 - E5 - - .", "F5 - E5 - C5 - - .", "E5 - G5 - C6 - B5 -", "D5 - - - B4 - - .",
            "A4 - C5 - E5 - A5 -", "G5 - F5 - E5 - C5 -", "D5 - E5 - G5 - B4 -", "A4 - - - . . . .",
        ],
    },
    "noite": {
        "bpm": 66, "estilo": "ninar",
        "acordes": "C Am F G C Am G C",
        "melodia": [
            "G5 - E5 - - - C5 -", "A4 - C5 - E5 - - -", "F5 - E5 - D5 - C5 -", "D5 - - - . . . .",
            "G5 - E5 - - - C5 -", "A4 - C5 - E5 - G5 -", "F5 - D5 - B4 - D5 -", "C5 - - - . . . .",
        ],
    },
}

# qual música toca em cada lugar
# A fazenda soa diferente em cada estação. Não é música nova: é o mesmo tema
# vestido de outro jeito, mudando o andamento e o instrumento. O cenário e o céu
# já mudam com a estação; faltava o ouvido perceber que o ano está passando.
#
# (estilo, quanto muda o bpm em relação ao tema base)
ESTACAO_MUSICA = {
    "Primavera": ("alegre", 0),     # o tema como ele nasceu
    "Verão":     ("alegre", 12),    # mais corrido, dia comprido
    "Outono":    ("calmo", -14),    # arrastado, com eco
    "Inverno":   ("ninar", -30),    # quase parado, quieto
}
BPM_FAZENDA = MUSICAS["fazenda"]["bpm"]

MUSICA_DO_LOCAL = {"titulo": "fazenda", "fazenda": "fazenda", "cidade": "cidade", "festa": "cidade",
                   "floresta": "calmo", "lago": "calmo", "vizinho": "calmo", "noite": "noite"}

# instrumentos de cada estilo: (onda, duty, volume, sustentação, decaimento em s)
ESTILOS = {
    "alegre": {"melodia": ("q", 0.25, 0.10, 0.55, 0.18), "baixo": ("t", 0.5, 0.26, 0.7, 0.3),
               "arpejo": ("q", 0.125, 0.030, 0.2, 0.05), "bateria": True, "eco": False},
    "calmo": {"melodia": ("t", 0.5, 0.20, 0.5, 0.35), "baixo": ("t", 0.5, 0.20, 0.6, 0.6),
              "arpejo": ("t", 0.5, 0.06, 0.3, 0.12), "bateria": False, "eco": True},
    "ninar": {"melodia": ("s", 0.5, 0.20, 0.45, 0.5), "baixo": ("s", 0.5, 0.18, 0.6, 0.8),
              "arpejo": ("t", 0.5, 0.06, 0.2, 0.2), "bateria": False, "eco": True},
}


def midi(nota):
    """'Bb4' -> número MIDI."""
    semitom = NOTAS[nota[0]]
    resto = nota[1:]
    if resto[0] in "#b":
        semitom += 1 if resto[0] == "#" else -1
        resto = resto[1:]
    return 12 * (int(resto) + 1) + semitom


def acorde(nome):
    """'Am' -> (classe da nota fundamental, é menor?)."""
    menor = nome.endswith("m")
    raiz = nome[:-1] if menor else nome
    return midi(raiz + "0") % 12, menor


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


PEDACO = 4096  # a síntese pausa (yield) a cada tantas amostras, para não travar o navegador


class Sintetizador:
    """Todos os métodos são geradores: `yield` de vez em quando para dar a vez ao jogo."""

    def __init__(self, taxa, total):
        self.taxa = taxa
        self.total = total
        self.buf = [0.0] * total

    def nota(self, f, inicio, dur, onda, duty, vol, sus, dec):
        taxa, total, buf = self.taxa, self.total, self.buf
        i0, n = int(inicio * taxa), int(dur * taxa)
        inc = f / taxa
        ataque = max(1, min(n // 4, int(0.006 * taxa)))
        solta = max(1, min(n // 3, int(0.03 * taxa)))
        coef = math.exp(-1 / (dec * taxa))
        fase, env = 0.0, 1.0
        for k in range(n):
            if k % PEDACO == PEDACO - 1:
                yield
            fase += inc
            p = fase % 1.0
            if onda == "q":
                v = 1.0 if p < duty else -1.0
            elif onda == "t":
                v = 4.0 * abs(p - 0.5) - 1.0
            else:
                v = math.sin(6.283185307 * p)
            g = sus + (1.0 - sus) * env
            env *= coef
            if k < ataque:
                g *= k / ataque
            elif k > n - solta:
                g *= (n - k) / solta
            buf[(i0 + k) % total] += v * g * vol  # o final "dá a volta" para o loop ficar contínuo
        yield

    def bumbo(self, inicio, vol=0.32):
        taxa, total, buf = self.taxa, self.total, self.buf
        i0, n = int(inicio * taxa), int(0.11 * taxa)
        fase = 0.0
        for k in range(n):
            t = k / n
            fase += (140 - 95 * t) / taxa
            buf[(i0 + k) % total] += math.sin(6.283185307 * fase) * (1 - t) ** 2 * vol
        yield

    def ruido(self, inicio, dur, vol, semente):
        taxa, total, buf = self.taxa, self.total, self.buf
        rnd = random.Random(semente)
        i0, n = int(inicio * taxa), int(dur * taxa)
        for k in range(n):
            buf[(i0 + k) % total] += rnd.uniform(-1, 1) * (1 - k / n) ** 3 * vol
        yield

    def para_bytes(self, canais):
        """Gerador: no fim, self.pronto guarda os bytes do áudio."""
        pico = 0.0
        for i in range(0, self.total, PEDACO * 4):
            pico = max(pico, max(map(abs, self.buf[i:i + PEDACO * 4])))
            yield
        maior = max(1.0, pico / 0.9)
        dados = array.array("h")
        for i in range(0, self.total, PEDACO * 4):
            dados.extend(int(x / maior * 32767) for x in self.buf[i:i + PEDACO * 4])
            yield
        if canais == 2:
            estereo = array.array("h", bytes(len(dados) * 4))
            estereo[0::2] = dados
            estereo[1::2] = dados
            dados = estereo
        self.pronto = dados.tobytes()


def compor(nome, taxa, canais):
    """Gera a música inteira de uma vez e devolve os bytes."""
    for resultado in compor_aos_poucos(nome, taxa, canais):
        if resultado is not None:
            return resultado


def compor_aos_poucos(nome, taxa, canais):
    """Gerador: dá `yield None` enquanto trabalha e, no fim, `yield` com os bytes do áudio."""
    m = MUSICAS[nome]
    est = ESTILOS[m["estilo"]]
    colcheia = 60 / m["bpm"] / 2
    acordes = m["acordes"].split()
    total = int(len(acordes) * 8 * colcheia * taxa)
    s = Sintetizador(taxa, total)

    # melodia (+ eco suave nos estilos calmos)
    itens = " ".join(m["melodia"]).split()
    for i, item in enumerate(itens):
        if item in ("-", "."):
            continue
        dur = 1
        while i + dur < len(itens) and itens[i + dur] == "-":
            dur += 1
        f = hz(midi(item))
        onda, duty, vol, sus, dec = est["melodia"]
        yield from s.nota(f, i * colcheia, dur * colcheia * 0.95, onda, duty, vol, sus, dec)
        if est["eco"]:
            yield from s.nota(f, (i + 3) * colcheia, dur * colcheia * 0.9, onda, duty, vol * 0.3, sus, dec)

    for c, nome_acorde in enumerate(acordes):
        raiz, menor = acorde(nome_acorde)
        inicio = c * 8 * colcheia
        # baixo
        onda, duty, vol, sus, dec = est["baixo"]
        grave = 36 + raiz if 36 + raiz >= 40 else 48 + raiz  # baixo sempre entre E2 e D#3
        if m["estilo"] == "alegre":
            for b, intervalo in enumerate((0, 7, 0, 7)):
                yield from s.nota(hz(grave + intervalo), inicio + b * 2 * colcheia, colcheia * 1.6,
                                  onda, duty, vol, sus, dec)
        else:
            yield from s.nota(hz(grave), inicio, colcheia * 3.8, onda, duty, vol, sus, dec)
            yield from s.nota(hz(grave + 7), inicio + 4 * colcheia, colcheia * 3.8, onda, duty, vol * 0.8, sus, dec)
        # arpejo
        onda, duty, vol, sus, dec = est["arpejo"]
        base = 60 + raiz - (12 if raiz >= 7 else 0)
        tons = [0, 3 if menor else 4, 7, 12]
        passo = colcheia / 2 if m["estilo"] == "alegre" else colcheia
        for k in range(int(8 * colcheia / passo)):
            yield from s.nota(hz(base + tons[k % 4]), inicio + k * passo, passo * 0.9, onda, duty, vol, sus, dec)
        # bateria
        if est["bateria"]:
            for b in range(8):
                t = inicio + b * colcheia
                if b in (0, 4):
                    yield from s.bumbo(t)
                elif b in (2, 6):
                    yield from s.ruido(t, 0.09, 0.07, c * 10 + b)
                else:
                    yield from s.ruido(t, 0.025, 0.035, c * 10 + b)
    yield from s.para_bytes(canais)
    yield s.pronto


class Musica:
    """Toca a trilha certa para cada lugar, com transição suave (crossfade)."""

    VOLUME = 0.5

    def __init__(self):
        self.faixas = {}
        self.atual = None
        self.desejada = "fazenda"
        self.estacao = None   # qual estação o tema da fazenda está vestindo
        self.mudo = False
        self.fila = ["fazenda", "calmo", "cidade", "noite"]
        self.gerando = None  # (nome, gerador) da música sendo sintetizada agora
        self.ok = bool(pygame.mixer.get_init())
        if not self.ok:
            return
        pygame.mixer.set_reserved(2)  # canais 0 e 1 só para música
        self.canais = [pygame.mixer.Channel(0), pygame.mixer.Channel(1)]
        self.canal = 0
        if not WEB:  # no computador uma thread gera tudo; no navegador (sem threads) vai aos poucos
            threading.Thread(target=self._gerar_todas, daemon=True).start()

    def _gerar_todas(self):
        while self._passo():
            pass

    def _passo(self):
        """Avança um pouquinho a síntese. Devolve False quando todas as músicas estão prontas."""
        if self.gerando is None:
            if not self.fila:
                return False
            taxa, _, canais = pygame.mixer.get_init()
            nome = self.fila.pop(0)
            self.gerando = (nome, compor_aos_poucos(nome, taxa, canais))
        nome, gerador = self.gerando
        resultado = next(gerador)
        if resultado is not None:
            som = pygame.mixer.Sound(buffer=resultado)
            som.set_volume(0 if self.mudo else self.VOLUME)
            self.faixas[nome] = som
            self.gerando = None
        return True

    def ajustar_estacao(self, estacao):
        """Reveste o tema da fazenda quando a estação vira.

        Só re-sintetiza nas quatro viradas do ano, não a cada tela. A faixa
        antiga continua tocando até a nova ficar pronta e ocupar o lugar dela.
        """
        if estacao == self.estacao or estacao not in ESTACAO_MUSICA:
            return
        self.estacao = estacao
        estilo, delta = ESTACAO_MUSICA[estacao]
        MUSICAS["fazenda"]["estilo"] = estilo
        MUSICAS["fazenda"]["bpm"] = BPM_FAZENDA + delta
        if "fazenda" not in self.fila:
            self.fila.append("fazenda")

    def para_local(self, local):
        self.desejada = MUSICA_DO_LOCAL.get(local, "fazenda")
        try:  # a música que você vai ouvir agora passa na frente da fila
            self.fila.remove(self.desejada)
            self.fila.insert(0, self.desejada)
        except ValueError:
            pass  # já está pronta (ou sendo gerada agora)

    def atualizar(self):
        """Chamado a cada quadro: troca de música quando a desejada estiver pronta."""
        if not self.ok:
            return
        if WEB:
            limite = time.perf_counter() + 0.006  # ~6 ms por quadro para sintetizar
            while time.perf_counter() < limite and self._passo():
                pass
        if self.desejada == self.atual or self.desejada not in self.faixas:
            return
        self.canais[self.canal].fadeout(900)
        self.canal ^= 1
        self.canais[self.canal].play(self.faixas[self.desejada], loops=-1, fade_ms=1200)
        self.atual = self.desejada

    def alternar_mudo(self):
        self.mudo = not self.mudo
        for som in self.faixas.values():
            som.set_volume(0 if self.mudo else self.VOLUME)
        return not self.mudo
