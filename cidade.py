"""A cidade do vale: mercado, feira de animais, carpintaria, pedidos e café."""
import random

from config import (ANIMAIS, CANTEIROS_MAX, CONSTRUCOES, PACOTE_RACAO, PESSOAS, canteiro_preco)
from estado import nome_item
from tela import Opcao, Tela

NL = chr(10)

DICAS_CAFE = [
    "dizem que geleia de morango vale uma fortuna no mercado.",
    "ouvi que as raposas atacam galinheiros de quem não tem cachorro.",
    "no inverno a terra congela... só quem tem estufa continua plantando.",
    "animais bem cuidados (♥♥♥♥♥) às vezes dão produto em dobro!",
    "o Seu Zé adora visitas. Quem sabe ele não te dá um presente?",
    "planta sem água por duas noites seguidas... morre. Triste, mas é verdade.",
    "a floresta esconde cogumelos, amoras e às vezes umas surpresas.",
    "pedidos do quadro pagam bem mais do que vender no mercado.",
]


def praca(h, msg=""):
    e = h.e
    alta = nome_item(e.em_alta)
    texto = (msg + "\n" if msg else "") + \
        f"A praça está movimentada e cheira a pão de queijo. Hoje o preço de {alta} está nas alturas! Onde você vai?"
    ops = [
        Opcao("Mercado da Dona Lúcia", lambda: mercado(h)),
        Opcao("Feira de animais", lambda: feira(h)),
        Opcao("Carpintaria da Rosa", lambda: carpintaria(h)),
        Opcao("Quadro de pedidos", lambda: pedidos(h),
              dica=f"{sum(1 for p in e.pedidos if e.pode_entregar(p))} prontos"),
        Opcao("Café da praça", lambda: cafe(h), ativa=e.flags.get("cafe") != e.dia and e.dinheiro >= 15,
              dica="¢15" if e.flags.get("cafe") != e.dia else "já tomou hoje"),
        Opcao("Conversar com alguém", lambda: gente(h),
              dica=f"{sum(1 for k in PESSOAS if not e.ja_viu_hoje(k))} sem ver hoje"),
        Opcao("Voltar para a fazenda", h.menu_fazenda),
    ]
    return Tela(texto, ops, titulo="Praça da cidade", local="cidade")


# ---------------------------------------------------------------- mercado
def mercado(h, msg=""):
    e = h.e
    q, preco = PACOTE_RACAO
    texto = (msg + "\n" if msg else "") + \
        f"Dona Lúcia: \"Olá, {e.nome}! Veio vender ou comprar? Hoje {nome_item(e.em_alta)} está saindo a " \
        f"¢{e.preco(e.em_alta)}!\""
    ops = [
        Opcao("Vender itens do celeiro", lambda: vender_lista(h), ativa=bool(e.celeiro),
              dica="" if e.celeiro else "celeiro vazio"),
        Opcao(f"Comprar {q} de ração", lambda: comprar_racao(h), ativa=e.dinheiro >= preco,
              dica=f"¢{preco}", icone="racao"),
        Opcao("Comprar semente de abóbora gigante", lambda: comprar_abobora(h),
              ativa=e.pode_plantar_abobora() and e.dinheiro >= e.SEMENTE_ABOBORA,
              dica=(f"¢{e.SEMENTE_ABOBORA}" if e.pode_plantar_abobora()
                    else "só no começo do outono"), icone="abobora"),
        Opcao("Voltar à praça", lambda: praca(h)),
    ]
    return Tela(texto, ops, titulo="Mercado", local="cidade", retrato="lucia", painel="celeiro")


def comprar_abobora(h):
    h.e.plantar_abobora()
    return mercado(h, "Dona Lúcia entrega a semente com cuidado: \"Essa aqui é especial. "
                      "Rega todo santo dia até o Festival, senão ela murcha. Boa sorte!\"")


def comprar_racao(h):
    q, preco = PACOTE_RACAO
    h.e.dinheiro -= preco
    h.e.racao += q
    return mercado(h, f"Você comprou {q} de ração. Agora tem {h.e.racao}.")


def vender_lista(h, msg=""):
    e = h.e
    itens = sorted(e.celeiro.items(), key=lambda kv: -e.preco(kv[0]) * kv[1])
    total = sum(e.preco(i) * n for i, n in itens)
    ops = [Opcao("Vender TUDO", lambda: vender_tudo(h), ativa=bool(itens), dica=f"¢{total}")]
    for item, n in itens[:8]:
        ops.append(Opcao(f"{nome_item(item)} x{n}", lambda i=item: vender_item(h, i),
                         dica=f"¢{e.preco(item)} cada", icone=item))
    ops.append(Opcao("Voltar", lambda: mercado(h)))
    texto = (msg + "\n" if msg else "") + "O que você quer vender? (preços de hoje)"
    return Tela(texto, ops, titulo="Vender", local="cidade", retrato="lucia")


def _recibo(h, ganho, desc):
    xp = max(1, ganho // 25)
    return h.xp(xp, f"Você vendeu {desc} por ¢{ganho}. (+★{xp})")


def vender_tudo(h):
    e = h.e
    ganho = sum(e.vender(i, n) for i, n in list(e.celeiro.items()))
    return mercado(h, _recibo(h, ganho, "tudo o que tinha no celeiro"))


def vender_item(h, item):
    e = h.e
    n, preco = e.qtd(item), e.preco(item)

    def vender(qtd):
        ganho = e.vender(item, qtd)
        msg = _recibo(h, ganho, f"{qtd} {nome_item(item)}")
        return vender_lista(h, msg) if e.celeiro else mercado(h, msg)
    ops = [Opcao(f"Vender tudo (x{n})", lambda: vender(n), dica=f"¢{n * preco}")]
    if n >= 2:
        ops.append(Opcao(f"Vender metade (x{n // 2})", lambda: vender(n // 2), dica=f"¢{(n // 2) * preco}"))
    if n >= 3:
        ops.append(Opcao("Vender só 1", lambda: vender(1), dica=f"¢{preco}"))
    ops.append(Opcao("Guardar para depois", lambda: vender_lista(h)))
    dica = " Guarde alguns se tiver pedidos para entregar!" if any(item in p["itens"] for p in e.pedidos) else ""
    return Tela(f"Você tem {n} {nome_item(item)}. Dona Lúcia paga ¢{preco} cada.{dica}",
                ops, titulo="Vender", local="cidade", retrato="lucia")


# ---------------------------------------------------------------- feira de animais
def feira(h, msg=""):
    e = h.e
    ops = []
    for tipo, a in ANIMAIS.items():
        casa = a["casa"]
        livre = e.capacidade(casa) - e.ocupacao(casa)
        if a["nivel"] > e.nivel:
            ops.append(Opcao(a["nome"], lambda: feira(h), False, f"nível {a['nivel']}", a["produto"]))
        elif e.capacidade(casa) == 0:
            ops.append(Opcao(a["nome"], lambda: feira(h), False, "precisa de estábulo", a["produto"]))
        elif livre <= 0:
            ops.append(Opcao(a["nome"], lambda: feira(h), False, f"{casa} cheio", a["produto"]))
        else:
            ops.append(Opcao(a["nome"], lambda t=tipo: nomear(h, t), e.dinheiro >= a["preco"],
                             f"¢{a['preco']} · dá {nome_item(a['produto'])}", a["produto"]))
    ops.append(Opcao("Voltar à praça", lambda: praca(h)))
    texto = (msg + "\n" if msg else "") + \
        "Seu Zé: \"Bicho bom é bicho bem tratado! Todo dia precisa de ração, viu? Qual vai levar?\""
    return Tela(texto, ops, titulo="Feira de animais", local="cidade", retrato="ze")


def nomear(h, tipo):
    nome = ANIMAIS[tipo]["nome"].lower()

    def confirmar(apelido):
        h.e.comprar_animal(tipo, apelido[:12])
        return feira(h, h.xp(10, f"{apelido} agora mora na Fazenda Girassol! (+★10)"))
    return Tela(f"Que nome você dá para a sua nova {nome}?" if tipo in ("galinha", "vaca", "ovelha")
                else f"Que nome você dá para o seu novo {nome}?",
                [Opcao("Desistir", lambda: feira(h))], titulo="Batizado", local="cidade",
                retrato="ze", entrada=confirmar)


# ---------------------------------------------------------------- carpintaria
def carpintaria(h, msg=""):
    e = h.e
    ops = []
    n = len(e.canteiros)
    if n < CANTEIROS_MAX:
        p = canteiro_preco(n)
        ops.append(Opcao(f"Canteiro extra ({n}/{CANTEIROS_MAX})", lambda: comprar_canteiro(h),
                         e.dinheiro >= p, f"¢{p}"))
    for chave, c in CONSTRUCOES.items():
        if e.tem(chave):
            continue
        if c["nivel"] > e.nivel:
            ops.append(Opcao(c["nome"], lambda: carpintaria(h), False, f"nível {c['nivel']}"))
        else:
            ops.append(Opcao(c["nome"], lambda k=chave: construir(h, k), e.dinheiro >= c["preco"], f"¢{c['preco']}"))
    ops.append(Opcao("Voltar à praça", lambda: praca(h)))
    texto = (msg + "\n" if msg else "") + \
        "Rosa: \"Serragem, martelo e boa vontade! O que vamos construir na sua fazenda?\""
    return Tela(texto, ops, titulo="Carpintaria", local="cidade", retrato="rosa")


def comprar_canteiro(h):
    e = h.e
    e.dinheiro -= canteiro_preco(len(e.canteiros))
    e.canteiros.append(e._canteiro_vazio())
    return carpintaria(h, h.xp(8, "Rosa preparou mais um canteiro na sua plantação! (+★8)"))


def construir(h, chave):
    c = CONSTRUCOES[chave]
    preco = round(c["preco"] * h.e.desconto_obra())
    amiga = " (preço de amiga!)" if preco < c["preco"] else ""

    def sim():
        h.e.dinheiro -= preco
        h.e.construcoes.append(chave)
        return carpintaria(h, h.xp(25, f"Toc, toc, toc! {c['nome']} construído(a) na fazenda! (+★25)"))
    return Tela(f"Rosa: \"{c['nome']}: {c['desc']} Fica ¢{preco}{amiga}. Fechado?\"",
                [Opcao("Fechado! Pode construir", sim), Opcao("Vou pensar melhor", lambda: carpintaria(h))],
                titulo="Carpintaria", local="cidade", retrato="rosa")


# ---------------------------------------------------------------- pedidos
def pedidos(h, msg=""):
    e = h.e
    ops = []
    for i, p in enumerate(e.pedidos):
        ops.append(Opcao(f"Entregar para {p['cliente']}", lambda k=i: entregar(h, k), e.pode_entregar(p),
                         f"¢{p['moedas']} ★{p['xp']}"))
    if e.pedidos:
        ops.append(Opcao("Rasgar um pedido difícil", lambda: rasgar(h), dica="troca amanhã"))
    ops.append(Opcao("Voltar à praça", lambda: praca(h)))
    texto = (msg + "\n" if msg else "") + \
        "O quadro de avisos está cheio de papeizinhos. Pedidos pagam mais que o mercado e deixam a vila feliz (+♥)."
    return Tela(texto, ops, titulo="Quadro de pedidos", local="cidade", painel="pedidos")


def entregar(h, i):
    e = h.e
    p = e.entregar(i)
    extra = ""
    # quem pediu fica seu amigo: o quadro de pedidos ja tinha um "cliente",
    # so nao valia nada para a amizade
    chave = e.pessoa_do_cliente(p["cliente"])
    if chave:
        if e.mudar_amizade(chave, 4):
            extra = f" Vocês ficaram mais próximos! ({_cor(e, chave)})"
        else:
            extra = f" ({_cor(e, chave)})"
    return pedidos(h, h.xp(p["xp"], f"{p['cliente'].capitalize()} adorou! Você recebeu "
                                    f"¢{p['moedas']} e ★{p['xp']}.{extra}"))


def rasgar(h):
    ops = [Opcao(f"Rasgar o de {p['cliente']}", lambda k=i: _rasgar(h, k)) for i, p in enumerate(h.e.pedidos)]
    ops.append(Opcao("Não rasgar nada", lambda: pedidos(h)))
    return Tela("Qual pedido você tira do quadro? Um novo aparece amanhã.", ops,
                titulo="Quadro de pedidos", local="cidade", painel="pedidos")


def _rasgar(h, i):
    h.e.pedidos.pop(i)
    return pedidos(h, "Você tirou o pedido do quadro. Amanhã aparece outro.")


# ---------------------------------------------------------------- café
def cafe(h):
    e = h.e
    e.flags["cafe"] = e.dia
    e.dinheiro -= 15
    e.energia = min(e.energia_max, e.energia + 1)
    return praca(h, f"Você tomou um cafezinho com pão de queijo (+⚡1). Na mesa ao lado, alguém comenta: "
                    f"\"{random.choice(DICAS_CAFE)}\"")


# ---------------------------------------------------------------- gente do vale
def _cor(e, chave):
    cheios = e.coracoes(chave)
    return "♥" * cheios + "·" * (5 - cheios)


def gente(h, msg=""):
    """Quem está na praça hoje. Conversar é de graça; presente é que pesa."""
    e = h.e
    ops = []
    for chave, d in PESSOAS.items():
        visto = e.ja_viu_hoje(chave)
        festa = " ANIVERSÁRIO!" if e.aniversariante() == chave else ""
        ops.append(Opcao(d["nome"], lambda c=chave: pessoa(h, c),
                         dica=_cor(e, chave) + festa + ("  (já hoje)" if visto else "")))
    ops.append(Opcao("Voltar para a praça", lambda: praca(h)))
    texto = ((msg + NL if msg else "")
             + "A praça é o ponto de encontro do vale. Conversar não custa nada, e é conversando "
               "que você descobre do que cada um gosta.")
    return Tela(texto, ops, titulo="Gente do vale", local="cidade")


def pessoa(h, chave, msg=""):
    e = h.e
    d = PESSOAS[chave]
    linhas = [msg] if msg else []
    linhas.append(f"{d['nome']} · {_cor(e, chave)}")
    for tipo, verbo in (("adora", "Adora"), ("odeia", "Não suporta")):
        if e.sabe(chave, tipo):
            linhas.append(f"{verbo}: {nome_item(d[tipo])}.")
    if not e.sabe(chave, "adora") and not e.sabe(chave, "odeia"):
        linhas.append("Você ainda não sabe do que essa pessoa gosta.")
    for n, txt, tem in e.bonus_de(chave):
        # ■ conquistado, □ ainda não. A fonte não tem ✓ e trocaria por "?"
        linhas.append(("■ " if tem else f"□ {n}♥ ") + txt)
    ja = e.ja_viu_hoje(chave)
    ops = [
        Opcao("Conversar", lambda: conversar(h, chave), ativa=not ja,
              dica="já conversaram hoje" if ja else "+♥"),
        Opcao("Dar um presente", lambda: presentear(h, chave), ativa=not ja and bool(e.celeiro),
              dica="celeiro vazio" if not e.celeiro else ("já foi hoje" if ja else "")),
        Opcao("Voltar", lambda: gente(h)),
    ]
    return Tela(NL.join(linhas), ops, titulo=d["nome"], local="cidade", retrato=chave)


def conversar(h, chave):
    e = h.e
    d = PESSOAS[chave]
    e.marcar_visita(chave)
    subiu = e.mudar_amizade(chave, 2)
    # conversar é também como se descobre o gosto: primeiro o que a pessoa ama
    revelou = ""
    for tipo, frase in (("adora", "comenta que adora {}"), ("odeia", "faz careta e diz que detesta {}")):
        if e.descobrir(chave, tipo):
            revelou = " " + d["nome"] + " " + frase.format(nome_item(d[tipo])) + "."
            break
    msg = f"Vocês conversam um pouco.{revelou}"
    if subiu:
        msg += f" Vocês ficaram mais próximos! ({_cor(e, chave)})"
    return pessoa(h, chave, msg)


POR_PAGINA = 8   # mais que isso e a lista vaza da caixa e cobre o cenario


def presentear(h, chave, pag=0):
    """O celeiro pode ter mais de 20 tipos de item, e a lista inteira nao cabe
    na tela: ela vaza por cima do cenario. Entao vai em paginas, com o que a
    pessoa adora sempre na frente.
    """
    e = h.e
    d = PESSOAS[chave]
    sabe_adora = e.sabe(chave, "adora")
    sabe_odeia = e.sabe(chave, "odeia")

    def ordem(kv):
        return (0 if sabe_adora and kv[0] == d["adora"] else 1, -e.preco(kv[0]))

    itens = sorted(e.celeiro.items(), key=ordem)
    fatia = itens[pag * POR_PAGINA:(pag + 1) * POR_PAGINA]
    ops = []
    for i, n in fatia:
        marca = ""
        if sabe_adora and i == d["adora"]:
            marca = " ♥"
        elif sabe_odeia and i == d["odeia"]:
            marca = " (ela detesta)"
        ops.append(Opcao(f"{nome_item(i)} ({n}){marca}", lambda x=i: _dar(h, chave, x),
                         dica=f"vale ¢{e.preco(i)}", icone=i))
    if (pag + 1) * POR_PAGINA < len(itens):
        ops.append(Opcao("Ver o resto do celeiro", lambda: presentear(h, chave, pag + 1)))
    if pag:
        ops.append(Opcao("Voltar os itens", lambda: presentear(h, chave, pag - 1)))
    ops.append(Opcao("Melhor não", lambda: pessoa(h, chave)))
    quantos = f" ({pag * POR_PAGINA + 1}-{pag * POR_PAGINA + len(fatia)} de {len(itens)})" if len(itens) > POR_PAGINA else ""
    return Tela(f"O que você tira da cesta?{quantos}", ops,
                titulo=f"Presente para {d['nome']}", local="cidade",
                retrato=chave, painel="celeiro")


def _dar(h, chave, item):
    e = h.e
    d = PESSOAS[chave]
    e.remover(item, 1)
    e.marcar_visita(chave)
    if item == d["adora"]:
        pontos, reacao = 8, "Os olhos brilham! Era exatamente isso que faltava."
        e.descobrir(chave, "adora")
    elif item == d["odeia"]:
        pontos, reacao = -5, "O sorriso some na hora. Não era uma boa ideia..."
        e.descobrir(chave, "odeia")
    else:
        pontos, reacao = 3, "Um agrado sempre é bem-vindo."
    # presente no dia do aniversário vale o dobro (menos o que a pessoa odeia:
    # errar o presente justo hoje não devia render dobro de estrago)
    festa = e.aniversariante() == chave
    if festa and pontos > 0:
        pontos *= 2
        reacao += " E hoje é aniversário: você lembrou!"
    subiu = e.mudar_amizade(chave, pontos)
    msg = f"Você dá {nome_item(item)}. {reacao} ({_cor(e, chave)})"
    if subiu:
        msg += " Vocês ficaram mais próximos!"
    return pessoa(h, chave, msg)


# ------------------------------------------------- caderneta (só de olhar)
def caderneta(h, msg=""):
    """Tudo que você já sabe sobre o vale, de graça e sem sair de casa.

    A lista de gente na praça custa a ação de ir à cidade e só mostra coração.
    Aqui o jogador confere gosto, aniversário e o que falta destravar antes de
    decidir o que levar na cesta.
    """
    e = h.e
    ops = []
    for chave, d in PESSOAS.items():
        falta = next((f"falta {n}♥" for n, _, tem in e.bonus_de(chave) if not tem), "tudo destravado")
        ops.append(Opcao(f"{d['nome']} {_cor(e, chave)}", lambda c=chave: caderneta_pessoa(h, c),
                         dica=f"dia {d['aniversario']} · {falta}"))
    ops.append(Opcao("Fechar a caderneta", h.menu_fazenda))
    sabidos = sum(1 for c in PESSOAS for tp in ("adora", "odeia") if e.sabe(c, tp))
    texto = ((msg + NL if msg else "")
             + "Sua caderneta do vale, com tudo que você foi descobrindo sobre as pessoas daqui."
             + NL + f"Você já sabe {sabidos} de {len(PESSOAS) * 2} gostos. A fofoca do jornal revela um por dia.")
    return Tela(texto, ops, titulo="Caderneta do vale", local="fazenda")


def caderneta_pessoa(h, chave):
    e = h.e
    d = PESSOAS[chave]
    linhas = [f"{d['nome']} · {_cor(e, chave)}",
              f"Aniversário: dia {d['aniversario']} do ano (presente vale em dobro)."]
    for tipo, verbo in (("adora", "Adora"), ("odeia", "Não suporta")):
        linhas.append(f"{verbo}: {nome_item(d[tipo])}." if e.sabe(chave, tipo)
                      else f"{verbo}: ainda não descobri.")
    for n, txt, tem in e.bonus_de(chave):
        linhas.append(("■ " if tem else f"□ {n}♥ ") + txt)
    return Tela(NL.join(linhas), [Opcao("Voltar para a caderneta", lambda: caderneta(h))],
                titulo=d["nome"], local="fazenda", retrato=chave)
