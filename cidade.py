"""A cidade do vale: mercado, feira de animais, carpintaria, pedidos e café."""
import random

from config import (ANIMAIS, CANTEIROS_MAX, CONSTRUCOES, PACOTE_RACAO, canteiro_preco)
from estado import nome_item
from tela import Opcao, Tela

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
        Opcao("Voltar à praça", lambda: praca(h)),
    ]
    return Tela(texto, ops, titulo="Mercado", local="cidade", retrato="lucia", painel="celeiro")


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

    def sim():
        h.e.dinheiro -= c["preco"]
        h.e.construcoes.append(chave)
        return carpintaria(h, h.xp(25, f"Toc, toc, toc! {c['nome']} construído(a) na fazenda! (+★25)"))
    return Tela(f"Rosa: \"{c['nome']}: {c['desc']} Fica ¢{c['preco']}. Fechado?\"",
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
    p = h.e.entregar(i)
    return pedidos(h, h.xp(p["xp"], f"{p['cliente'].capitalize()} adorou! Você recebeu ¢{p['moedas']} e ★{p['xp']}. (+1 ♥)"))


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
