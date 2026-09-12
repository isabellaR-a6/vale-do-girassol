"""Estado do jogo: dinheiro, plantações, animais, celeiro, clima, pedidos e save."""
import json
import os
import random
import sys

from config import (ANIMAIS, ARQUIVO_SAVE, CANTEIROS_INICIAIS, CLIMA_POR_ESTACAO, CONSTRUCOES,
                    CULTURAS, DIAS_DO_ANO, DIAS_POR_ESTACAO, ENERGIA_BASE, ESTACOES, ITENS,
                    NOME_CLIMA, RECEITAS, XP_NIVEIS, LOTES_POR_ACAO, WEB, ANDROID)

if ANDROID:  # pasta privada do app: não é apagada quando o APK é atualizado
    CAMINHO_SAVE = os.path.join(os.environ.get("ANDROID_PRIVATE", "."), ARQUIVO_SAVE)
elif sys.platform == "ios":  # o bundle do app é somente leitura; Documents é gravável
    CAMINHO_SAVE = os.path.join(os.path.expanduser("~/Documents"), ARQUIVO_SAVE)
else:
    CAMINHO_SAVE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ARQUIVO_SAVE)
CHAVE_WEB = "vale_do_girassol_save"  # no navegador o save fica no localStorage


def _local_storage():
    import platform  # no pygbag, este módulo dá acesso ao "window" do navegador
    return platform.window.localStorage


def nome_item(item):
    return ITENS[item][0] if item in ITENS else ("Ração" if item == "racao" else item)


class Estado:
    def __init__(self, nome="Fazendeira"):
        self.nome = nome
        self.dinheiro = 500
        self.dia = 1
        self.xp = 0
        self.energia = ENERGIA_BASE
        # cada canteiro: {"cultura": str|None, "dias": int, "regado": bool, "seco": int, "morto": bool}
        self.canteiros = [self._canteiro_vazio() for _ in range(CANTEIROS_INICIAIS)]
        # cada animal: {"tipo", "nome", "alimentado", "feliz", "progresso", "pronto"}
        self.animais = []
        self.celeiro = {}
        self.racao = 5
        self.construcoes = []
        self.clima = "sol"
        self.mod_precos = {}
        self.em_alta = None
        self.pedidos = []
        self.reputacao = 0
        self.cachorro = None
        self.flags = {}
        self.stats = {"ganho": 0, "colhido": 0, "pedidos": 0}
        self.modo_livre = False
        self.sortear_precos()
        self.gerar_pedidos()

    # ------------------------------------------------------------ utilidades
    @staticmethod
    def _canteiro_vazio():
        return {"cultura": None, "dias": 0, "regado": False, "seco": 0, "morto": False, "magica": False}

    @property
    def estacao(self):
        return ESTACOES[((self.dia - 1) // DIAS_POR_ESTACAO) % 4]

    @property
    def dia_da_estacao(self):
        return (self.dia - 1) % DIAS_POR_ESTACAO + 1

    @property
    def nome_clima(self):
        return NOME_CLIMA[self.clima]

    @property
    def nivel(self):
        n = 1
        for i, limite in enumerate(XP_NIVEIS):
            if self.xp >= limite:
                n = i + 1
        return n

    def progresso_xp(self):
        """(xp dentro do nível, xp necessário para o próximo)."""
        n = self.nivel
        if n >= len(XP_NIVEIS):
            return 1, 1
        base, prox = XP_NIVEIS[n - 1], XP_NIVEIS[n]
        return self.xp - base, prox - base

    @property
    def energia_max(self):
        return ENERGIA_BASE + (1 if self.tem("casa_reformada") else 0)

    def tem(self, construcao):
        return construcao in self.construcoes

    def qtd(self, item):
        return self.celeiro.get(item, 0)

    def adicionar(self, item, n=1):
        if item == "racao":
            self.racao += n
        else:
            self.celeiro[item] = self.celeiro.get(item, 0) + n

    def remover(self, item, n=1):
        self.celeiro[item] = self.celeiro.get(item, 0) - n
        if self.celeiro[item] <= 0:
            del self.celeiro[item]

    def gastar_energia(self, n=1):
        self.energia = max(0, self.energia - n)

    def ganhar_xp(self, n):
        """Dá XP e devolve uma mensagem se subiu de nível."""
        antes = self.nivel
        self.xp += n
        if self.nivel > antes:
            novos = [c["nome"] for c in CULTURAS.values() if c["nivel"] == self.nivel]
            novos += [a["nome"] for a in ANIMAIS.values() if a["nivel"] == self.nivel]
            novos += [c["nome"] for c in CONSTRUCOES.values() if c["nivel"] == self.nivel]
            extra = f" Desbloqueou: {', '.join(novos)}." if novos else ""
            return f"★ Você subiu para o nível {self.nivel}!{extra}"
        return ""

    # ------------------------------------------------------------ mercado
    def sortear_precos(self):
        self.mod_precos = {item: random.uniform(0.8, 1.25) for item in ITENS}
        self.em_alta = random.choice([i for i in ITENS if i != "abobora_gigante"])
        self.mod_precos[self.em_alta] = 1.6

    def preco(self, item):
        return max(1, round(ITENS[item][1] * self.mod_precos.get(item, 1.0)))

    def vender(self, item, n):
        n = min(n, self.qtd(item))
        ganho = self.preco(item) * n
        self.remover(item, n)
        self.dinheiro += ganho
        self.stats["ganho"] += ganho
        return ganho

    # ------------------------------------------------------------ plantação
    def pode_plantar(self):
        return self.estacao != "Inverno" or self.tem("estufa")

    def canteiros_vazios(self):
        return [c for c in self.canteiros if c["cultura"] is None]

    def plantar(self, cultura):
        """Planta em todos os canteiros vazios que o dinheiro permitir. Devolve (qtd, custo)."""
        preco = CULTURAS[cultura]["semente"]
        qtd = 0
        for c in self.canteiros_vazios():
            if self.dinheiro < preco:
                break
            self._semear(c, cultura)
            self.dinheiro -= preco
            qtd += 1
        return qtd, qtd * preco

    def _semear(self, c, cultura, magica=False):
        c.update(cultura=cultura, dias=0, regado=self.clima in ("chuva", "tempestade") or self.tem("irrigacao"),
                 seco=0, morto=False, magica=magica)

    def plantar_magica(self):
        """A semente do viajante vira uma abóbora gigante."""
        self._semear(self.canteiros_vazios()[0], "abobora", magica=True)
        self.flags.pop("semente_magica", None)
        self.flags["magica_plantada"] = True

    def precisa_regar(self):
        return [c for c in self.canteiros if c["cultura"] and not c["morto"] and not c["regado"]
                and not self.maduro(c)]

    def regar(self):
        alvo = self.precisa_regar()
        for c in alvo:
            c["regado"] = True
        return len(alvo)

    def maduro(self, c):
        return c["cultura"] and not c["morto"] and c["dias"] >= CULTURAS[c["cultura"]]["dias"]

    def prontos(self):
        return [c for c in self.canteiros if self.maduro(c)]

    def colher(self):
        colhido = {}
        xp = 0
        for c in self.canteiros:
            if self.maduro(c):
                cult = c["cultura"]
                n = 2 if random.random() < 0.25 else 1  # às vezes vem colheita dupla
                item = cult
                if c.get("magica"):
                    item, n = "abobora_gigante", 1
                    xp += 40
                colhido[item] = colhido.get(item, 0) + n
                self.adicionar(item, n)
                xp += CULTURAS[cult]["xp"]
                c.update(self._canteiro_vazio())
            elif c["morto"]:
                c.update(self._canteiro_vazio())
        self.stats["colhido"] += sum(colhido.values())
        return colhido, xp

    # ------------------------------------------------------------ animais
    def capacidade(self, casa):
        if casa == "galinheiro":
            return 5 if self.tem("galinheiro_grande") else 2
        return 4 if self.tem("estabulo") else 0

    def ocupacao(self, casa):
        return sum(1 for a in self.animais if ANIMAIS[a["tipo"]]["casa"] == casa)

    def comprar_animal(self, tipo, nome):
        self.dinheiro -= ANIMAIS[tipo]["preco"]
        self.animais.append({"tipo": tipo, "nome": nome, "alimentado": False,
                             "feliz": 3, "progresso": 0, "pronto": False})

    def racao_necessaria(self):
        return sum(ANIMAIS[a["tipo"]]["racao"] for a in self.animais if not a["alimentado"])

    def alimentar(self):
        n = 0
        for a in self.animais:
            custo = ANIMAIS[a["tipo"]]["racao"]
            if not a["alimentado"] and self.racao >= custo:
                self.racao -= custo
                a["alimentado"] = True
                n += 1
        return n

    def coletar(self):
        produtos = {}
        for a in self.animais:
            if a["pronto"]:
                prod = ANIMAIS[a["tipo"]]["produto"]
                n = 2 if a["feliz"] >= 5 and random.random() < 0.4 else 1
                produtos[prod] = produtos.get(prod, 0) + n
                self.adicionar(prod, n)
                a["pronto"] = False
        return produtos

    # ------------------------------------------------------------ oficinas
    def receitas_disponiveis(self):
        return [k for k, r in RECEITAS.items() if self.tem(r["predio"])]

    def lotes_possiveis(self, chave):
        r = RECEITAS[chave]
        return min(self.qtd(i) // n for i, n in r["precisa"].items())

    def produzir(self, chave):
        r = RECEITAS[chave]
        lotes = min(LOTES_POR_ACAO, self.lotes_possiveis(chave))
        for i, n in r["precisa"].items():
            self.remover(i, n * lotes)
        item, n = r["faz"]
        self.adicionar(item, n * lotes)
        return lotes, n * lotes

    # ------------------------------------------------------------ pedidos (estilo Hay Day)
    def gerar_pedidos(self):
        while len(self.pedidos) < 3:
            self.pedidos.append(self._novo_pedido())

    def _novo_pedido(self):
        disponiveis = [c for c, d in CULTURAS.items() if d["nivel"] <= self.nivel]
        disponiveis += [ANIMAIS[a["tipo"]]["produto"] for a in self.animais]
        disponiveis += [RECEITAS[r]["faz"][0] for r in self.receitas_disponiveis() if RECEITAS[r]["faz"][0] != "racao"]
        disponiveis = sorted(set(disponiveis))
        itens = {}
        for item in random.sample(disponiveis, k=min(len(disponiveis), random.choice([1, 1, 2]))):
            itens[item] = random.randint(2, 5) if ITENS[item][1] < 100 else random.randint(1, 2)
        valor = sum(ITENS[i][1] * n for i, n in itens.items())
        clientes = ["Dona Lúcia", "Seu Zé", "Bia", "Rosa", "o Prefeito", "a Escola", "o Café da Praça"]
        return {"itens": itens, "moedas": round(valor * 1.45), "xp": max(8, valor // 12),
                "cliente": random.choice(clientes)}

    def pode_entregar(self, pedido):
        return all(self.qtd(i) >= n for i, n in pedido["itens"].items())

    def entregar(self, idx):
        p = self.pedidos.pop(idx)
        for i, n in p["itens"].items():
            self.remover(i, n)
        self.dinheiro += p["moedas"]
        self.stats["ganho"] += p["moedas"]
        self.stats["pedidos"] += 1
        self.reputacao += 1
        return p

    # ------------------------------------------------------------ passagem do dia
    def sortear_clima(self):
        opcoes = CLIMA_POR_ESTACAO[self.estacao]
        self.clima = random.choices([o[0] for o in opcoes], [o[1] for o in opcoes])[0]

    def avancar_dia(self):
        """Roda a noite: plantas crescem, animais produzem, novo clima. Devolve o relatório."""
        rel = []
        cresceu = secou = 0
        inverno_sem_estufa = self.estacao == "Inverno" and not self.tem("estufa")
        for c in self.canteiros:
            if not c["cultura"] or c["morto"] or self.maduro(c):
                continue
            if inverno_sem_estufa:
                c["morto"] = True
                secou += 1
            elif c["regado"]:
                c["dias"] += 1
                c["seco"] = 0
                cresceu += 1
            else:
                c["seco"] += 1
                if c["seco"] >= 2:
                    c["morto"] = True
                    secou += 1
        if cresceu:
            rel.append(f"{cresceu} canteiro(s) cresceram durante a noite.")
        if secou:
            rel.append(f"{secou} planta(s) morreram de sede ou frio. Lembre de regar!")

        prontos = 0
        for a in self.animais:
            if a["alimentado"]:
                a["feliz"] = min(5, a["feliz"] + 1)
                if not a["pronto"]:
                    a["progresso"] += 1
                    if a["progresso"] >= ANIMAIS[a["tipo"]]["intervalo"]:
                        a["progresso"] = 0
                        a["pronto"] = True
                        prontos += 1
            else:
                a["feliz"] = max(0, a["feliz"] - 1)
            a["alimentado"] = False
        if prontos:
            rel.append(f"{prontos} animal(is) têm produtos esperando por você.")
        tristes = [a["nome"] for a in self.animais if a["feliz"] <= 1]
        if tristes:
            rel.append(f"{', '.join(tristes)} está com fome e tristonho(a)...")

        self.dia += 1
        if self.dia_da_estacao == 1:
            rel.append(f"Começou o {self.estacao}!" if self.estacao != "Primavera"
                       else "Começou a Primavera!")
            if self.estacao == "Inverno" and not self.tem("estufa"):
                rel.append("A terra congelou: sem estufa, nada cresce no inverno.")
        self.sortear_clima()
        self.sortear_precos()
        self.energia = self.energia_max
        chuva = self.clima in ("chuva", "tempestade")
        for c in self.canteiros:
            c["regado"] = chuva or self.tem("irrigacao")
        if chuva:
            rel.append("Está chovendo: as plantações já amanheceram regadas.")
        elif self.tem("irrigacao") and any(c["cultura"] for c in self.canteiros):
            rel.append("A irrigação regou tudo sozinha.")
        self.gerar_pedidos()
        return rel

    @property
    def fim_do_ano(self):
        return self.dia > DIAS_DO_ANO and not self.modo_livre

    def patrimonio(self):
        total = self.dinheiro
        total += sum(CONSTRUCOES[c]["preco"] // 2 for c in self.construcoes)
        total += sum(ANIMAIS[a["tipo"]]["preco"] // 2 for a in self.animais)
        total += sum(ITENS[i][1] * n for i, n in self.celeiro.items())
        total += (len(self.canteiros) - CANTEIROS_INICIAIS) * 80
        return total

    # ------------------------------------------------------------ save
    def salvar(self):
        if WEB:
            _local_storage().setItem(CHAVE_WEB, json.dumps(self.__dict__, ensure_ascii=False))
            return
        with open(CAMINHO_SAVE, "w", encoding="utf-8") as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=1)

    @classmethod
    def carregar(cls):
        if WEB:
            dados = json.loads(_local_storage().getItem(CHAVE_WEB))
        else:
            with open(CAMINHO_SAVE, encoding="utf-8") as f:
                dados = json.load(f)
        e = cls()
        e.__dict__.update(dados)
        return e

    @staticmethod
    def existe_save():
        if WEB:
            return bool(_local_storage().getItem(CHAVE_WEB))
        return os.path.exists(CAMINHO_SAVE)
