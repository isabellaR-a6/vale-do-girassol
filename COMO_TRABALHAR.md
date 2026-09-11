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
| `build/` | É gerado pelo pygbag (versão web). Dá para gerar de novo quando quiser. |
| `__pycache__/` | Arquivos temporários do Python. |

(Isso está configurado no `.gitignore`.)

## 5. Testar

| Comando | O que faz |
|---|---|
| `python main.py` | Roda o jogo no computador |
| `python main.py --celular` | Roda com o layout de celular (letra grande), para testar no PC |

Teclas: **M** liga/desliga a música, **F11** tela cheia.

## 6. Versão web (celular) e publicação

### Jeito automático (recomendado): Netlify ligado ao GitHub

Faça uma vez:

1. Entre em https://app.netlify.com → **Add new site** → **Import an existing project** → **GitHub**.
2. Escolha o repositório **vale-do-girassol**. As configurações de build já vêm do arquivo `netlify.toml`.
3. Clique em **Deploy**. Pronto: o link do jogo aparece no painel (dá para trocar o nome em *Site configuration*).

Depois disso, **cada `git push` publica a versão nova sozinho**, em 1–2 minutos.

> Esse site é **separado** do site da VSC. Não ligue este repositório ao site da oficina.

### Jeito manual

```bash
python -X utf8 -m pygbag --build --archive --title "Vale do Girassol" .
```

Isso cria `build/web` (arraste em https://app.netlify.com/drop) e `build/web.zip` (para o itch.io).
Rode **dentro da pasta do projeto**, para ele ler o `pygbag.ini`. O `-X utf8` evita erro com acentos no Windows.

No celular: abra o link, **deite o celular** e toque na tela. Em pé aparece "Gire o celular".

## 7. Onde mexer em cada coisa

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

## 8. Problemas comuns

| Problema | Solução |
|---|---|
| `'python' não é reconhecido` | Reinstale o Python marcando **Add to PATH**, ou use `py` no lugar de `python`. |
| `No module named 'pygame'` | `pip install -r requirements.txt` |
| `UnicodeDecodeError` ao gerar a versão web | Use o comando com `python -X utf8 ...` |
| `git push` pede senha e não aceita | A senha da conta não funciona no Git; use o login pela janela do navegador. |
| `git pull` diz que há mudanças locais | Faça `add` + `commit` antes, e depois `git pull` de novo. |
| A página web fica cinza parada | Espere (a 1ª vez baixa o Python, ~20 s) e toque na tela. |

## 9. Usando o Claude Code

Abra a pasta do projeto no Claude Code e peça o que quiser ("adiciona uma cultura nova", "muda a música da cidade").
O arquivo `.claude/launch.json` já tem o servidor **fazenda-web** para testar a versão web gerada em `build/web`.
