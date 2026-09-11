# Vale do Girassol — contexto para o Claude

RPG de escolhas numa fazenda (estilo Hay Day / Stardew Valley), em Python + pygame, com pixel art,
fonte bitmap e música chiptune **gerados em código** (sem imagens nem áudio externos). Tudo em português.

- **Repositório:** https://github.com/isabellaR-a6/vale-do-girassol (privado, branch `main`)
- **Jogo publicado:** https://vale-do-girassol.netlify.app — o Netlify publica sozinho a cada `git push` no `main`
- **APK Android:** gerado pelo GitHub Actions (`.github/workflows/apk.yml` + `buildozer.spec`, Python 3.10 + pygame 2.1
  do python-for-android) e publicado na release `apk`. Assinado com `android/debug.keystore` (fixo, para atualizar por cima).
  No Android: `config.ANDROID` é True, layout celular sempre, save em `$ANDROID_PRIVATE`, toque via clique do SDL.
- **Guia humano:** `COMO_TRABALHAR.md` (instalar, rotina git, publicação). README tem o resumo.

## Decisões da dona do projeto (respeitar)

- Projeto **separado e independente** do site "VSC Serviços Automotivos" (`Documentos\VSC`). Nunca pôr nada do jogo lá.
- O jogo é jogado **deitado** (paisagem). Na web, com o celular em pé, a página gira o jogo 90° (funciona com a
  rotação travada) e o toque é "desgirado" em `main._traduzir_toque`. Nunca bloquear o jogo em pé.
- Mensagens de commit em português; commit/push só quando pedirem (ela costuma pedir para manter o GitHub em dia).

## Estrutura

| Arquivo | Papel |
|---|---|
| `main.py` | Loop **assíncrono** (exigência do pygbag), sons, fades, toque (`FINGERDOWN`), orientação |
| `config.py` | Todos os números/cores; `WEB = sys.platform == "emscripten"` |
| `estado.py` | Regras e save (arquivo no PC, `localStorage` na web) |
| `historia.py`, `cidade.py`, `eventos.py` | Telas de escolha (`Tela` + `Opcao` de `tela.py`), cada ação devolve a próxima `Tela` |
| `interface.py` | Caixa de diálogo, HUD, painéis; classe `Layout` com modo PC e **modo celular** (letra 2×) |
| `cenario*.py`, `desenho.py`, `sprites.py`, `fonte.py` | Pixel art procedural (cenário 320×104 ampliado 2×) |
| `musica.py` | Síntese em geradores: thread no PC, aos poucos por quadro na web (sem threads) |
| `web/pagina.tmpl`, `web/icone.png` | Página própria do pygbag (viewport certo, encaixe 16:9, pixels nítidos) |
| `netlify.toml`, `pygbag.ini`, `requirements.txt` | Build web (Python 3.12 no Netlify) e o que fica fora do pacote |

## Comandos

- Rodar: `python main.py` · layout de celular no PC: `python main.py --celular`
- Build web (rodar na pasta do projeto): `python -X utf8 -m pygbag --build --archive --title "Vale do Girassol" --template web/pagina.tmpl --icon web/icone.png .`
- Servidor local de teste: configuração `fazenda-web` em `.claude/launch.json` (serve `build/web`). Em localhost o pygbag
  procura o pygame na porta 8000; use `127.0.0.1` em vez de `localhost`.

## Como testar sem abrir janela

Rodar com `SDL_VIDEODRIVER=dummy` e `SDL_AUDIODRIVER=dummy`, criar `main.Jogo()`, chamar `j.escolher(opcao)` /
`j._desenhar(dt)` e salvar `j.tela` com `pygame.image.save`. Um "robô" escolhendo opções ativas aleatórias por milhares
de passos pega erros de lógica. Aponte `estado.CAMINHO_SAVE` para um arquivo temporário para não sobrescrever o save real.

## Pegadinhas conhecidas

- Windows: o pygbag precisa de `python -X utf8` (acentos nos arquivos).
- Web: clique sem movimento prévio chega com posição velha; por isso o toque usa `FINGERDOWN` com coordenadas 0–1.
- Web: aba/janela escondida congela o carregamento do pygbag (rAF pausado) — não é bug do jogo.
- O `save_fazenda.json` (progresso) não vai para o git; cada computador tem o seu.
