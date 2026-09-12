# Plano do Vale do Girassol

Conversa de 12/09/2026 (madrugada). A pergunta que começou tudo: *"queria alguma
coisa pra ficar emocionante, tipo 'resolvo isso e vou dormir' e passam 4 horas."*

Este arquivo tem duas partes: **o que fazer no próximo dia de trabalho** e **a
fila do que vem depois**, pra nenhuma ideia se perder.

---

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

A ordem importa: **energia primeiro**. Sem ela, qualquer conteúdo novo é mais uma
coisa que o jogador não consegue alcançar.

### 1. Energia e comida que restaura

- Comida vira item consumível: pão, bolo, geleia e queijo devolvem energia.
  Hoje eles só servem pra vender.
- Efeito de projeto: a cadeia de produção deixa de ser "outra forma de ganhar
  dinheiro" e vira a forma de **comprar tempo**, que é o recurso escasso de
  verdade. Trigo → pão → uma ação a mais no dia. É a espinha do Stardew.
- Rever `ENERGIA_BASE` e o preço/nível da reforma da casa.
- **Dizer o que o clima já faz:** a chuva já rega os canteiros de graça
  (`estado.py:161`), e o jogador nunca soube. Basta uma frase no relatório da
  manhã. Custo zero, valor real.

Arquivos: `config.py` (ENERGIA_BASE, itens comestíveis), `estado.py`
(consumir comida), `historia.py` (opção de comer, relatório da manhã).

### 2. Os anos, com o Concurso como placar

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

### 3. O bonequinho personalizável

**O motor já existe e só é usado pelos outros personagens.** `RETRATOS` não
guarda desenhos: ele *gera* cada retrato a partir de pele, cor de cabelo, estilo
(coque, curto, longo, careca), óculos, barba, bigode, chapéu e roupa. E
`pessoa(cabelo, roupa, calca)` já recebe as cores como parâmetro.

Falta só a tela de criação e guardar as escolhas no save.

Arquivos: `sprites.py` (reaproveitar `retrato`), `historia.py` (tela de criação,
logo depois de escolher o nome), `estado.py` (guardar a aparência).

---

## A fila — depois, em cima de um jogo onde já dá pra respirar

### Amizade por pessoa (a de maior retorno)

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

### O jornal da cidade (de manhã)

Substitui a ideia de "carta". Uma tela só, de manhã, com:
- **Coluna de fofoca** — é daqui que saem as dicas de gosto dos personagens.
  Resolve o problema de descoberta da amizade sem precisar de sistema novo
- Previsão do tempo do dia
- Avisos: festival chegando, o que a feira vai ter

É também o **gancho do amanhã**: o jogador dorme sabendo que tem algo esperando.

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

### O Concurso da Abóbora Gigante

`abobora_gigante` **já existe** e vale ¢900, o item mais caro do jogo. Hoje só
aparece por sorte e no festival. Virar projeto de temporada: planta no começo do
outono, cuida vários dias seguidos (regar, adubar, proteger da raposa — que já é
um evento escrito), e no festival é pesada e disputa.

É um objetivo com prazo que atravessa muitos dias: o "não posso dormir agora, a
abóbora precisa de água".

### O cachorro com função

Existe e hoje é quase decoração. Carinho de manhã dá energia, ou acompanha na
floresta e acha coisa, ou espanta a raposa.

### Música que muda com a estação

`MUSICA_DO_LOCAL` mapeia por **lugar** (título, fazenda, cidade, festa), não por
estação: primavera e inverno soam igual. O cenário e o céu já mudam; falta o
ouvido.

Importa mais agora que o jogo vai ter anos: o que faz um ano *parecer* um ano não
é o contador na tela, é a coisa mudar de cor e de som embaixo do jogador.

**Não precisa compor quatro músicas.** Com `ESTILOS` e o sistema de acordes que já
existem, dá pra vestir o mesmo tema de outro jeito: mais grave e lento no inverno,
mais agudo e rápido no verão.

### Mais animais

Cada um é uma entrada no `config.py` com preço, produto e casa. Encaixe rápido
pra qualquer dia.

---

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
