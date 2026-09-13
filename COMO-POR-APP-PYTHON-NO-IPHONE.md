# Como pôr um app Python no meu iPhone sem Mac

Receita testada em 11/09/2026 com os jogos `click` e `vale-do-girassol`.
Serve para qualquer projeto Python meu.

## A ideia

Não dá para compilar para iOS sem macOS. Mas o **GitHub Actions tem runners
macOS de graça para repositório público**. Então:

```
GitHub Actions (macOS)  →  .ipa SEM assinatura  →  SideStore assina no iPhone
```

O `.ipa` sai sem assinar **de propósito**. Assinar exigiria conta paga da
Apple. Quem assina no fim é o SideStore, com Apple ID gratuito.

Custo total: zero. Sem Mac, sem Mac em nuvem, sem os R$ 500/ano da Apple.

## Antes de tudo: o repositório precisa ser público

Runner macOS é gratuito só em repo público. Em repo privado ele consome
cota a 10x.

---

## Passo 1 — Escolher a ferramenta

| Meu projeto usa | Ferramenta | Maturidade |
|---|---|---|
| **Flet** | `flet build ipa` | madura (é Flutter por baixo) |
| **pygame** | [`pygame-ios`](https://github.com/seekerluke/pygame-ios) | experimental |

Se for pygame: a ferramenta exige **pygame-ce**, não o pygame comum. Mas o
`import pygame` do meu código **não muda** — é substituto direto.

## Passo 2 — Estrutura que o Flet exige

Só para projetos Flet. O `flet build` espera exatamente isto:

```
pyproject.toml
src/
  main.py          ← o entry point TEM que se chamar main.py
  assets/
    icon.png       ← 1024x1024
```

E no `pyproject.toml`:

```toml
[project]
dependencies = ["flet==0.86.5"]

[tool.flet]
org = "br.isabellaradael"

[tool.flet.app]
path = "src"
```

## Passo 3 — O workflow

Copiar de `click/.github/workflows/ios.yml` ou
`vale-do-girassol/.github/workflows/ios.yml`, conforme o caso, e trocar
nome do app, bundle id e nome do `.ipa`.

---

## As armadilhas (cada uma custou uma rodada de CI)

### 1. Nunca usar `channel: stable` solto

O Flutter novo sai e quebra o build sem eu ter mexido em nada. Foi o que
aconteceu: a 3.47.4 saiu, o Flet queria a 3.44.8, abriu um prompt `[y/n]`
e o CI morreu com `EOFError` porque não existe teclado lá.

```yaml
flutter-version: '3.44.8'   # fixar SEMPRE
```

E como rede de segurança, responder automaticamente a qualquer pergunta:

```bash
yes "" | flet build ipa ...
```

### 2. Versão de Python importa

`pygame-ios` exige **Python >= 3.13**. Com 3.12 o pip simplesmente diz que
o pacote não existe — mensagem que engana.

### 3. pygame-ce só tem template 2.5.5 e 2.5.6

Mesmo que a versão atual no PyPI seja mais nova. Fixar em `2.5.6`.

### 4. Consertar o Info.plist depois do build

O template do `pygame-ios` entrega o app chamado `pygame-ios`, com bundle
`com.example.pygame-ios` e as 4 orientações liberadas. Como o `.ipa` está
**sem assinatura**, dá para editar o `Info.plist` livremente — não invalida
nada, porque a assinatura vem depois, no SideStore.

```bash
PB=/usr/libexec/PlistBuddy
"$PB" -c "Set :CFBundleDisplayName Meu Jogo" "$APP/Info.plist"
"$PB" -c "Set :CFBundleIdentifier br.isabellaradael.meujogo" "$APP/Info.plist"
```

Ícone: `sips -z 180 180 icone.png --out "$APP/AppIcon60x60@3x.png"`

### 5. No iPhone o app é SOMENTE LEITURA

Save, config, qualquer escrita: o bundle não aceita. Tem que ir para
`~/Documents`.

```python
if sys.platform == "ios":
    CAMINHO_SAVE = os.path.join(os.path.expanduser("~/Documents"), ARQUIVO)
```

Isso vale para **qualquer** app meu que salve alguma coisa.

### 6. Publicar o log junto com o .ipa

Log do Actions exige login para ler — o que atrapalha quando alguém precisa
me ajudar a diagnosticar. Release é download público:

```yaml
files: |
  meujogo.ipa
  build.log
```

### 7. `continue-on-error` esconde o erro

Ele marca o passo como sucesso e eu fico sem saber o que quebrou. Capturar
a saída antes, com `tee -a build.log`.

### 8. Cuidado com `releases/latest/download/`

Se o repositório tiver outras releases (ex.: uma tag `apk` de build Android),
o GitHub pode considerar aquela a "latest" e o link quebra. Melhor apontar
para a **tag exata** do build.

---

## Passo 4 — Instalar no iPhone

**Antes de tudo, e isso independe da conta descartável:**

1. Instalar o **LocalDevVPN** pela App Store normal ([link](https://apps.apple.com/us/app/localdevvpn/id6755608044)) — com a minha conta de sempre, não é sideload
2. **Ajustes → Privacidade e Segurança → Modo de Desenvolvedor** → ligar. O iPhone reinicia.

**Depois, uma vez só, com cabo:**

3. Baixar o [iloader](https://iloader.app) — MSI, no Windows
4. Criar um **Apple ID descartável** em appleid.apple.com (janela anônima)
5. iloader → login com a conta descartável → selecionar o aparelho → "Install SideStore (Stable)"
6. No iPhone: Ajustes → Geral → VPN e Gerenciamento de Dispositivo → tocar no nome da conta → **Confiar**
7. Abrir o **LocalDevVPN** → Connect
8. Abrir o SideStore, entrar com a conta descartável, tocar em "7 DAYS"

**Nunca sair do iCloud nos Ajustes.** A conta descartável só é digitada
dentro do iloader e do SideStore.

Por que descartável: o SideStore usa um servidor de terceiro no handshake
com a Apple, e isso às vezes faz a Apple travar a conta. Travar uma conta
vazia não custa nada; travar a principal derruba meu iCloud.

**Depois disso o cabo nunca mais é necessário.** As renovações de 7 dias o
iPhone faz sozinho.

## Passo 5 — Atualizar sem sofrer

Adicionar a fonte no SideStore (aba Sources → `+`):

```
https://raw.githubusercontent.com/isabellaR-a6/<repo>/main/source.json
```

Aí o ciclo vira:

```
edito o código → git push → ~25 min → botão "Atualizar" no SideStore
```

Instalar por cima **preserva o save**, porque o bundle id é o mesmo.

O `source.json` é gerado sozinho pelo workflow (`tools/gerar_source.py`).
Só precisa existir um por repositório.

## Limites do Apple ID gratuito

- **3 apps por vez**, contando o próprio SideStore
- 10 apps diferentes por semana
- Renovação a cada 7 dias, automática

## Regra de ouro

**Não usar o CI como ciclo de desenvolvimento.** 25 minutos por tentativa é
insuportável. Testo no notebook, em segundos, e só mando para o CI quando já
está do jeito que quero.

---

# ONDE PAREI (13/09/2026, 01:30)

**Feito e que não precisa refazer:**

- Apple ID descartável criado e funcionando (`isabellaradael04@gmail.com`)
- Número confiável registrado: celular da mãe, recebe SMS
- "Dispositivos Apple" instalado no notebook (era o que faltava para o cabo
  funcionar — o erro era `Failed to connect to usbmuxd`)
- **SideStore instalado no iPhone**, com o arquivo de pareamento no lugar
- Modo de Desenvolvedor ligado, perfil confiado, LocalDevVPN conectada
- Os dois `.ipa` compilados e no ar (Vale build-6, Cabo de Guerra build-5)

**O que falta: um login.** Só isso. No iPhone, sem cabo e sem notebook.

A Apple bloqueou por excesso de tentativas (429 à tarde, 503 à noite). Isso
solta sozinho — é esperar e tentar **uma vez**, com alguém de olho no celular
que recebe o SMS.

## Passo a passo do que falta

1. Abrir o **SideStore** → **Settings** → entrar com a conta descartável
2. Quando pedir o código, alguém lê o SMS e você digita
3. Na aba **My Apps**, tocar em **Refresh All**
4. Aba **Sources** → botão **+** → adicionar as duas fontes:
   - `https://raw.githubusercontent.com/isabellaR-a6/vale-do-girassol/main/source.json`
   - `https://raw.githubusercontent.com/isabellaR-a6/click/main/source.json`
   - As duas aparecem como "Jogos da Isabella" (mesmo nome; está na fila para arrumar)
5. Aba **Browse** → tocar no jogo → **Install**

## Se der errado

| O que aparece | O que fazer |
|---|---|
| 429 ou 503 | É a Apple segurando por excesso de tentativa. Parar e esperar. Cada tentativa a mais aumenta a espera. |
| App não abre, "Untrusted" | Ajustes → Geral → VPN e Gerenciamento de Dispositivo → Confiar |
| Falha ao instalar | Conferir se a **LocalDevVPN está conectada**. É o erro mais comum. |
| Jogo não aparece na fonte | Puxar a tela para baixo para atualizar |

## Depois que estiver funcionando

- **Cada app expira em 7 dias.** O SideStore tenta renovar sozinho com a VPN
  ligada, mas o iOS corta tarefa em segundo plano — conte com abrir e tocar em
  **Refresh All** uma vez por semana. Vencer não apaga nada: renova e volta com
  o save intacto.
- **Limite de 3 apps** ao mesmo tempo, e **o SideStore conta como um**. Então
  cabem ele + 2 jogos. Para um terceiro jogo, apagar um (o save daquele se perde).
  Há também um limite de 10 apps novos por semana.
- **Atualizar um jogo:** `git push` → a CI compila em uns 15 minutos → o
  `source.json` se atualiza sozinho → no iPhone aparece **Update** no SideStore.
  Um toque. Sem cabo, sem notebook, sem código.
