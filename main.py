"""Vale do Girassol - um RPG de escolhas numa fazenda, em pixel art.

Rodar:  python main.py      (precisa do pygame:  pip install pygame)
Versão web (celular/navegador), rodando DENTRO desta pasta (para ler o pygbag.ini):
    python -X utf8 -m pygbag --build --archive --title "Vale do Girassol" --template web/pagina.tmpl --icon web/icone.png .
    -> build/web e build/web.zip  (web/pagina.tmpl é a página própria: tamanho certo no celular e pixels nítidos)
Controles: mouse/toque, setas + ENTER/ESPAÇO, ou teclas 1-9.  F11 = tela cheia.  M = liga/desliga música.
"""
import array
import asyncio
import math
import sys

import pygame

from cenario import Cenario
from config import ALTURA, ARTE_A, ESCALA_ARTE, FPS, LARGURA, TITULO_JOGO, COR, WEB
from estado import Estado
from fonte import FontePixel
from historia import Historia
from interface import UI
from musica import Musica


class Sons:
    """Efeitos sonoros 8-bit gerados na hora (nenhum arquivo de áudio necessário)."""

    RECEITAS = {
        "blip": ([1200], 0.018, 0.035, "quadrada"),
        "ok": ([660, 990], 0.09, 0.10, "quadrada"),
        "erro": ([220, 150], 0.16, 0.10, "quadrada"),
        "moeda": ([988, 1319], 0.20, 0.10, "quadrada"),
        "nivel": ([523, 659, 784, 1047], 0.45, 0.10, "quadrada"),
        "fanfarra": ([392, 523, 659, 784, 659, 784, 1047], 0.9, 0.09, "quadrada"),
        "noite": ([392, 330, 262], 0.7, 0.14, "seno"),
    }

    def __init__(self):
        self.sons = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(22050, -16, 1, 512)
            freq, _, canais = pygame.mixer.get_init()
            for nome, (notas, dur, vol, forma) in self.RECEITAS.items():
                self.sons[nome] = self._gerar(notas, dur, vol, forma, freq, canais)
        except pygame.error:
            self.sons = {}  # sem placa de som: o jogo roda em silêncio

    @staticmethod
    def _gerar(notas, dur, vol, forma, taxa, canais):
        n = int(taxa * dur)
        buf = array.array("h")
        for i in range(n):
            f = notas[min(len(notas) - 1, i * len(notas) // n)]
            fase = (i / taxa) * f
            onda = (1 if fase % 1 < 0.5 else -1) if forma == "quadrada" else math.sin(fase * 2 * math.pi)
            envelope = (1 - (i % (n // len(notas))) / (n / len(notas))) ** 0.6
            amostra = int(onda * envelope * vol * 32767)
            buf.extend([amostra] * canais)
        return pygame.mixer.Sound(buffer=buf.tobytes())

    def tocar(self, nome):
        som = self.sons.get(nome)
        if som:
            som.play()


def estado_demo():
    """Uma fazenda bonita e cheia, só para enfeitar a tela de título."""
    e = Estado("Demo")
    e.clima = "sol"
    e.construcoes = ["moinho", "estabulo", "padaria", "estufa", "irrigacao"]
    e.canteiros = [e._canteiro_vazio() for _ in range(8)]
    for c, (cult, dias) in zip(e.canteiros, [("trigo", 2), ("milho", 3), ("tomate", 4), ("morango", 4),
                                             ("cenoura", 3), ("abobora", 5), ("trigo", 1), ("milho", 1)]):
        c.update(cultura=cult, dias=dias, regado=True)
    for tipo, nome in (("galinha", "a"), ("galinha", "b"), ("vaca", "c"), ("ovelha", "d"), ("porco", "e")):
        e.comprar_animal(tipo, nome)
    e.cachorro = "Paçoca"
    return e


def eh_celular():
    """Celular/tablet (tela de toque) usa o layout de letra grande. `--celular` força no PC, para testar."""
    if "--celular" in sys.argv:
        return True
    if not WEB:
        return False
    try:
        import platform
        return bool(platform.window.matchMedia("(pointer: coarse)").matches)
    except Exception:
        return False


def icone_janela():
    s = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.line(s, COR["folha"], (16, 18), (16, 31), 3)
    for i in range(10):
        ang = i * math.pi / 5
        pygame.draw.circle(s, COR["amarelo"], (16 + int(math.cos(ang) * 8), 13 + int(math.sin(ang) * 8)), 5)
    pygame.draw.circle(s, COR["madeira_esc"], (16, 13), 6)
    return s


class Jogo:
    def __init__(self):
        pygame.mixer.pre_init(22050, -16, 1, 512)
        pygame.init()
        # no navegador o próprio pygbag amplia a tela para caber na página
        self.tela = pygame.display.set_mode((LARGURA, ALTURA), 0 if WEB else pygame.SCALED | pygame.RESIZABLE)
        pygame.display.set_caption(TITULO_JOGO)
        pygame.display.set_icon(icone_janela())
        self.relogio = pygame.time.Clock()
        self.sons = Sons()
        self.musica = Musica()
        self.ui = UI(FontePixel(), celular=eh_celular())
        self.ui.tocar = self.sons.tocar
        self.cenario = Cenario()
        self.cena = pygame.Surface((LARGURA, ARTE_A * ESCALA_ARTE))  # no celular ela é recortada em cima
        self.em_pe = False           # celular em pé (retrato)? então pede para girar
        self._checar_em_pe = 0.0
        self.historia = Historia()
        self.demo = estado_demo()
        self.ui.nova_tela(self.historia.titulo())
        self.fade = 0.0        # 0 = transparente, 1 = preto
        self.fade_dir = 0
        self.proxima = None
        self.escurecer = pygame.Surface((LARGURA, ALTURA))
        self.t = 0.0
        self.usou_toque = False

    # ---------------------------------------------------------- troca de telas
    def trocar(self, nova):
        if nova is None:
            self.sair()
            return
        muda_lugar = nova.local != self.ui.tela.local or nova.local == "noite"
        if muda_lugar:
            self.proxima = nova
            self.fade_dir = 1
        else:
            self._aplicar(nova)

    def _aplicar(self, nova):
        self.ui.nova_tela(nova)
        self.musica.para_local(nova.local)
        if nova.som:
            self.sons.tocar(nova.som)

    def escolher(self, resultado):
        e = self.historia.e
        antes = (e.dinheiro, e.xp, e.nivel, e.reputacao)
        if isinstance(resultado, tuple):
            nova = self.ui.tela.entrada(resultado[1])
        else:
            nova = resultado.acao()
        e = self.historia.e  # pode ter mudado (novo jogo / continuar)
        if e.dinheiro != antes[0] and self.ui.tela.local != "titulo":
            dif = e.dinheiro - antes[0]
            self.ui.flutuar(f"{'+' if dif > 0 else ''}{dif} ¢", LARGURA - 90, 52,
                            COR["amarelo"] if dif > 0 else COR["vermelho_claro"])
            if dif > 0:
                self.sons.tocar("moeda")
        if e.xp > antes[1]:
            self.ui.flutuar(f"+{e.xp - antes[1]} ★", 60, 30, COR["amarelo"])
        if e.nivel > antes[2]:
            self.ui.flutuar("NÍVEL NOVO!", 40, 44, COR["grama_clara"])
            self.sons.tocar("nivel")
        if e.reputacao > antes[3]:
            self.ui.flutuar(f"+{e.reputacao - antes[3]} ♥", 150, 30, COR["rosa"])
        self.trocar(nova)

    def sair(self):
        if self.ui.tela and self.ui.tela.local != "titulo":
            self.historia.e.salvar()
        if WEB:  # uma página não "fecha": só salva e segue
            return
        pygame.quit()
        sys.exit()

    # ---------------------------------------------------------- loop
    async def rodar(self):
        """Loop assíncrono: o `await` a cada quadro devolve o controle ao navegador."""
        while True:
            await asyncio.sleep(0)
            dt = min(self.relogio.tick(FPS) / 1000, 0.05)
            self.t += dt
            for ev in pygame.event.get():
                ev = self._traduzir_toque(ev)
                if ev is None:
                    continue
                if ev.type == pygame.QUIT:
                    self.sair()
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                    continue
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_m and not self.ui.tela.entrada:
                    ligada = self.musica.alternar_mudo()
                    self.ui.flutuar("Música ligada" if ligada else "Música desligada", LARGURA // 2 - 40, 90,
                                    COR["creme"])
                    continue
                if self.fade_dir or self.em_pe:
                    continue
                resultado = self.ui.evento(ev)
                if resultado is not None:
                    self.escolher(resultado)
            self._atualizar_fade(dt)
            self._atualizar_orientacao(dt)
            self.musica.atualizar()
            self.ui.atualizar(dt)
            self._desenhar(dt)

    def _traduzir_toque(self, ev):
        """Toque na tela do celular vira um clique na posição exata do dedo.

        No navegador, o SDL às vezes entrega o clique "de imitação" de um toque com a
        posição antiga do mouse; o evento FINGERDOWN traz a posição certa (de 0 a 1).
        """
        if ev.type == pygame.FINGERDOWN:
            self.usou_toque = True
            self.ui.usar_layout(True)  # tocou na tela: é celular/tablet, usa letra e botões grandes
            pos = (int(ev.x * LARGURA), int(ev.y * ALTURA))
            self.ui.evento(pygame.event.Event(pygame.MOUSEMOTION, pos=pos))  # destaca a opção tocada
            return pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=1)
        if (self.usou_toque and getattr(ev, "touch", False)
                and ev.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION)):
            return None  # já tratado pelo FINGERDOWN; evita clique duplo
        return ev

    def _atualizar_fade(self, dt):
        if self.fade_dir > 0:
            self.fade = min(1.0, self.fade + dt * 4)
            if self.fade >= 1:
                self._aplicar(self.proxima)
                self.proxima = None
                self.fade_dir = -1
        elif self.fade_dir < 0:
            self.fade = max(0.0, self.fade - dt * 4)
            if self.fade <= 0:
                self.fade_dir = 0

    def _atualizar_orientacao(self, dt):
        """No navegador do celular, confere de vez em quando se ele está em pé."""
        if not (WEB and self.ui.celular):
            return
        self._checar_em_pe -= dt
        if self._checar_em_pe <= 0:
            self._checar_em_pe = 0.5
            try:
                import platform
                self.em_pe = platform.window.innerHeight > platform.window.innerWidth
            except Exception:
                self.em_pe = False

    def _desenhar(self, dt):
        if self.em_pe:
            self.ui.gire_o_celular(self.tela, self.t)
            pygame.display.flip()
            return
        tela_atual = self.ui.tela
        e = self.demo if tela_atual.local == "titulo" else self.historia.e
        self.tela.fill(COR["contorno"])
        self.cenario.desenhar(self.cena, tela_atual.local, e, self.t, dt)
        self.tela.blit(self.cena, (0, -self.ui.lay.corte_cena))
        self.ui.desenhar(self.tela, e, self.t)
        if self.fade > 0:
            self.escurecer.set_alpha(int(self.fade * 255))
            self.tela.blit(self.escurecer, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    asyncio.run(Jogo().rodar())
