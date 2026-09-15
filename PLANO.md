# Plano do Vale do Girassol

Conversa de 12/09/2026 (madrugada). A pergunta que começou tudo: *"queria alguma
coisa pra ficar emocionante, tipo 'resolvo isso e vou dormir' e passam 4 horas."*

Este arquivo tem duas partes: **o que fazer no próximo dia de trabalho** e **a
fila do que vem depois**, pra nenhuma ideia se perder.

---

## Como retomar (inclusive de outra máquina)

```bash
git pull
python main.py                    # jogar
python tools/checar_texto.py      # antes de commitar texto: acusa o que virar "?"
python tools/gerar_icone.py       # redesenha o ícone do app
```

**Antes de mexer, leia as pegadinhas no `CLAUDE.md`** — elas já custaram tempo:
a fonte troca caractere desconhecido por "?" sem avisar, `j.ui.tela` não é
`j.tela`, e tirar foto sem `ui.atualizar(dt)` sai com a caixa de diálogo vazia.

**O que falta está em "A fila", mais abaixo.** As três do topo e quase tudo da
fila saíram em 12/09/2026; sobraram o trem, as ferramentas e o teclado do
Android.

## O diagnóstico

O jogo não sofre de falta de conteúdo. Sofre de duas coisas medidas no código:

**1. `ENERGIA_BASE = 5`.** Cinco ações por dia. Plantar, regar, colher, cuidar dos
animais e ir à cidade já são cinco. A floresta, o lago, o vizinho, os cinco
lugares da cidade e os eventos existem — mas o jogador **não tem energia pra ir**
sem abandonar a fazenda. Não falta o que fazer: não sobra com o que fazer.

Os dois remédios que existem estão longe demais: irrigação ¢700 e reforma da
casa ¢800 para dar **+1** de energia, no nível 3.

**2. O jogo tem três anos de conteúdo espremidos em 28 dias.** São 6 culturas,
4 animais, 8 construções e 6 receitas, com coisas pedindo nível 4 e 5 e preços de
¢600 a ¢900, num ano de 28 dias que começa com ¢500. A estufa, o laticínio, a
ovelha, o queijo e a geleia provavelmente nenhum jogador vê.

---

## Próximo dia de trabalho — três coisas, nesta ordem

> **FEITO em 12/09/2026.** As três saíram. O que a fila abaixo guarda continua valendo.

A ordem importa: **energia primeiro**. Sem ela, qualquer conteúdo novo é mais uma
coisa que o jogador não consegue alcançar.

### 1. Energia e comida que restaura ✅

- Comida vira item consumível: pão, bolo, geleia e queijo devolvem energia.
  Hoje eles só servem pra vender.
- Efeito de projeto: a cadeia de produção deixa de ser "outra forma de ganhar
  dinheiro" e vira a forma de **comprar tempo**, que é o recurso escasso de
  verdade. Trigo → pão → uma ação a mais no dia. É a espinha do Stardew.
- Rever `ENERGIA_BASE` e o preço/nível da reforma da casa.
- **Dizer o que o clima já faz:** a chuva já rega os canteiros de graça
  (`estado.py:161`). A frase já existia; agora ela diz o que isso significa
  ("sobrou uma ação no seu dia").

Arquivos: `config.py` (ENERGIA_BASE, itens comestíveis), `estado.py`
(consumir comida), `historia.py` (opção de comer, relatório da manhã).

### 2. Os anos, com o Concurso como placar ✅

- Deixar o `dia` crescer sem parar. `ano = (dia - 1) // 28 + 1` e
  `dia_do_ano = (dia - 1) % 28 + 1`. **As estações já ciclam sozinhas**, porque
  `estacao` já usa `% 4`.
- Fazer o Concurso da Fazenda do Ano acontecer **todo** ano. Hoje ele dispara uma
  vez só, porque `fim_do_ano` exige `not modo_livre`.
- Guardar a pontuação de cada ano e mostrar o histórico na cerimônia:
  `Ano 1 — 2.340 — Aconchegante` / `Ano 2 — 5.120 — Próspera ↑`. É o placar
  pessoal que faz querer jogar mais um ano.
- Mostrar "Ano 2 · Verão · Dia 3" na interface.

Arquivos: `estado.py` (`ano`, `fim_do_ano`, histórico no save), `historia.py`
(`final_ano`), `interface.py` (HUD).

### 3. O bonequinho personalizável ✅

**O motor já existe e só é usado pelos outros personagens.** `RETRATOS` não
guarda desenhos: ele *gera* cada retrato a partir de pele, cor de cabelo, estilo
(coque, curto, longo, careca), óculos, barba, bigode, chapéu e roupa. E
`pessoa(cabelo, roupa, calca)` já recebe as cores como parâmetro.

Falta só a tela de criação e guardar as escolhas no save.

Arquivos: `sprites.py` (reaproveitar `retrato`), `historia.py` (tela de criação,
logo depois de escolher o nome), `estado.py` (guardar a aparência).

---

## A fila — depois, em cima de um jogo onde já dá pra respirar

### Amizade por pessoa ✅ (12/09/2026) — com os prêmios, na segunda leva

Hoje existe **uma** `reputacao` global. Mas o jogo tem **sete personagens com
retrato**: Vovó Cida, Zé, Lúcia, Rosa, o viajante, o Prefeito Otávio e a Bia.

- Amizade individual, com item preferido **e item odiado** por pessoa
- Aba **"Conversar"**, separada de comprar e vender: é conversando que se
  descobre o gosto de cada um
- **Proteção contra injustiça:** o personagem reage antes de aceitar ("a Vovó
  olha torto pro peixe...") e dá pra voltar atrás. Errar vira escolha, não
  armadilha
- Amizade destrava coisa concreta: receita da Lúcia, desconto da Rosa, semente
  rara do viajante
- Aniversários, com data no calendário de 28 dias

Efeito: os itens ganham um terceiro uso. Vender, comer e **presentear**.

### O jornal da cidade ✅ (12/09/2026) — a Gazeta do Vale

Substitui a ideia de "carta". Uma tela só, de manhã, com:
- **Coluna de fofoca** — é daqui que saem as dicas de gosto dos personagens.
  Resolve o problema de descoberta da amizade sem precisar de sistema novo
- Previsão do tempo do dia
- Avisos: festival chegando, o que a feira vai ter

É também o **gancho do amanhã**: o jogador dorme sabendo que tem algo esperando.

### O inverno como estação social ✅ (12/09/2026)

Hoje o inverno são **7 dias por ano em que nada cresce** sem estufa (¢900, nível 4).
O jogador fica olhando terra congelada. Isso é um problema — ou uma oportunidade.

A ideia: em vez de "a estação em que não dá para jogar", virar **"a estação em que
se joga diferente"**. O inverno é quando se cozinha, se visita as pessoas, se faz
artesanato, se fica perto do fogo.

Peças possíveis (não é para fazer todas):
- Receitas que **só existem no inverno** (sopa quente, chocolate, conserva)
- As pessoas ficam mais tempo em casa: conversar rende mais amizade
- Um evento de fim de ano na praça, com fogueira
- Trabalho de dentro de casa: tricô com a lã da ovelha, conserto de ferramentas
- Vender conserva feita no outono por preço melhor no inverno

O importante é que o jogador **queira** que chegue o inverno, em vez de aguentar.

### Decorar a fazenda ✅ (12/09/2026)

Depois que tudo está construído, dinheiro vira número. Falta **coisa cara e bonita
para querer**: o que não dá lucro, dá gosto.

- Cerca pintada, caminho de pedra, canteiro de flores, balanço na árvore,
  espantalho, lampião, caixa de correio nova
- Cada uma aparece no cenário desenhado (`cenario.py` já desenha a fazenda)
- Sem efeito em dinheiro: efeito em **olhar para a própria fazenda e gostar**
- Talvez um bônus pequeno de reputação, para o Concurso do fim do ano notar

É o sumidouro de dinheiro que falta, e o motivo para continuar jogando depois de
ter construído tudo que é útil.

### Ver o acessório antes de escolher (pedido da Isabella, 14/09/2026)

**O problema:** na criação do personagem (`historia.py`, de `criar_pessoa` até
`escolher_oculos`) cada opção é só um nome — "Tiara", "Laço", "Bandana". O
retrato no canto (`retrato="jogador"`) só muda **depois** de escolher. Quem não
conhece o jogo não tem como adivinhar como fica, e escolhe no escuro.

**A ideia:** o retrato mostrar a opção **marcada**, não só a escolhida.
- No computador: passar o mouse ou as setas por cima já troca o retrato.
- No celular não existe "passar por cima": o **primeiro toque** marca e mostra no
  retrato, o **segundo toque** na mesma opção confirma. (Mesmo jeito de
  loja de roupa em jogo de celular.)
- Vale para todas as telas de aparência: pele, estilo, cor, roupa, cabeça,
  brinco, colar e óculos.
- Onde mexer: a UI já sabe qual opção está marcada (`UI.sel`); falta a tela de
  aparência avisar o `sprites.definir_jogador` com a opção marcada, e voltar ao
  que estava se a pessoa desistir.

Tamanho: pequeno. Não muda save nem regra do jogo.

### Teclado no celular ✅ no iPhone (14/09/2026) — falta conferir no APK

**Achado pela Isabella jogando o APK.** No celular o teclado do sistema não abre,
então nenhuma tela de digitar funciona. Na web isso já estava resolvido
(`interface.py:107` abre a caixinha do navegador, que chama o teclado); no APK
não existe navegador nenhum.

**No iPhone (14/09) o teclado abriu** — mas sozinho, assim que a tela de nome
aparecia, e cobria a pergunta inteira. Agora a caixa mostra "toque aqui para
digitar", o teclado só abre no toque, o jogo avisa o SDL onde está a caixa
(`set_text_input_rect`, para ele empurrar a tela para cima) e o "retorno" com a
caixa vazia esconde o teclado. **Conferido no iPhone pela Isabella: a tela sobe
junto com o teclado e a caixa fica à vista.** Falta só testar isso no APK.

**O pior já foi contornado (12/09):** as quatro telas que pedem texto agora têm
alternativa sem teclado. A de batizar animal comprado na feira era a única sem
saída além de "Desistir" — ela travava a feira inteira no celular, e ganhou três
nomes sorteados. O APK é jogável do começo ao fim; só não dá nome próprio.

**Tentativa feita em 12/09:** o `interface.nova_tela` agora chama
`pygame.key.start_text_input()` quando a tela aceita texto (e `stop` quando não).
No computador o teclado já está sempre ligado, mas no celular o SDL só mostra o
teclado da tela quando o programa pede — e o jogo nunca pedia. É a causa mais
provável, e o mesmo conserto valeria para iPhone e Android.

**Continua na fila porque não foi verificado:** conferi que digitar continua
funcionando no computador, mas se resolve no aparelho só se sabe com o celular na
mão. Se não resolver, o próximo passo é código nativo (pyjnius no Android).

### O trem (projeto de restauração)

O Centro Comunitário do Stardew. **Trava por juntar coisas, não por tempo** — e
foi por isso que essa ideia substituiu a de travar conteúdo por ano: quem joga
bem abre rápido, quem joga devagar abre depois. O jogador decide o ritmo.

Um quadro com coleções ("a Feira precisa de 3 queijos, 2 geleias e 1 abóbora"),
progresso visível, e o trem consertado abre destino novo.

**Começar pequeno:** um destino só, uma feira que aparece de vez em quando com
coisa que não existe no vale. Cidade inteira é caro — a cidade atual tem 10 KB de
texto e personagens, e isso não é código, é **escrita**.

### Ferramentas: pá, machado, picareta, enxada

**Regra que não pode ser quebrada:** ferramenta serve pra *abrir coisa nova* ou
*economizar energia*, **nunca** pra criar passo obrigatório no que já existe. Se a
enxada virar "arar antes de plantar", a gente desfaz o conserto da energia.

- **Machado** → madeira, e dá função à floresta, que hoje é evento solto
- **Picareta** → pedra e minério, material novo
- **Pá** → cavar: tesouro, minhoca pra pescar
- **Enxada** → não ara: *amplia*, abre mais canteiros a cada melhoria

Madeira e pedra viram **segunda moeda**: melhorar a casa e o celeiro passa a ser
conquistado, não só comprado.

### O Concurso da Abóbora Gigante ✅ (12/09/2026)

`abobora_gigante` **já existe** e vale ¢900, o item mais caro do jogo. Hoje só
aparece por sorte e no festival. Virar projeto de temporada: planta no começo do
outono, cuida vários dias seguidos (regar, adubar, proteger da raposa — que já é
um evento escrito), e no festival é pesada e disputa.

É um objetivo com prazo que atravessa muitos dias: o "não posso dormir agora, a
abóbora precisa de água".

### O cachorro com função ✅ (12/09/2026)

Existe e hoje é quase decoração. Carinho de manhã dá energia, ou acompanha na
floresta e acha coisa, ou espanta a raposa.

### Música que muda com a estação ✅ (12/09/2026)

`MUSICA_DO_LOCAL` mapeia por **lugar** (título, fazenda, cidade, festa), não por
estação: primavera e inverno soam igual. O cenário e o céu já mudam; falta o
ouvido.

Importa mais agora que o jogo vai ter anos: o que faz um ano *parecer* um ano não
é o contador na tela, é a coisa mudar de cor e de som embaixo do jogador.

**Feito assim:** `ESTACAO_MUSICA` no `musica.py` guarda (estilo, delta de bpm) por
estação, e `Musica.ajustar_estacao` re-sintetiza o tema da fazenda nas quatro
viradas do ano. Primavera 112 bpm alegre, Verão 124 alegre, Outono 98 calmo,
Inverno 82 ninar. **Ninguém ouviu ainda** — os números são plausíveis, mas se
alguma estação soar errada é só mexer nessa tabela.

### Mais animais ✅ (12/09/2026) — pato e cabra

Cada um é uma entrada no `config.py` com preço, produto e casa. Encaixe rápido
pra qualquer dia.

---

## O que saiu no dia 12/09/2026

Além das três do topo e das que estão marcadas na fila:

- **Cozinha da casa e 7 receitas novas** — havia 4 receitas de verdade, todas
  atrás de prédios de nível 3 e 4: no começo do jogo não existia comida cozida.
- **Caderneta do vale** — ver corações, gostos, aniversários e bônus sem gastar
  a ação de ir à cidade.
- **Prêmios da amizade** — os corações destravam preço melhor, obra mais barata,
  pedido que paga mais, energia e presentes de manhã.
- **Limite de presentes** — dois por pessoa a cada 7 dias, para amizade ser
  construída com tempo em vez de comprada com o celeiro cheio.
- **Correções achadas jogando:** o meio do lago castigava duas vezes; o festival
  só acontecia no ano 1 (regressão dos anos); presentear e comer vazavam da tela
  com o celeiro cheio; o cabelo comprido parecia barba; travessões viravam "?".
- **`tools/checar_texto.py`** — acusa caractere que a fonte não desenha, antes
  de virar interrogação na tela.

## O que NÃO fazer

- **Namoro/casamento.** É o que mais dá retorno no Stardew e o que mais custa:
  horas de diálogo, e diálogo só a Isabella pode escrever.
- **Árvore de fabricação grande.** Quatro ferramentas sim; vinte ferramentas e
  cinquenta receitas não.
- **Cidades inteiras antes do trem funcionar.**
- Qualquer coisa com internet ou dois jogadores.

---

## A regra que vale mais que este plano

Um dia de trabalho cabe **três coisas**. O jeito mais fácil de terminar frustrada
é começar nove. Esta fila existe pra as ideias não se perderem — não pra serem
feitas todas.
