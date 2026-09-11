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

### Jeito automático (já está ligado ✅)

🎮 **Link do jogo: https://vale-do-girassol.netlify.app**
📋 Painel dos deploys: https://app.netlify.com/projects/vale-do-girassol/deploys

O projeto **vale-do-girassol** do Netlify está ligado a este repositório. **Cada `git push` no branch `main`
gera e publica a versão nova sozinho**, em 1–2 minutos. Nada de arrastar pasta.

- Se um deploy falhar, abra o painel acima, clique no deploy com status **Failed** e leia o log.
  O site continua mostrando a última versão que deu certo.
- A receita do build fica no `netlify.toml`. Ele fixa o **Python 3.12**, porque o Netlify usa uma versão mais nova
  por padrão, e o pygame ainda não funciona nela (o Netlify instala o `requirements.txt` sozinho antes do build).

> Esse site é **separado** do site da VSC. Não ligue este repositório ao site da oficina.

### Jeito manual

```bash
python -X utf8 -m pygbag --build --archive --title "Vale do Girassol" --template web/pagina.tmpl --icon web/icone.png .
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
