# 🌻 Como trabalhar no Vale do Girassol em outro notebook

O projeto fica no GitHub: **https://github.com/isabellaR-a6/vale-do-girassol**
Em qualquer computador você baixa de lá, mexe, e manda de volta. Nada de copiar pasta ou pendrive.

---

## 1. Instalar (só na primeira vez em cada notebook)

| Programa | Onde baixar | Cuidado |
|---|---|---|
| **Git** | https://git-scm.com/download/win | Pode ir no "Next" em tudo |
| **Python 3.12 ou 3.13** | https://www.python.org/downloads/ | Marque **"Add python.exe to PATH"** na primeira tela |
| VS Code ou Claude Code *(opcional)* | https://code.visualstudio.com / https://claude.com/claude-code | Para editar o código |

Depois de instalar, feche e abra o terminal e confira:

```bash
git --version
```

```bash
python --version
```

Diga ao Git quem você é (uma vez por computador):

```bash
git config --global user.name "Isabella Radael"
```

```bash
git config --global user.email "isabella.radael@aluno.senai.br"
```

## 2. Baixar o projeto

Escolha uma pasta **fora do OneDrive** (por exemplo `C:\Projetos`) — o OneDrive sincronizando a pasta
`.git` em dois computadores costuma dar conflito.

```bash
cd C:\Projetos
```

```bash
git clone https://github.com/isabellaR-a6/vale-do-girassol.git
```

```bash
cd vale-do-girassol
```

```bash
pip install -r requirements.txt
```

```bash
python main.py
```

Na primeira vez que o Git falar com o GitHub, abre uma janela pedindo login: entre com a conta
**isabellaR-a6** pelo navegador. O Windows guarda o login depois disso.

## 3. A rotina: puxar antes, enviar depois

**Antes de começar a mexer** (pega o que você fez no outro notebook):

```bash
git pull
```

**Quando terminar** (manda para o GitHub):

```bash
git add .
```

```bash
git commit -m "Descreva o que mudou"
```

```bash
git push
```

> Regra de ouro: **sempre `git pull` ao sentar, sempre `git push` ao levantar.**
> Se esquecer e os dois notebooks mexerem no mesmo arquivo, o Git avisa de "conflito" ao dar `git pull`:
> abra o arquivo, escolha qual versão fica (o VS Code mostra botões para isso), salve e faça `add` + `commit` + `push`.

## 4. O que NÃO vai para o GitHub

| Arquivo/pasta | Por quê |
|---|---|
| `save_fazenda.json` | É o seu progresso no jogo. Cada computador tem o seu. Para levar o progresso, copie esse arquivo à mão. |
| `__pycache__/` | Arquivos temporários do Python. |

(Isso está configurado no `.gitignore`.)

## 5. Testar

| Comando | O que faz |
|---|---|
| `python main.py` | Roda o jogo no computador |
| `python main.py --celular` | Roda com o layout de celular (letra grande), para testar no PC |

Teclas: **M** liga/desliga a música, **F11** tela cheia.

## 6. Versão web — aposentada

A versão web (pygbag + Netlify) **saiu do projeto em 12/09/2026**. Ficava bugada demais para valer a manutenção.
Foram removidos o `netlify.toml`, o `pygbag.ini` e o `web/pagina.tmpl`.

⚠️ A pasta `web/` **continua**, apesar do nome: o `web/icone.png` vira o ícone do iPhone (o `ios.yml` gera o
`AppIcon` @2x e @3x a partir dele) e do Android, e o `web/abertura.png` é a tela de abertura do Android.
Não apague esses dois.

Para distribuir o jogo hoje existem dois caminhos: o **APK Android** (abaixo) e o **app de iPhone**
(veja `COMO-POR-APP-PYTHON-NO-IPHONE.md`).

## 7. App Android (APK) feito pelo GitHub

O GitHub gera um **app Android de verdade** (APK), que roda sem internet e em tela cheia.

📦 **Download: https://github.com/isabellaR-a6/vale-do-girassol/releases/tag/apk**
(o repositório é privado: no celular, entre na conta do GitHub antes de abrir o link)

**Instalar:** baixe o `vale-do-girassol.apk`, abra o arquivo e permita **"instalar apps desconhecidos"** quando o
Android pedir. O Play Protect pode avisar que o app é desconhecido; é normal (ele não está na Play Store), toque em
"Instalar mesmo assim".

**Como é gerado:** o fluxo `.github/workflows/apk.yml` roda sozinho a cada `git push` que muda o jogo
(arquivos `.py`, `buildozer.spec`, ícone ou abertura). Leva uns **20–40 minutos** e publica o APK novo no mesmo link.
Para gerar na mão: aba **Actions** do repositório → **APK Android** → **Run workflow**.

- **Atualizar:** instale o APK novo por cima do antigo. O progresso fica guardado (a assinatura é sempre a mesma,
  por causa do `android/debug.keystore`; não apague esse arquivo, senão o celular recusa a atualização).
- **Receita:** `buildozer.spec` (nome, ícone, abertura, só deitado, Python 3.10 + pygame 2.1).
  No Android o jogo já abre no modo celular (letra grande) e salva numa pasta própria do app.
- **Se falhar:** aba Actions → clique no build com ❌ → abra o passo que falhou e leia o fim do log.
- **Minutos:** repositório privado tem ~2000 minutos grátis de Actions por mês; cada APK gasta uns 30.

## 8. Onde mexer em cada coisa

| Quero mudar... | Arquivo |
|---|---|
| Preços, tempo das plantas, níveis, cores | `config.py` |
| Textos e escolhas da fazenda, começo e final | `historia.py` |
| Cidade (mercado, feira, carpintaria, pedidos, café) | `cidade.py` |
| Floresta, lago, vizinho, eventos surpresa, cartas | `eventos.py` |
| Regras (crescimento, animais, save) | `estado.py` |
| Músicas (notas e acordes) | `musica.py` |
| Caixa de diálogo, botões, HUD, modo celular | `interface.py` |
| Desenhos (sprites, cenários) | `sprites.py`, `cenario.py`, `cenario_locais.py`, `desenho.py` |
| Letras da fonte pixelada | `fonte.py` |

## 9. Problemas comuns

| Problema | Solução |
|---|---|
| `'python' não é reconhecido` | Reinstale o Python marcando **Add to PATH**, ou use `py` no lugar de `python`. |
| `No module named 'pygame'` | `pip install -r requirements.txt` |
| `git push` pede senha e não aceita | A senha da conta não funciona no Git; use o login pela janela do navegador. |
| `git pull` diz que há mudanças locais | Faça `add` + `commit` antes, e depois `git pull` de novo. |

## 10. Usando o Claude Code

Abra a pasta do projeto no Claude Code e peça o que quiser ("adiciona uma cultura nova", "muda a música da cidade").
