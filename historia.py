"""Os menus de escolha da fazenda, o começo da história e o fim do ano."""
import random

import cidade
import eventos
from config import ANIMAIS, CULTURAS, RECEITAS, WEB
from estado import Estado, nome_item
from tela import Opcao, Tela


def lista_itens(d):
    return ", ".join(f"{n} {nome_item(i)}" for i, n in d.items())


class Historia:
    def __init__(self):
        self.e = Estado()

    # ------------------------------------------------------------ ajudantes
    def op(self, texto, acao, energia=0, ativa=True, dica="", icone=""):
        """Cria uma opção; se custa energia e não há energia, ela fica desativada."""
        if energia:
            if self.e.energia < energia:
                ativa, dica = False, "sem energia"
            elif not dica:
                dica = f"⚡{energia}"
        return Opcao(texto, acao, ativa, dica, icone)

    def xp(self, n, msg):
        subiu = self.e.ganhar_xp(n)
        return msg + (f"\n{subiu}" if subiu else "")

    # ------------------------------------------------------------ título e começo
    def titulo(self):
        ops = [Opcao("Novo jogo", self.novo_jogo)]
        if Estado.existe_save():
            ops.insert(0, Opcao("Continuar", self.continuar))
        ops.append(Opcao("Como jogar", self.como_jogar))
        if not WEB:  # no navegador não tem como "fechar" o jogo
            ops.append(Opcao("Sair", lambda: None))
        return Tela("Um vale tranquilo, uma fazenda esquecida e muitas escolhas pela frente.",
                    ops, local="titulo")

    def como_jogar(self):
        return Tela(
            "Tudo é feito por escolhas: leia a situação e escolha uma opção embaixo (clique, setas + ENTER "
            "ou as teclas 1 a 9; M liga/desliga a música). Cada dia você tem ⚡ energia para fazer coisas: plantar, regar, colher, cuidar "
            "dos animais, ir à cidade, explorar... Quando a energia acaba, é hora de dormir.\n"
            "Plantas só crescem se forem regadas (ou se chover). Animais só produzem se forem alimentados. "
            "Venda no mercado, cumpra pedidos e construa melhorias. Em 28 dias (1 ano) a vila avalia a sua fazenda!",
            [Opcao("Entendi!", self.titulo)], local="titulo", titulo="Como jogar")

    def continuar(self):
        self.e = Estado.carregar()
        return self.menu_fazenda("Bem-vindo(a) de volta ao Vale do Girassol!")

    def novo_jogo(self):
        self.e = Estado()
        return Tela("Uma carta amarelada chegou pelo correio, com cheiro de terra molhada e bolo de fubá...\n"
                    "Antes de abrir, o carteiro pergunta: para quem devo assinar o recibo?",
                    titulo="Uma carta", local="titulo", entrada=self.definir_nome)

    def definir_nome(self, nome):
        self.e.nome = nome[:16]
        return Tela(
            f"\"Oi, {self.e.nome}! Se você está lendo isto, é porque eu finalmente me aposentei e fui morar "
            "na praia. Deixo para você a Fazenda Girassol: um celeiro velho, um galinheiro, quatro canteiros "
            "e ¢500 guardados na lata de biscoito. A terra é boa e os vizinhos também. "
            "Daqui a um ano a vila faz o Concurso da Fazenda do Ano... quem sabe? Com amor, Vovó Cida.\"",
            [Opcao("Arrumar a mala", self.mala)], titulo="Carta da Vovó Cida", retrato="vovo", local="titulo")

    def mala(self):
        def escolher(tipo):
            e = self.e
            if tipo == "dinheiro":
                e.dinheiro += 60
                e.adicionar("racao", 5)
                msg = "Você trouxe um saco de dinheiro da venda das suas coisas: +¢60 e ração extra."
            elif tipo == "galinha":
                e.comprar_animal("galinha", "Pipoca")
                e.dinheiro += ANIMAIS["galinha"]["preco"]
                msg = "Você trouxe a Pipoca, sua galinha de estimação. Ela já foi morar no galinheiro!"
            else:
                e.reputacao += 3
                msg = "Você trouxe um bolo caseiro para os vizinhos. Todo mundo já gosta de você! (+3 ♥)"
            return self.chegada(msg)
        return Tela("Antes de partir para o Vale do Girassol, o que você coloca na mala?",
                    [Opcao("Minhas economias", lambda: escolher("dinheiro"), dica="+¢60"),
                     Opcao("Minha galinha de estimação", lambda: escolher("galinha"), dica="+1 galinha"),
                     Opcao("Um bolo para os vizinhos", lambda: escolher("bolo"), dica="+3 ♥")],
                    titulo="A mala", local="titulo")

    def chegada(self, msg):
        return Tela(msg + "\n\nDepois de uma longa viagem de ônibus, você chega. O mato está alto, a pintura do "
                    "celeiro descascando... mas o pôr do sol no vale é lindo. É aqui que tudo começa.",
                    [Opcao("Começar o primeiro dia", lambda: self.menu_fazenda(
                        "Primeiro dia! Dica: plante trigo (cresce rápido) e não esqueça de regar."))],
                    titulo="Fazenda Girassol")

    # ------------------------------------------------------------ menu principal
    def resumo(self):
        e = self.e
        partes = []
        vazios, prontos, sede = len(e.canteiros_vazios()), len(e.prontos()), len(e.precisa_regar())
        mortos = sum(1 for c in e.canteiros if c["morto"])
        if prontos:
            partes.append(f"{prontos} canteiro(s) pronto(s) para colher")
        if sede:
            partes.append(f"{sede} com sede")
        if mortos:
            partes.append(f"{mortos} com plantas mortas")
        if vazios:
            partes.append(f"{vazios} vazio(s)")
        txt = "Plantação: " + (", ".join(partes) if partes else "tudo crescendo bem") + "."
        if e.animais:
            fome = sum(1 for a in e.animais if not a["alimentado"])
            prod = sum(1 for a in e.animais if a["pronto"])
            txt += f" Animais: {len(e.animais)}"
            txt += f", {fome} com fome" if fome else ", todos alimentados"
            txt += f", {prod} com produtos." if prod else "."
        return txt

    def menu_fazenda(self, msg=""):
        e = self.e
        if e.energia <= 0:
            cabeca = "Você está sem energia. O corpo pede cama!"
        else:
            cabeca = f"Você tem ⚡{e.energia} de energia. O que você faz agora?"
        texto = (msg + "\n" if msg else "") + self.resumo() + "\n" + cabeca
        ops = [
            Opcao("Cuidar da plantação", self.menu_plantacao),
            Opcao("Cuidar dos animais", self.menu_animais),
            Opcao("Usar as oficinas", self.menu_oficinas, ativa=bool(e.receitas_disponiveis()),
                  dica="" if e.receitas_disponiveis() else "construa uma"),
            Opcao("Espiar o celeiro", self.ver_celeiro),
            Opcao("Sair da fazenda", self.menu_passeio),
            Opcao("Dormir até amanhã", self.dormir, dica="fim do dia"),
            Opcao("Salvar e ir ao título", self.salvar_sair),
        ]
        return Tela(texto, ops, titulo=f"Fazenda Girassol · {e.nome}", som="")

    def ver_celeiro(self):
        e = self.e
        total = sum(e.preco(i) * n for i, n in e.celeiro.items())
        return Tela(f"O celeiro velho range, mas guarda tudo direitinho. Se vendesse tudo hoje, daria uns ¢{total}.",
                    [Opcao("Voltar", self.menu_fazenda)], titulo="Celeiro", painel="celeiro")

    def salvar_sair(self):
        self.e.salvar()
        return self.titulo()

    # ------------------------------------------------------------ plantação
    def menu_plantacao(self, msg=""):
        e = self.e
        linhas = []
        for i, c in enumerate(e.canteiros):
            if c["cultura"] is None:
                continue
            nome = CULTURAS[c["cultura"]]["nome"]
            if c["morto"]:
                linhas.append(f"{nome} (morto)")
            elif e.maduro(c):
                linhas.append(f"{nome} (pronto!)")
            else:
                falta = CULTURAS[c["cultura"]]["dias"] - c["dias"]
                linhas.append(f"{nome} ({falta}d{'' if c['regado'] else ', sem água'})")
        info = "Canteiros: " + (", ".join(linhas) if linhas else "todos vazios") + "."
        if not e.pode_plantar():
            info += " A terra está congelada: sem estufa, nada cresce no inverno."
        texto = (msg + "\n" if msg else "") + info
        vazios, sede, prontos = e.canteiros_vazios(), e.precisa_regar(), e.prontos()
        mortos = any(c["morto"] for c in e.canteiros)
        ops = [
            self.op("Plantar sementes", self.escolher_semente, 1, ativa=bool(vazios) and e.pode_plantar(),
                    dica="" if vazios else "sem espaço"),
            self.op("Regar os canteiros", self.regar, 1, ativa=bool(sede), dica="" if sede else "tudo regado"),
            self.op("Colher", self.colher, 1, ativa=bool(prontos) or mortos, dica="" if prontos or mortos else "nada pronto"),
            Opcao("Voltar", self.menu_fazenda),
        ]
        if e.flags.get("semente_magica"):
            ops.insert(0, self.op("Plantar a Semente Mágica", self.plantar_magica, 1,
                                  ativa=bool(vazios) and e.pode_plantar(), icone="abobora"))
        return Tela(texto, ops, titulo="Plantação")

    def plantar_magica(self):
        self.e.plantar_magica()
        self.e.gastar_energia()
        return self.menu_plantacao("Você enterra a semente brilhante. A terra em volta dela esquenta... "
                                   "Regue e espere 5 dias!")

    def escolher_semente(self):
        e = self.e
        n = len(e.canteiros_vazios())
        ops = []
        for chave, c in CULTURAS.items():
            if c["nivel"] > e.nivel:
                ops.append(Opcao(c["nome"], self.escolher_semente, False, f"nível {c['nivel']}", chave))
            else:
                ops.append(Opcao(c["nome"], lambda k=chave: self.plantar(k), e.dinheiro >= c["semente"],
                                 f"¢{c['semente']} · {c['dias']} dias", chave))
        ops.append(Opcao("Voltar", self.menu_plantacao))
        return Tela(f"Você tem {n} canteiro(s) vazio(s). Qual semente você planta? (preço por canteiro)",
                    ops, titulo="Sementes")

    def plantar(self, cultura):
        e = self.e
        qtd, custo = e.plantar(cultura)
        e.gastar_energia()
        nome = CULTURAS[cultura]["nome"]
        msg = f"Você plantou {nome} em {qtd} canteiro(s) por ¢{custo}."
        if any(c["cultura"] == cultura and not c["regado"] for c in e.canteiros):
            msg += " Não esqueça de regar!"
        return self.menu_plantacao(self.xp(qtd, msg))

    def regar(self):
        n = self.e.regar()
        self.e.gastar_energia()
        return self.menu_plantacao(f"Você encheu o regador no poço e regou {n} canteiro(s). A terra agradece!")

    def colher(self):
        colhido, xp = self.e.colher()
        self.e.gastar_energia()
        if colhido:
            msg = f"Colheita! Foram para o celeiro: {lista_itens(colhido)}. (+★{xp})"
        else:
            msg = "Você limpou os canteiros com plantas mortas. Agora dá para plantar de novo."
        return self.menu_plantacao(self.xp(xp, msg))

    # ------------------------------------------------------------ animais
    def menu_animais(self, msg=""):
        e = self.e
        cap_g, cap_e = e.capacidade("galinheiro"), e.capacidade("estabulo")
        info = f"Galinheiro: {e.ocupacao('galinheiro')}/{cap_g}"
        info += f" · Estábulo: {e.ocupacao('estabulo')}/{cap_e}" if cap_e else " · Sem estábulo"
        info += f" · Ração: {e.racao}\n"
        if e.animais:
            info += "  ".join(f"{a['nome']} ({ANIMAIS[a['tipo']]['nome']} {'♥' * max(1, a['feliz'])})"
                              for a in e.animais)
        else:
            info += "Nenhum animal ainda. A Feira de Animais fica na cidade."
        texto = (msg + "\n" if msg else "") + info
        precisa = e.racao_necessaria()
        prontos = any(a["pronto"] for a in e.animais)
        ops = [
            self.op("Alimentar todos", self.alimentar, 1, ativa=precisa > 0 and e.racao > 0,
                    dica="" if precisa else "todos comeram"),
            self.op("Coletar produtos", self.coletar, 1, ativa=prontos, dica="" if prontos else "nada ainda"),
            self.op("Fazer carinho em todos", self.carinho, 1, ativa=bool(e.animais)),
            Opcao("Voltar", self.menu_fazenda),
        ]
        if precisa and e.energia and e.racao > 0:
            ops[0].dica = f"⚡1 · usa {min(precisa, e.racao)} ração"
        return Tela(texto, ops, titulo="Animais")

    def alimentar(self):
        e = self.e
        n = e.alimentar()
        e.gastar_energia()
        faltou = any(not a["alimentado"] for a in e.animais)
        msg = f"Você encheu os cochos: {n} animal(is) comeram felizes."
        if faltou:
            msg += " A ração acabou antes de todos comerem! Compre mais no mercado."
        return self.menu_animais(msg)

    def coletar(self):
        prods = self.e.coletar()
        self.e.gastar_energia()
        xp = sum(prods.values()) * 2
        return self.menu_animais(self.xp(xp, f"Você recolheu: {lista_itens(prods)}. (+★{xp})"))

    def carinho(self):
        e = self.e
        for a in e.animais:
            a["feliz"] = min(5, a["feliz"] + 1)
        e.gastar_energia()
        fofo = random.choice(e.animais)
        return self.menu_animais(self.xp(3, f"Você fez carinho em todo mundo. {fofo['nome']} até fechou os olhinhos. "
                                            "Animais felizes às vezes produzem em dobro!"))

    # ------------------------------------------------------------ oficinas
    def menu_oficinas(self, msg=""):
        e = self.e
        ops = []
        for chave in e.receitas_disponiveis():
            r = RECEITAS[chave]
            lotes = e.lotes_possiveis(chave)
            ingr = " + ".join(f"{n} {nome_item(i)}" for i, n in r["precisa"].items())
            item, n = r["faz"]
            op = self.op(f"{r['nome']} ({ingr})", lambda k=chave: self.produzir(k), 1, ativa=lotes > 0,
                         dica="" if lotes else "faltam itens", icone=item if item != "racao" else "racao")
            ops.append(op)
        ops.append(Opcao("Voltar", self.menu_fazenda))
        texto = (msg + "\n" if msg else "") + \
            f"Com ⚡1 você produz até 3 receitas de uma vez. Itens feitos valem bem mais no mercado!"
        return Tela(texto, ops, titulo="Oficinas", painel="celeiro")

    def produzir(self, chave):
        lotes, total = self.e.produzir(chave)
        self.e.gastar_energia()
        item = RECEITAS[chave]["faz"][0]
        return self.menu_oficinas(self.xp(5 * lotes, f"Pronto! Você fez {total} {nome_item(item)}. (+★{5 * lotes})"))

    # ------------------------------------------------------------ passeios
    def menu_passeio(self):
        return Tela("Para onde você vai? Cada passeio gasta ⚡1 (andar cansa!).", [
            self.op("Ir à cidade", lambda: self.ir(cidade.praca), 1),
            self.op("Explorar a floresta", lambda: self.ir(eventos.floresta), 1),
            self.op("Pescar no lago", lambda: self.ir(eventos.lago), 1),
            self.op("Visitar o Seu Zé", lambda: self.ir(eventos.vizinho), 1),
            Opcao("Ficar na fazenda", self.menu_fazenda),
        ], titulo="Estrada do vale")

    def ir(self, destino):
        self.e.gastar_energia()
        return destino(self)

    # ------------------------------------------------------------ fim do dia
    def dormir(self):
        e = self.e
        relatorio = e.avancar_dia()
        e.salvar()
        texto = "Você toma um banho, come uma sopinha e dorme como uma pedra. Zzz...\n" + " ".join(relatorio)
        if e.fim_do_ano:
            return Tela(texto, [Opcao("Acordar", self.final_ano)], local="noite", titulo="Noite", som="noite")
        return Tela(texto, [Opcao("Acordar", self.amanhecer)], local="noite", titulo="Noite", som="noite")

    def amanhecer(self):
        evento = eventos.da_manha(self)
        if evento:
            return evento
        e = self.e
        return self.menu_fazenda(f"Bom dia! Dia {e.dia}, {e.estacao}. O tempo está: {e.nome_clima.lower()}.")

    def final_ano(self):
        e = self.e
        pat = e.patrimonio() + e.reputacao * 40 + e.nivel * 100
        if pat >= 10000:
            titulo, fala = "FAZENDA LENDÁRIA", ("Nunca vi nada igual! A Fazenda Girassol virou cartão-postal do vale. "
                                                "O festival do ano que vem vai ter o seu nome!")
        elif pat >= 5000:
            titulo, fala = "FAZENDA PRÓSPERA", ("Que ano! Celeiro cheio, animais felizes e a vila inteira comprando "
                                                "de você. A Vovó Cida ficaria orgulhosa.")
        elif pat >= 2000:
            titulo, fala = "FAZENDA ACONCHEGANTE", ("Uma fazenda pequena, mas cheia de carinho. Com mais um ano de "
                                                    "trabalho, ninguém segura você!")
        else:
            titulo, fala = "UM BOM COMEÇO", ("Foi um ano difícil, mas você não desistiu. Toda grande fazenda "
                                             "começou com um canteiro só.")
        texto = (f"Prefeito Otávio: \"Atenção, vale! O resultado do Concurso da Fazenda do Ano...\"\n"
                 f"Pontuação de {e.nome}: {pat} pontos (patrimônio, amizade e experiência).\n"
                 f"Título: {titulo}! {fala}\n"
                 f"Você ganhou ¢{e.stats['ganho']}, colheu {e.stats['colhido']} vezes e entregou "
                 f"{e.stats['pedidos']} pedido(s).")

        def livre():
            e.modo_livre = True
            e.salvar()
            return self.amanhecer()
        return Tela(texto, [Opcao("Continuar cuidando da fazenda", livre),
                            Opcao("Voltar ao título", self.titulo)],
                    local="festa", retrato="prefeito", titulo="Festival do Fim do Ano", som="fanfarra")
