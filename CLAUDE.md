# Vale do Girassol — contexto para o Claude

RPG de escolhas numa fazenda (estilo Hay Day / Stardew Valley), em Python + pygame, com pixel art,
fonte bitmap e música chiptune **gerados em código** (sem imagens nem áudio externos). Tudo em português.

- **Repositório:** https://github.com/isabellaR-a6/vale-do-girassol (privado, branch `main`)
- **APK Android:** gerado pelo GitHub Actions (`.github/workflows/apk.yml` + `buildozer.spec`, Python 3.10 + pygame 2.1
  do python-for-android) e publicado na release `apk`. Assinado com `android/debug.keystore` (fixo, para atualizar por cima).
  No Android: `config.ANDROID` é True, layout celular sempre, save em `$ANDROID_PRIVATE`, toque via clique do SDL.
- **Guia humano:** `COMO_TRABALHAR.md` (instalar, rotina git, publicação). README tem o resumo.

## Decisões da dona do projeto (respeitar)

- Projeto **separado e independente** do site "VSC Serviços Automotivos" (`Documentos\VSC`). Nunca pôr nada do jogo lá.
- O jogo é jogado **deitado** (paisagem). No iPhone quem trava isso é o `Info.plist`, escrito pelo `ios.yml`.
  Nunca bloquear o jogo em pé.
- Mensagens de commit em português; commit/push só quando pedirem (ela costuma pedir para manter o GitHub em dia).

## Estrutura

| Arquivo | Papel |
|---|---|
| `main.py` | Loop **assíncrono** (herdado da versão web; mantido porque funciona), sons, fades, toque (`FINGERDOWN`), orientação |
| `config.py` | Todos os números/cores; `WEB = sys.platform == "emscripten"` |
| `estado.py` | Regras e save (arquivo no PC, `localStorage` na web) |
| `historia.py`, `cidade.py`, `eventos.py` | Telas de escolha (`Tela` + `Opcao` de `tela.py`), cada ação devolve a próxima `Tela` |
| `interface.py` | Caixa de diálogo, HUD, painéis; classe `Layout` com modo PC e **modo celular** (letra 2×) |
| `cenario*.py`, `desenho.py`, `sprites.py`, `fonte.py` | Pixel art procedural (cenário 320×104 ampliado 2×) |
| `musica.py` | Síntese em geradores: thread no PC, aos poucos por quadro na web (sem threads) |
| `web/icone.png`, `web/abertura.png` | **Arte compartilhada, apesar do nome da pasta.** `ios.yml` gera o AppIcon @2x/@3x do iPhone a partir do `icone.png`; o `buildozer.spec` usa os dois no Android. Não apagar. |
| `requirements.txt` | Dependências de quem roda o jogo no PC |

## Comandos

- Rodar: `python main.py` · layout de celular no PC: `python main.py --celular`

## Como testar sem abrir janela

Rodar com `SDL_VIDEODRIVER=dummy` e `SDL_AUDIODRIVER=dummy`, criar `main.Jogo()`, chamar `j.escolher(opcao)` /
`j._desenhar(dt)` e salvar `j.tela` com `pygame.image.save`.

Três pegadinhas que já custaram tempo:
- A tela de escolhas atual é **`j.ui.tela`**, não `j.tela` (essa é a Surface do pygame).
- Para trocar de tela use **`j._aplicar(tela)`**; atribuir `j.ui.tela` direto pula a preparação.
- O texto aparece com efeito de máquina de escrever, e quem avança isso é **`j.ui.atualizar(dt)`**,
  que o laço chama *antes* de `_desenhar`. Só desenhar deixa a caixa de diálogo vazia na foto.
- `j.escolher` pode **trocar o objeto `Estado`** (novo jogo / continuar). Pegue `h.e` de novo depois. Um "robô" escolhendo opções ativas aleatórias por milhares
de passos pega erros de lógica. Aponte `estado.CAMINHO_SAVE` para um arquivo temporário para não sobrescrever o save real.

## Pegadinhas conhecidas

- **A fonte só conhece 87 caracteres, e o que falta vira `?` sem avisar** (`fonte.py:168`).
  Não tem travessão (`—`), reticências (`…`) nem meia-risca. Use `-`, `:` ou `·`.
  Acentos do português têm; `⚡ ¢ ★ ♥` são ícones tratados à parte e funcionam.

- Web: clique sem movimento prévio chega com posição velha; por isso o toque usa `FINGERDOWN` com coordenadas 0–1.
- O `save_fazenda.json` (progresso) não vai para o git; cada computador tem o seu.
