"""Interface: HUD, caixa de diálogo de madeira, opções, texto digitando e painéis.

Tem dois layouts: o de computador e o de celular (deitado), com letra 2x maior e
botões altos para tocar com o dedo.
"""
import math
import random

import pygame

import sprites
from config import ALTURA, ANDROID, COR, IOS, LARGURA, WEB
from estado import nome_item
from fonte import ALTURA_LINHA
from tela import Opcao

NOMES = ["Luna", "Chico", "Mel", "Bento", "Nina", "Tito", "Jade", "Theo", "Lia", "Pingo", "Cacau", "Fubá"]
VEL_TEXTO = 75  # caracteres por segundo
# no celular o teclado e da tela: so abre quando a pessoa toca na caixa de texto
TECLADO_DE_TELA = ANDROID or IOS


class Layout:
    """Medidas da interface para computador ou celular."""

    def __init__(self, celular):
        self.celular = celular
        self.esc = 2 if celular else 1                  # escala da letra
        self.caixa = (pygame.Rect(6, 132, LARGURA - 12, ALTURA - 138) if celular
                      else pygame.Rect(6, 216, LARGURA - 12, ALTURA - 222))
        self.linha = ALTURA_LINHA * self.esc            # altura de uma linha de texto
        self.linha_opcao = 24 if celular else 13        # altura de cada botão de opção
        self.corte_cena = 76 if celular else 0          # quanto do céu some no celular


# ---------------------------------------------------------------- formas básicas
def arredondado(s, cor, r):
    """Retângulo com cantos 'mordidos' de 1 pixel (visual pixel art)."""
    s.fill(cor, r.inflate(0, -2))
    s.fill(cor, r.inflate(-2, 0))


def pilula(s, r, cor=COR["pergaminho"]):
    arredondado(s, COR["madeira_esc"], r.move(0, 2))
    arredondado(s, COR["contorno"], r)
    arredondado(s, cor, r.inflate(-2, -2))
    s.fill(COR["branco"], (r.x + 3, r.y + 2, r.w - 6, 1))


def moldura(s, r):
    arredondado(s, COR["madeira_esc"], r.move(0, 3))
    arredondado(s, COR["contorno"], r)
    arredondado(s, COR["madeira_esc"], r.inflate(-2, -2))
    arredondado(s, COR["madeira"], r.inflate(-4, -4))
    s.fill(COR["madeira_clara"], (r.x + 4, r.y + 3, r.w - 8, 1))
    arredondado(s, COR["contorno"], r.inflate(-10, -10))
    interno = r.inflate(-12, -12)
    arredondado(s, COR["pergaminho"], interno)
    s.fill(COR["pergaminho_esc"], (interno.x + 1, interno.bottom - 2, interno.w - 2, 2))
    for cx, cy in ((r.x + 2, r.y + 2), (r.right - 4, r.y + 2), (r.x + 2, r.bottom - 4), (r.right - 4, r.bottom - 4)):
        s.fill(COR["madeira_brilho"], (cx, cy, 2, 2))
    return interno


# ---------------------------------------------------------------- UI principal
class UI:
    def __init__(self, fonte, celular=False):
        self.f = fonte
        self.lay = Layout(celular)
        self.tela = None
        self.sel = 0
        self.paginas = [[]]
        self.pag = 0
        self.chars = 0.0
        self.texto_entrada = ""
        self.teclado_aberto = False
        self.flutuantes = []
        self.tocar = lambda nome: None  # trocado pelo main para tocar sons
        self._ultimo_blip = 0

    @property
    def celular(self):
        return self.lay.celular

    def usar_layout(self, celular):
        """Troca entre computador e celular (refaz a quebra de linhas da tela atual)."""
        if celular != self.lay.celular:
            self.lay = Layout(celular)
            if self.tela:
                self._paginar()
                self.pag = min(self.pag, len(self.paginas) - 1)

    # ---------------------------------------------------------- troca de tela
    def nova_tela(self, tela):
        self.tela = tela
        # No celular (iPhone e Android) o teclado da tela so abre quando a pessoa
        # toca na caixa de texto: aberto logo de cara ele cobria a pergunta antes
        # de dar para ler. No computador o teclado fisico segue ligado direto.
        self._teclado(bool(tela.entrada) and not TECLADO_DE_TELA)
        if tela.entrada and not any(o.automatica for o in tela.opcoes):
            # no celular não há teclado físico: botões para digitar (janela do navegador) ou sortear
            extras = [Opcao("Sortear um nome", lambda: tela.entrada(random.choice(NOMES)), automatica=True)]
            if WEB:
                extras.insert(0, Opcao("Digitar o nome", lambda: self._digitar(tela), automatica=True))
            tela.opcoes[:0] = extras
        self.sel = next((i for i, o in enumerate(tela.opcoes) if o.ativa), 0)
        self.pag = 0
        self.chars = 0.0
        self.texto_entrada = ""
        self._paginar()

    def _teclado(self, ligar):
        """Liga/desliga a digitacao. No iPhone, o SDL empurra a tela para cima para
        a caixa de texto (set_text_input_rect) nao ficar escondida atras do teclado."""
        try:
            if ligar:
                pygame.key.set_text_input_rect(self._rect_campo())
                pygame.key.start_text_input()
            else:
                pygame.key.stop_text_input()
        except (AttributeError, pygame.error):
            pass   # pygame antigo ou sem video: seguir sem teclado de tela
        self.teclado_aberto = ligar

    def _rect_campo(self):
        esc = self.lay.esc
        return pygame.Rect(self.lay.caixa.x + 14, self._topo_opcoes() + 2, 200 * esc, 6 + 12 * esc)

    @staticmethod
    def _digitar(tela):
        """Abre a caixinha de texto do navegador (no celular ela chama o teclado)."""
        try:
            import platform
            nome = platform.window.prompt("Digite o nome:", "")
        except Exception:
            nome = None
        nome = str(nome).strip() if nome else ""
        return tela.entrada(nome[:16]) if nome else tela

    def _area_texto(self):
        caixa = self.lay.caixa
        x = caixa.x + (78 if self.tela.retrato else 14)
        return x, caixa.y + 11, caixa.right - 14 - x

    def _colunas(self):
        return 2 if len(self.tela.opcoes) > 5 else 1

    def _topo_opcoes(self):
        n = len(self.tela.opcoes) + (2 if self.tela.entrada else 0)
        linhas = math.ceil(n / self._colunas()) if n else 0
        return self.lay.caixa.bottom - 9 - linhas * self.lay.linha_opcao

    def _paginar(self):
        x, y, w = self._area_texto()
        esc, alt = self.lay.esc, self.lay.linha
        linhas = self.f.quebrar(self.tela.texto, w, esc)
        max_cheia = max(1, (self.lay.caixa.bottom - 12 * esc - 12 - y) // alt)
        max_ultima = max(1, (self._topo_opcoes() - 4 - y) // alt)
        paginas = []
        while len(linhas) > max_ultima:
            corte = min(max_cheia, len(linhas))
            if corte == len(linhas):  # tudo cabe numa página, mas não junto com as opções
                corte = max(1, len(linhas) - max_ultima)
            paginas.append(linhas[:corte])
            linhas = linhas[corte:]
        paginas.append(linhas)
        self.paginas = paginas

    @property
    def ultima_pagina(self):
        return self.pag >= len(self.paginas) - 1

    @property
    def digitando(self):
        return self.chars < sum(len(l) for l in self.paginas[self.pag])

    # ---------------------------------------------------------- lógica
    def atualizar(self, dt):
        if self.digitando:
            self.chars += VEL_TEXTO * dt
            if int(self.chars) // 4 != self._ultimo_blip:
                self._ultimo_blip = int(self.chars) // 4
                self.tocar("blip")
        for fl in self.flutuantes:
            fl[2] -= 18 * dt
            fl[4] -= dt
        self.flutuantes = [fl for fl in self.flutuantes if fl[4] > 0]

    def flutuar(self, texto, x, y, cor):
        self.flutuantes.append([texto, x, y, cor, 1.4])

    def _avancar_texto(self):
        """Clique/Enter enquanto há texto: completa ou passa a página. Devolve True se consumiu."""
        if self.digitando:
            self.chars = 9999
            return True
        if not self.ultima_pagina:
            self.pag += 1
            self.chars = 0
            self.tocar("blip")
            return True
        return False

    def _rects_opcoes(self):
        cols = self._colunas()
        alt = self.lay.linha_opcao
        topo = self._topo_opcoes() + (2 * alt if self.tela.entrada else 0)
        x0 = self.lay.caixa.x + 14
        largura = (self.lay.caixa.w - 28) // cols
        linhas = math.ceil(len(self.tela.opcoes) / cols)
        rects = []
        for i in range(len(self.tela.opcoes)):
            c, l = (i // linhas, i % linhas) if cols > 1 else (0, i)
            rects.append(pygame.Rect(x0 + c * largura, topo + l * alt, largura - 6, alt - 1))
        return rects

    def _mover(self, passo):
        n = len(self.tela.opcoes)
        if n:
            self.sel = (self.sel + passo) % n
            self.tocar("blip")

    def evento(self, ev):
        """Devolve a Opcao escolhida, ("entrada", texto) ou None."""
        t = self.tela
        if t is None:
            return None
        mostrando_opcoes = self.ultima_pagina and not self.digitando
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if not mostrando_opcoes:
                self._avancar_texto()
                return None
            if t.entrada and self._rect_campo().collidepoint(ev.pos):
                self._teclado(True)
                return None
            for i, r in enumerate(self._rects_opcoes()):
                if r.collidepoint(ev.pos):
                    self.sel = i
                    return self._confirmar()
            return None
        if ev.type == pygame.MOUSEMOTION and mostrando_opcoes:
            for i, r in enumerate(self._rects_opcoes()):
                if r.collidepoint(ev.pos) and self.sel != i:
                    self.sel = i
                    self.tocar("blip")
            return None
        if ev.type != pygame.KEYDOWN:
            return None
        if t.entrada and mostrando_opcoes:
            if ev.key == pygame.K_RETURN and self.texto_entrada.strip():
                self.tocar("ok")
                return ("entrada", self.texto_entrada.strip())
            if ev.key == pygame.K_RETURN and TECLADO_DE_TELA:
                self._teclado(False)   # "retorno" com a caixa vazia: so esconde o teclado
                return None
            if ev.key == pygame.K_BACKSPACE:
                self.texto_entrada = self.texto_entrada[:-1]
            elif ev.unicode and ev.unicode.isprintable() and len(self.texto_entrada) < 16:
                self.texto_entrada += ev.unicode
            return None
        if ev.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER):
            if not mostrando_opcoes:
                self._avancar_texto()
                return None
            return self._confirmar()
        if not mostrando_opcoes:
            return None
        cols = self._colunas()
        linhas = math.ceil(len(t.opcoes) / cols) if t.opcoes else 1
        if ev.key in (pygame.K_UP, pygame.K_w):
            self._mover(-1)
        elif ev.key in (pygame.K_DOWN, pygame.K_s):
            self._mover(1)
        elif ev.key in (pygame.K_LEFT, pygame.K_a) and cols > 1:
            self._mover(-linhas)
        elif ev.key in (pygame.K_RIGHT, pygame.K_d) and cols > 1:
            self._mover(linhas)
        elif pygame.K_1 <= ev.key <= pygame.K_9:
            i = ev.key - pygame.K_1
            if i < len(t.opcoes):
                self.sel = i
                return self._confirmar()
        return None

    def _confirmar(self):
        if not self.tela.opcoes:
            return None
        op = self.tela.opcoes[self.sel]
        if not op.ativa:
            self.tocar("erro")
            return None
        self.tocar("ok")
        return op

    # ---------------------------------------------------------- desenho
    def desenhar(self, s, e, t):
        tela, esc, caixa = self.tela, self.lay.esc, self.lay.caixa
        if tela.local != "titulo":
            self.hud(s, e)
        if tela.painel == "celeiro":
            self.painel_celeiro(s, e)
        elif tela.painel == "pedidos":
            self.painel_pedidos(s, e)
        elif tela.local == "titulo":
            self.logo(s, t)

        interno = moldura(s, caixa)
        if tela.titulo:
            w = self.f.largura(tela.titulo, esc) + 20
            alt = 20 if esc == 1 else 28
            aba = pygame.Rect(caixa.x + 16, caixa.y - alt + 8, w, alt)
            pilula(s, aba, COR["madeira_clara"])
            self.f.desenhar(s, tela.titulo, aba.x + 10, aba.y + 1 + esc, COR["contorno"], esc,
                            sombra=COR["madeira_brilho"])
        if tela.retrato:
            quadro = pygame.Rect(interno.x + 4, interno.y + 4, 52, 52)
            arredondado(s, COR["contorno"], quadro)
            s.blit(sprites.retrato(tela.retrato), (quadro.x + 2, quadro.y + 2))
        # texto com efeito de máquina de escrever
        x, y, _ = self._area_texto()
        resta = int(self.chars)
        for linha in self.paginas[self.pag]:
            self.f.desenhar(s, linha[:max(0, resta)], x, y, COR["texto"], esc)
            resta -= len(linha)
            y += self.lay.linha
        if not self.ultima_pagina and not self.digitando and int(t * 3) % 2:
            self.f.desenhar(s, "▼", caixa.right - 14 - 8 * esc, caixa.bottom - 10 - 12 * esc, COR["madeira"], esc)
        if self.ultima_pagina and not self.digitando:
            if tela.entrada:
                self._campo_texto(s, t)
            self._opcoes(s, t)

    def _campo_texto(self, s, t):
        esc = self.lay.esc
        r = self._rect_campo()
        arredondado(s, COR["contorno"], r)
        arredondado(s, COR["branco"], r.inflate(-2, -2))
        if TECLADO_DE_TELA and not self.teclado_aberto and not self.texto_entrada:
            self.f.desenhar(s, "toque aqui para digitar", r.x + 5, r.y + 2, COR["texto_claro"], esc)
            return
        fim = self.f.desenhar(s, self.texto_entrada, r.x + 5, r.y + 2, COR["texto"], esc)
        if int(t * 2) % 2:
            s.fill(COR["texto"], (fim + 1, r.y + 2 + 2 * esc, esc, 10 * esc))
        if not self.celular:  # no celular se usa os botões embaixo
            self.f.desenhar(s, "Digite e aperte ENTER", r.right + 10, r.y + 2, COR["texto_claro"])

    def _cabe(self, texto, largura):
        """Corta o texto com '..' se não couber na largura."""
        esc = self.lay.esc
        if self.f.largura(texto, esc) <= largura:
            return texto
        while texto and self.f.largura(texto + "..", esc) > largura:
            texto = texto[:-1]
        return texto.rstrip() + ".."

    def _opcoes(self, s, t):
        esc = self.lay.esc
        for i, (op, r) in enumerate(zip(self.tela.opcoes, self._rects_opcoes())):
            ty = r.y + (r.h - 12 * esc) // 2  # centraliza o texto no botão
            if i == self.sel:
                arredondado(s, COR["pergaminho_esc"], r.inflate(4, 0))
                dx = int(math.sin(t * 8) * 1.5)
                self.f.desenhar(s, "▶", r.x + dx, ty, COR["vermelho"] if op.ativa else COR["texto_claro"], esc)
            elif self.celular:  # no celular cada opção parece um botão
                pygame.draw.rect(s, COR["pergaminho_esc"], r.inflate(4, 0), 1)
            cor = COR["texto"] if op.ativa else COR["texto_claro"]
            num = f"{i + 1}." if i < 9 else ""
            x = self.f.desenhar(s, num, r.x + 6 + 4 * esc, ty, COR["madeira"] if op.ativa else COR["texto_claro"], esc)
            x += 4 * esc
            if op.icone:
                s.blit(sprites.icone_item(op.icone, esc), (x, ty + 2 * esc))
                x += 11 * esc
            dica_w = self.f.largura(op.dica, esc) + 10 * esc if op.dica else 0
            self.f.desenhar(s, self._cabe(op.texto, r.right - x - dica_w - 4), x, ty, cor, esc)
            if op.dica:
                self.f.desenhar(s, op.dica, r.right - 4, ty, COR["madeira"] if op.ativa else COR["texto_claro"],
                                esc, direita=True)

    # ---------------------------------------------------------- HUD estilo Hay Day
    def hud(self, s, e):
        esc = self.lay.esc
        # nível + barra de XP
        atual, prox = e.progresso_xp()
        barra = pygame.Rect(26, 10, 96, 14)
        pilula(s, barra)
        s.fill(COR["dourado"], (barra.x + 12, barra.y + 4, int((barra.w - 16) * atual / prox), 6))
        s.fill(COR["amarelo"], (barra.x + 12, barra.y + 4, int((barra.w - 16) * atual / prox), 2))
        pygame.draw.circle(s, COR["madeira_esc"], (22, 19), 14)
        pygame.draw.circle(s, COR["contorno"], (22, 17), 14)
        pygame.draw.circle(s, COR["verde_ui"], (22, 17), 12)
        pygame.draw.circle(s, COR["verde_ui_esc"], (22, 19), 10)
        pygame.draw.circle(s, COR["verde_ui"], (22, 17), 10)
        self.f.desenhar(s, str(e.nivel), 23, 8, COR["branco"], escala=2 if e.nivel < 10 else 1,
                        sombra=COR["verde_ui_esc"], centro=True)
        # dia, estação e clima (no celular: só o essencial, com letra grande)
        if self.celular:
            info = f"Ano {e.ano} · {e.estacao} {e.dia_da_estacao}/7"
        else:
            info = f"Ano {e.ano}  ·  {e.estacao} {e.dia_da_estacao}/7  ·  {e.nome_clima}"
        r = pygame.Rect(132, 6 if self.celular else 8, self.f.largura(info, esc) + 18, 6 + 12 * esc)
        pilula(s, r)
        self.f.desenhar(s, info, r.x + 9, r.y + 1 + esc, COR["texto"], esc)
        # dinheiro
        txt = f"{e.dinheiro}"
        w = self.f.largura(txt, 2) + 34
        r = pygame.Rect(LARGURA - w - 8, 6, w, 22)
        pilula(s, r, COR["creme"])
        s.blit(sprites.sprite(sprites.MOEDA, escala=2), (r.x + 6, r.y + 4))
        self.f.desenhar(s, txt, r.x + 24, r.y - 2, COR["texto"], escala=2)
        # energia
        r2 = pygame.Rect(LARGURA - 8 - (e.energia_max * 9 + 26), 32, e.energia_max * 9 + 26, 16)
        pilula(s, r2)
        s.blit(sprites.sprite(sprites.RAIO), (r2.x + 7, r2.y + 4))
        for i in range(e.energia_max):
            cor = COR["verde_ui"] if i < e.energia else COR["pergaminho_esc"]
            s.fill(COR["contorno"], (r2.x + 17 + i * 9, r2.y + 4, 7, 8))
            s.fill(cor, (r2.x + 18 + i * 9, r2.y + 5, 5, 6))
        # números subindo (+moedas, +XP)
        for texto, x, y, cor, vida in self.flutuantes:
            self.f.desenhar(s, texto, int(x), int(y), cor, esc, sombra=COR["contorno"])

    def painel_celeiro(self, s, e):
        itens = sorted(e.celeiro.items(), key=lambda kv: nome_item(kv[0]))
        if self.celular:  # celular: grade de ícones com quantidade, letra grande
            cols = 8
            linhas = max(1, math.ceil(len(itens) / cols))
            interno = moldura(s, pygame.Rect(6, 4, LARGURA - 12, 44 + linhas * 22))
            self.f.desenhar(s, f"Celeiro · Ração: {e.racao}", interno.x + 4, interno.y - 2, COR["madeira_esc"], 2)
            if not itens:
                self.f.desenhar(s, "(vazio)", interno.x + 4, interno.y + 22, COR["texto_claro"], 2)
            for i, (item, n) in enumerate(itens):
                x, y = interno.x + 4 + (i % cols) * 76, interno.y + 24 + (i // cols) * 22
                s.blit(sprites.icone_item(item, 2), (x, y + 2))
                self.f.desenhar(s, f"x{n}", x + 20, y - 2, COR["texto"], 2)
            return
        cols = 2
        linhas = max(1, math.ceil(len(itens) / cols))
        interno = moldura(s, pygame.Rect(LARGURA - 262, 54, 254, 34 + linhas * 14))
        self.f.desenhar(s, f"Celeiro  ·  Ração: {e.racao}", interno.x + 4, interno.y, COR["madeira_esc"])
        if not itens:
            self.f.desenhar(s, "(vazio)", interno.x + 4, interno.y + 14, COR["texto_claro"])
        for i, (item, n) in enumerate(itens):
            c, l = i // linhas, i % linhas
            x, y = interno.x + 4 + c * 118, interno.y + 14 + l * 14
            s.blit(sprites.icone_item(item), (x, y + 2))
            self.f.desenhar(s, f"{nome_item(item)} x{n}", x + 11, y, COR["texto"])

    def painel_pedidos(self, s, e):
        esc = self.lay.esc
        linha = 14 * esc - (4 if esc > 1 else 0)
        for i, p in enumerate(e.pedidos):
            r = pygame.Rect(18 + i * 206, 4 if self.celular else 52, 192, 34 + (len(p["itens"]) + 2) * linha)
            interno = moldura(s, r)
            nome = p["cliente"].capitalize() if self.celular else f"Pedido de {p['cliente']}"
            self.f.desenhar(s, self._cabe(nome, interno.w - 6), interno.x + 3, interno.y - esc + 1,
                            COR["madeira_esc"], esc)
            y = interno.y + linha
            for item, n in p["itens"].items():
                tem = e.qtd(item)
                s.blit(sprites.icone_item(item, esc), (interno.x + 3, y + 2 * esc))
                cor = COR["verde_ui_esc"] if tem >= n else COR["vermelho"]
                texto = f"{tem}/{n}" if self.celular else f"{nome_item(item)}  {tem}/{n}"
                self.f.desenhar(s, texto, interno.x + 5 + 10 * esc, y, cor, esc)
                y += linha
            self.f.desenhar(s, f"¢ {p['moedas']}   ★ {p['xp']}", interno.x + 3, y + 2, COR["texto"], esc)

    def contornado(self, s, texto, x, y, cor, escala, borda=COR["contorno"], sombra=None):
        """Texto centralizado com contorno grosso, para ler bem sobre o cenário."""
        for dx in (-escala, 0, escala):
            for dy in (-escala, 0, escala, 2 * escala):
                if dx or dy:
                    self.f.desenhar(s, texto, x + dx, y + dy, borda, escala=escala, centro=True)
        self.f.desenhar(s, texto, x, y, cor, escala=escala, centro=True, sombra=sombra)

    def logo(self, s, t):
        y = (18 if self.celular else 30) + int(math.sin(t * 1.5) * 3)
        self.contornado(s, "Vale do Girassol", LARGURA // 2, y, COR["amarelo"], 4, sombra=COR["laranja"])
        self.contornado(s, "um RPG de escolhas na fazenda", LARGURA // 2, y + 56, COR["creme"], 2)
