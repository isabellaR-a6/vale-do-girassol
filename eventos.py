"""Passeios (floresta, lago, vizinho) e eventos surpresa que acontecem de manhã."""
import random

from config import CULTURAS, ITENS
from estado import nome_item
from tela import Opcao, Tela


def sortear(tabela):
    return random.choices([t[0] for t in tabela], [t[1] for t in tabela])[0]


def voltar(h, msg):
    return Tela(msg, [Opcao("Voltar para a fazenda", h.menu_fazenda)])


# ---------------------------------------------------------------- floresta
def floresta(h):
    return Tela("Você entra na floresta. Folhas estalam sob os pés e um pica-pau trabalha lá no alto. "
                "A trilha se divide em três caminhos:", [
                    Opcao("Seguir o som do riacho", lambda: _floresta(h, "riacho")),
                    Opcao("Entrar entre as árvores antigas", lambda: _floresta(h, "antigas")),
                    Opcao("Procurar coisas no chão", lambda: _floresta(h, "chao")),
                ], titulo="Floresta", local="floresta")


def _floresta(h, caminho):
    e = h.e
    inverno = e.estacao == "Inverno"
    tabelas = {
        "riacho": [("amoras", 35), ("peixinho", 20), ("cachorro", 20), ("descanso", 15), ("sapo", 10)],
        "antigas": [("bau", 20), ("viajante", 25), ("cogumelos", 25), ("abelhas", 15), ("coruja", 15)],
        "chao": [("cogumelos", 45), ("amoras", 30), ("moeda", 15), ("trufa", 10)],
    }
    tabela = [t for t in tabelas[caminho] if not (t[0] == "cachorro" and (e.cachorro or e.flags.get("viu_cao")))]
    r = sortear(tabela)
    if r == "amoras" and inverno:
        r = "descanso"
    if r == "cogumelos" and e.estacao == "Outono":
        n = random.randint(3, 6)
    else:
        n = random.randint(2, 4)

    def ganha(item, qtd, texto):
        e.adicionar(item, qtd)
        return Tela(h.xp(4, texto + " (+★4)"), [Opcao("Voltar para a fazenda", h.menu_fazenda)],
                    titulo="Floresta", local="floresta")

    if r == "amoras":
        return ganha("amora", n, f"Você encontra um arbusto carregado e enche o bolso com {n} amoras. A boca fica roxa!")
    if r == "cogumelos":
        return ganha("cogumelo", n, f"Debaixo das folhas úmidas, {n} cogumelos bonitos. Vão valer uns trocados!")
    if r == "peixinho":
        return ganha("lambari", 2, "No riacho, você pega 2 lambaris com as mãos, igual a um urso.")
    if r == "trufa":
        return ganha("trufa", 1, "Seu nariz sente um cheiro forte... é uma trufa! Coisa rara e cara.")
    if r == "moeda":
        v = random.randint(10, 40)
        e.dinheiro += v
        return Tela(f"Algo brilha na terra: uma bolsinha esquecida com ¢{v}!", [Opcao("Voltar", h.menu_fazenda)],
                    titulo="Floresta", local="floresta", som="moeda")
    if r == "bau":
        v = random.randint(60, 180)
        e.dinheiro += v
        return Tela(h.xp(10, f"Entre as raízes de uma árvore gigante, um baú velho! Dentro: ¢{v} em moedas antigas. (+★10)"),
                    [Opcao("Voltar", h.menu_fazenda)], titulo="Floresta", local="floresta", som="moeda")
    if r == "descanso":
        e.energia = min(e.energia_max, e.energia + 1)
        return Tela("Você senta numa pedra, molha os pés na água gelada e respira fundo. Que paz! (+⚡1)",
                    [Opcao("Voltar", h.menu_fazenda)], titulo="Floresta", local="floresta")
    if r == "sapo":
        return Tela(h.xp(2, "Um sapo gordo pula no seu pé e você grita tão alto que os pássaros fogem. "
                            "Pelo menos rendeu uma boa história. (+★2)"),
                    [Opcao("Voltar", h.menu_fazenda)], titulo="Floresta", local="floresta")
    if r == "abelhas":
        e.gastar_energia()
        return Tela("Você mexeu numa colmeia sem querer! Correu tanto que ficou exausto(a). (-⚡1)",
                    [Opcao("Voltar", h.menu_fazenda)], titulo="Floresta", local="floresta", som="erro")
    if r == "coruja":
        return Tela(h.xp(15, "Uma coruja enorme te encara em silêncio... e você sente que aprendeu algo "
                             "sobre a vida no campo. (+★15)"),
                    [Opcao("Voltar", h.menu_fazenda)], titulo="Floresta", local="floresta")
    if r == "cachorro":
        return cachorro(h, "floresta")
    return viajante(h, "floresta")


def cachorro(h, local):
    e = h.e
    e.flags["viu_cao"] = True

    def adotar(nome):
        e.cachorro = nome[:12]
        return Tela(h.xp(10, f"{e.cachorro} pula no seu colo e lambe sua cara inteira. Agora você tem um cão de guarda! "
                             "Raposas vão pensar duas vezes. (+★10)"),
                    [Opcao("Voltar para a fazenda", h.menu_fazenda)], retrato="cachorro", titulo="Novo amigo",
                    local=local)

    def nomear():
        return Tela("Que nome você dá para o filhote?", [
            Opcao("Paçoca", lambda: adotar("Paçoca")), Opcao("Biscoito", lambda: adotar("Biscoito")),
            Opcao("Pipoca", lambda: adotar("Pipoca") if not any(a["nome"] == "Pipoca" for a in e.animais)
                  else adotar("Pipoquinha"))],
            retrato="cachorro", titulo="Novo amigo", local=local, entrada=adotar)
    return Tela("Um filhote caramelo e magrinho sai do mato, abanando o rabo. Ele parece perdido... "
                "e está olhando para você com olhos pidões.", [
                    Opcao("Levar para casa", nomear),
                    Opcao("Dar um pedaço do lanche e seguir", lambda: voltar(h, "O filhote come e some no mato. "
                                                                               "Talvez vocês se encontrem de novo...")),
                ], retrato="cachorro", titulo="Um filhote!", local=local)


def viajante(h, local):
    e = h.e

    def comprar(preco):
        e.dinheiro -= preco
        e.flags["semente_magica"] = True
        return voltar(h, f"Você paga ¢{preco} e recebe uma semente que brilha no escuro. \"Plante... e espere\", "
                         "diz o viajante, sumindo na neblina. (Ela aparece no menu da plantação.)")

    def pechinchar():
        if random.random() < 0.5:
            return Tela("O viajante ri baixinho. \"Gosto de gente esperta. Leve por ¢70.\"",
                        [Opcao("Pagar ¢70", lambda: comprar(70), e.dinheiro >= 70),
                         Opcao("Recusar", lambda: voltar(h, "Você agradece e segue seu caminho."))],
                        retrato="viajante", titulo="Viajante misterioso", local=local)
        return voltar(h, "\"Pechinchar com o destino? Que pena...\" Ele se vira e desaparece. Só sobrou um cheiro de canela.")

    if e.flags.get("semente_magica") or e.flags.get("magica_plantada"):
        return voltar(h, "Você vê uma capa roxa ao longe, mas quando chega perto não há ninguém. Estranho...")
    return Tela("Um viajante de capa roxa surge do nada. \"Tenho uma Semente Mágica, criança da terra. "
                "Dizem que dá a maior abóbora que este vale já viu. Custa ¢120.\"", [
                    Opcao("Comprar a semente", lambda: comprar(120), e.dinheiro >= 120, "¢120"),
                    Opcao("Pechinchar", pechinchar, dica="arriscado"),
                    Opcao("Recusar educadamente", lambda: voltar(h, "\"Como quiser...\" A neblina engole o viajante.")),
                ], retrato="viajante", titulo="Viajante misterioso", local=local)


# ---------------------------------------------------------------- o cachorro
ACHADOS_CAO = [("amora", "chega abanando o rabo com uma amora na boca"),
               ("cogumelo", "aparece todo sujo de terra, com um cogumelo entre os dentes"),
               ("lambari", "volta pingando do córrego, com um lambari"),
               ("trufa", "cava feito doido embaixo da árvore e desenterra uma trufa!")]


def carinho(h):
    """Um carinho por dia. Não custa energia: é afago, não tarefa."""
    e = h.e
    e.flags["carinho"] = e.dia
    nome = e.cachorro
    if random.random() < 0.35:
        item, conta = random.choice(ACHADOS_CAO)
        e.adicionar(item, 1)
        msg = h.xp(3, f"{nome} {conta}. Presente para você! (+1 {nome_item(item)}, +★3)")
    else:
        msg = h.xp(2, f"{nome} se joga de barriga para cima e fica de perna bamba. "
                      f"O dia melhora um pouquinho. (+★2)")
    return Tela(msg, [Opcao("Voltar para a fazenda", h.menu_fazenda)],
                retrato="cachorro", titulo=nome, local="fazenda")


# ---------------------------------------------------------------- lago
def lago(h):
    gelo = h.e.estacao == "Inverno"
    texto = ("O lago está congelado! Você faz um buraquinho no gelo para pescar. " if gelo else
             "O lago brilha com o sol e um peixe pula lá no meio. ") + "Onde você joga o anzol?"
    return Tela(texto, [
        Opcao("Pescar do píer", lambda: _pescar(h, "pier"), dica="seguro"),
        Opcao("Remar até o meio do lago", lambda: _pescar(h, "meio"), dica="arriscado"),
    ], titulo="Lago", local="lago")


def _pescar(h, lugar):
    e = h.e
    if lugar == "pier":
        r = sortear([("lambari", 55), ("tilapia", 25), ("bota", 15), ("nada", 5)])
    else:
        # cair era 15% e "bota" 20%: 35% das idas ao meio nao rendiam nada, e
        # cair ainda tirava energia por cima da acao ja gasta. O risco continua,
        # mas nao empilha mais punicao — quem cai volta com alguma coisa.
        r = sortear([("tilapia", 45), ("dourado", 12), ("bota", 15), ("cair", 10), ("lambari", 18)])
    if r == "lambari":
        n = random.randint(1, 3)
        e.adicionar("lambari", n)
        msg = h.xp(3, f"Beliscou! Você pega {n} lambari(s). Pequenos, mas gostosos fritinhos. (+★3)")
    elif r == "tilapia":
        n = random.randint(1, 2)
        e.adicionar("tilapia", n)
        msg = h.xp(6, f"A vara enverga! {n} tilápia(s) bem gordinha(s)! (+★6)")
    elif r == "dourado":
        e.adicionar("peixe_dourado", 1)
        msg = h.xp(25, "Depois de uma briga épica, você puxa um PEIXE DOURADO! Dizem que dá sorte... e dinheiro. (+★25)")
    elif r == "bota":
        msg = "Você fisga algo pesado... é uma bota velha. Pelo menos o lago ficou mais limpo."
    elif r == "cair":
        e.gastar_energia()
        e.adicionar("lambari", 1)
        msg = ("O barco balança e você cai na água! Sai de lá pingando e com frio... mas com um "
               "lambari teimoso agarrado na camisa. (-⚡1, +1 lambari)")
    else:
        msg = "Nenhum peixe quis conversa hoje. Mas o pôr do sol valeu a pena."
    return Tela(msg, [Opcao("Voltar para a fazenda", h.menu_fazenda)], titulo="Lago", local="lago",
                som="moeda" if r in ("dourado", "tilapia") else "")


# ---------------------------------------------------------------- vizinho
FALAS_ZE = [
    "Sua avó me ensinou a plantar girassol. Mulher danada, a Cida!",
    "O segredo da terra é paciência. E esterco. Muito esterco.",
    "Quando eu era moço, o vale inteiro vinha no Festival da Colheita. Ainda vem!",
    "Minha vaca Mimosa já ganhou três concursos. Hoje ela só quer saber de dormir.",
    "Dizem que tem um viajante de capa roxa que aparece por aí... Eu nunca vi. Ou vi?",
]


def vizinho(h):
    e = h.e
    amizade = e.flags.get("ze", 0)
    fala = FALAS_ZE[amizade % len(FALAS_ZE)]
    return Tela(f"Seu Zé está sentado na varanda, entre os girassóis. \"Opa! Chegue, {e.nome}! {fala}\"", [
        Opcao("Ajudar na colheita de girassol", lambda: _ze(h, "ajudar"), e.energia >= 1,
              "⚡1 · +¢45" if e.energia >= 1 else "sem energia"),
        Opcao("Tomar um café e prosear", lambda: _ze(h, "prosa")),
        Opcao("Pedir um conselho", lambda: _ze(h, "conselho")),
    ], titulo="Sítio do Seu Zé", local="vizinho", retrato="ze")


def _ze(h, acao):
    e = h.e
    e.flags["ze"] = e.flags.get("ze", 0) + 1
    amizade = e.flags["ze"]
    if acao == "ajudar":
        e.gastar_energia()
        e.dinheiro += 45
        e.reputacao += 1
        msg = "Vocês colhem girassóis até o sol baixar. Seu Zé te paga ¢45 e um abraço apertado. (+1 ♥)"
    elif acao == "prosa":
        msg = "Café passado na hora, bolo de milho e muita história. Você volta pra casa com o coração quentinho."
    else:
        msg = "Seu Zé coça a barba: \"" + conselho(e) + "\""
    presentes = {2: ("racao", 15, "um saco de ração"), 4: ("cenoura", 4, "4 cenouras da horta dele"),
                 6: ("geleia", 1, "um pote da geleia famosa da falecida Dona Nena"),
                 8: ("queijo", 2, "2 queijos curados")}
    if amizade in presentes:
        item, n, desc = presentes[amizade]
        e.adicionar(item, n)
        e.reputacao += 1
        msg += f"\nNa saída, ele insiste: \"Leve isto!\" Você ganhou {desc}. (+1 ♥)"
    if amizade == 5 and not e.cachorro and not e.flags.get("viu_cao"):
        msg += "\n\"Ah, e minha cadela teve filhotes... quer um?\""
        return Tela(msg, [Opcao("Quero sim!", lambda: cachorro(h, "vizinho")),
                          Opcao("Agora não, obrigado(a)", h.menu_fazenda)],
                    titulo="Sítio do Seu Zé", local="vizinho", retrato="ze")
    return Tela(h.xp(3, msg), [Opcao("Voltar para a fazenda", h.menu_fazenda)],
                titulo="Sítio do Seu Zé", local="vizinho", retrato="ze")


def conselho(e):
    if e.precisa_regar():
        return "Tem planta com sede na sua roça! Planta sem água duas noites... já era."
    if e.animais and any(not a["alimentado"] for a in e.animais) and e.racao < 5:
        return "Bicho com fome não produz. Compre ração no mercado ou construa um moinho."
    if not e.tem("estabulo") and e.nivel >= 2:
        return "Com um estábulo você pode criar porcos e vacas. Aí sim o dinheiro entra!"
    if e.estacao == "Outono" and not e.tem("estufa"):
        return "O inverno vem aí. Sem estufa, a terra congela. Aproveite para cuidar dos bichos."
    if not e.receitas_disponiveis():
        return "Vender trigo cru é bom, mas vender pão é melhor. Pense numa padaria!"
    return "Você está indo muito bem. Só não esqueça de descansar, viu?"


# ---------------------------------------------------------------- eventos da manhã
CARTAS = {
    8: "Oi! Chegou o Verão. Faz calor, então regue sempre. E cuidado com as tempestades de verão!",
    15: "O Outono é a estação dos cogumelos na floresta. E no fim dele (dia 21) tem o Festival da Colheita! "
        "Leve o seu melhor produto.",
    22: "O Inverno chegou. Confesso um segredo: debaixo da tábua solta do celeiro, guardei uma lata. "
        "Considere um presente. Beijos! (Você encontrou ¢300!)",
}


def da_manha(h):
    e = h.e
    # Estes marcos sao do ANO, nao do jogo: com o calendario passando de 28, usar
    # e.dia faria o festival e as cartas acontecerem so no primeiro ano.
    if e.dia_do_ano in CARTAS and not e.flags.get(f"carta{e.dia_do_ano}"):
        e.flags[f"carta{e.dia_do_ano}"] = True
        if e.dia_do_ano == 22:
            e.dinheiro += 300
        return Tela(f"Bom dia! Tem uma carta na caixa do correio...\n\"{CARTAS[e.dia_do_ano]}\" - Vovó Cida",
                    [Opcao("Guardar a carta", h.menu_fazenda)], titulo="Carta da Vovó", retrato="vovo",
                    som="moeda" if e.dia_do_ano == 22 else "")
    if e.dia_do_ano == 21 and e.flags.get("festival") != e.ano:
        e.flags["festival"] = e.ano
        return festival(h)
    if e.dia_do_ano < 3 or random.random() > 0.45:
        return None
    possiveis = ["limonada", "lucia", "estrelas"]
    galinhas = [a for a in e.animais if a["tipo"] in ("galinha", "pato")]
    if galinhas and not e.cachorro:
        possiveis += ["raposa", "raposa"]
    if e.clima == "tempestade" and any(c["cultura"] and not c["morto"] for c in e.canteiros):
        possiveis += ["tempestade"] * 4
    if any(a["tipo"] == "porco" for a in e.animais):
        possiveis.append("porco")
    if galinhas and e.ocupacao("galinheiro") < e.capacidade("galinheiro"):
        possiveis.append("pintinho")
    if not e.flags.get("semente_magica") and not e.flags.get("magica_plantada"):
        possiveis.append("viajante")
    return EVENTOS[random.choice(possiveis)](h)


def _raposa(h):
    e = h.e

    def guarda():
        e.gastar_energia()
        return voltar(h, h.xp(8, "Você passa a madrugada de lanterna na mão. A raposa aparece, leva um susto e foge! (+★8)"))

    def cerca():
        e.dinheiro -= 60
        return voltar(h, "Você reforça a cerca do galinheiro. Nenhuma raposa passa por ali hoje!")

    def ignorar():
        galinhas = [a for a in e.animais if a["tipo"] in ("galinha", "pato")]
        if galinhas and random.random() < 0.4:
            vitima = random.choice(galinhas)
            e.animais.remove(vitima)
            return voltar(h, f"De manhã, o galinheiro está bagunçado e cheio de penas... {vitima['nome']} sumiu. "
                             "Um cachorro ajudaria a proteger os animais.")
        return voltar(h, "A raposa ronda, ronda... e vai embora. Foi sorte!")
    return Tela("Bom dia! Você encontra pegadas de raposa em volta do galinheiro. Ela vai voltar hoje à noite...", [
        Opcao("Montar guarda à noite", guarda, e.energia >= 1, "⚡1"),
        Opcao("Reforçar a cerca", cerca, e.dinheiro >= 60, "¢60"),
        Opcao("Deixar pra lá", ignorar, dica="arriscado"),
    ], titulo="Pegadas!")


def _tempestade(h):
    e = h.e

    def cobrir():
        e.gastar_energia(2)
        return voltar(h, h.xp(6, "Você cobre os canteiros com lona debaixo de trovões. Tudo salvo! (+★6)"))

    def torcer():
        vivos = [c for c in e.canteiros if c["cultura"] and not c["morto"]]
        perdidos = random.sample(vivos, k=len(vivos) // 2) if random.random() < 0.5 else []
        for c in perdidos:
            c["morto"] = True
        if perdidos:
            return voltar(h, f"O vento arrancou {len(perdidos)} planta(s). Que tristeza...")
        return voltar(h, "A tempestade passou raspando. Suas plantas estão inteiras!")
    return Tela("Bom dia! O céu está roxo e o vento uiva. Uma tempestade forte vem aí e sua plantação está exposta.", [
        Opcao("Cobrir tudo com lona", cobrir, e.energia >= 2, "⚡2"),
        Opcao("Torcer para passar", torcer, dica="50% de perder metade"),
    ], titulo="Tempestade!")


def _limonada(h):
    e = h.e

    def comprar():
        e.dinheiro -= 5
        e.energia = min(e.energia_max, e.energia + 1)
        e.reputacao += 1
        return voltar(h, "Geladinha e azedinha! Bia sorri de orelha a orelha. (+⚡1, +1 ♥)")
    return Tela("Bom dia! Bia, a menina do sítio vizinho, montou uma barraquinha de limonada na porteira. "
                "\"Moço(a), quer uma? Só ¢5!\"", [
                    Opcao("Comprar uma limonada", comprar, e.dinheiro >= 5, "¢5 · +⚡1"),
                    Opcao("Hoje não, obrigado(a)", lambda: voltar(h, "Bia dá de ombros e grita para o próximo que passa.")),
                ], retrato="bia", titulo="Limonada!")


def _lucia(h):
    e = h.e

    def ajudar():
        e.gastar_energia()
        e.dinheiro += 40
        e.reputacao += 2
        return voltar(h, "Vocês trocam a roda juntas(os). Dona Lúcia te dá ¢40 e diz que você é gente de ouro. (+2 ♥)")

    def recusar():
        e.reputacao = max(0, e.reputacao - 1)
        return voltar(h, "Dona Lúcia suspira e segue empurrando a carroça sozinha. (-1 ♥)")
    return Tela("Bom dia! A carroça da Dona Lúcia quebrou bem na frente da sua porteira, carregada de verduras.", [
        Opcao("Ajudar a consertar", ajudar, e.energia >= 1, "⚡1 · +♥♥"),
        Opcao("Dizer que está sem tempo", recusar),
    ], retrato="lucia", titulo="Carroça quebrada")


def _estrelas(h):
    e = h.e

    def pedido(tipo):
        if tipo == "dinheiro":
            e.dinheiro += 50
            return voltar(h, "Na manhã seguinte você acha ¢50 no bolso de uma calça velha. Coincidência?")
        if tipo == "colheita":
            for c in e.canteiros:
                if c["cultura"] and not c["morto"] and not e.maduro(c):
                    c["dias"] += 1
            return voltar(h, "As plantas parecem ter crescido um pouquinho durante a madrugada...")
        e.reputacao += 2
        return voltar(h, "Hoje todo mundo parece sorrir para você. (+2 ♥)")
    return Tela("Você acordou antes do sol e viu uma chuva de estrelas cadentes sobre o vale! Dá tempo de fazer um pedido...", [
        Opcao("Pedir dinheiro", lambda: pedido("dinheiro")),
        Opcao("Pedir uma boa colheita", lambda: pedido("colheita")),
        Opcao("Pedir amigos", lambda: pedido("amigos")),
    ], local="noite", titulo="Estrelas cadentes")


def _porco(h):
    h.e.adicionar("trufa", 1)
    porco = next(a for a in h.e.animais if a["tipo"] == "porco")
    return voltar(h, f"Bom dia! {porco['nome']} passou a noite fuçando e achou uma trufa extra! Que porquinho esperto.")


def _pintinho(h):
    e = h.e

    def nomear(nome):
        e.animais.append({"tipo": "galinha", "nome": nome[:12], "alimentado": False, "feliz": 3,
                          "progresso": 0, "pronto": False})
        return voltar(h, h.xp(5, f"{nome} já está ciscando pelo curral! (+★5)"))
    return Tela("Bom dia! Um ovo chocou no galinheiro e saiu um pintinho amarelinho! Como ele vai se chamar?",
                [Opcao("Deixar sem nome", lambda: nomear("Pintinho"))], titulo="Pio, pio!", entrada=nomear)


def festival(h):
    e = h.e
    candidatos = sorted((i for i in e.celeiro if i in CULTURAS or i in ("ovo", "leite", "la", "trufa", "queijo",
                                                                        "pao", "bolo", "geleia", "abobora_gigante")),
                        key=lambda i: -ITENS[i][1])[:6]

    def inscrever(item):
        nota = ITENS[item][1] * random.uniform(0.8, 1.3) + e.reputacao * 6
        e.remover(item, 1)
        if nota >= 300:
            premio, lugar = 600, "1º lugar"
        elif nota >= 120:
            premio, lugar = 250, "2º lugar"
        else:
            premio, lugar = 80, "menção honrosa"
        e.dinheiro += premio
        e.reputacao += 2
        return Tela(h.xp(30, f"Os jurados provam, cheiram, cochicham... e o seu {nome_item(item)} leva o {lugar}! "
                             f"Prêmio: ¢{premio}. A vila inteira aplaude! (+★30, +2 ♥)"),
                    [Opcao("Voltar para a fazenda", h.menu_fazenda)], local="festa", retrato="prefeito",
                    titulo="Festival da Colheita", som="fanfarra")
    def inscrever_gigante():
        peso = e.peso_abobora()
        e.abobora = None
        if peso >= 60:
            premio, lugar = 1200, "CAMPEÃ DO VALE"
            e.adicionar("abobora_gigante", 1)
        elif peso >= 40:
            premio, lugar = 600, "2º lugar"
        elif peso >= 25:
            premio, lugar = 300, "3º lugar"
        else:
            premio, lugar = 120, "menção honrosa"
        e.dinheiro += premio
        e.reputacao += 3
        e.mudar_amizade("prefeito", 5)
        return Tela(h.xp(40, f"Quatro homens carregam a sua abóbora até a balança. O ponteiro sobe, sobe... "
                             f"{peso} KG! O Prefeito Otávio grita: {lugar}! Prêmio: ¢{premio}. "
                             f"(+★40, +3 ♥ na vila)"),
                    [Opcao("Voltar para a fazenda", h.menu_fazenda)], local="festa", retrato="prefeito",
                    titulo="Concurso da Abóbora Gigante", som="fanfarra")

    ops = []
    if e.abobora:
        ops.append(Opcao(f"Inscrever a ABÓBORA GIGANTE · {e.peso_abobora()} kg", inscrever_gigante,
                         icone="abobora"))
    ops += [Opcao(f"Inscrever: {nome_item(i)}", lambda k=i: inscrever(k), icone=i) for i in candidatos]
    ops.append(Opcao("Só assistir e comer pamonha", lambda: voltar(h, "Você come três pamonhas e dança quadrilha. Que festa!")))
    texto = "Bom dia! Hoje é o FESTIVAL DA COLHEITA! A praça está enfeitada e o prefeito chama os fazendeiros " \
            "para o concurso. Qual produto seu vai para a mesa dos jurados?"
    if not candidatos:
        texto += " (Seu celeiro está vazio... dá para só curtir a festa.)"
    return Tela(texto, ops, local="cidade", retrato="prefeito", titulo="Festival da Colheita", painel="celeiro")


EVENTOS = {"raposa": _raposa, "tempestade": _tempestade, "limonada": _limonada, "lucia": _lucia,
           "estrelas": _estrelas, "porco": _porco, "pintinho": _pintinho,
           "viajante": lambda h: viajante(h, "fazenda")}
