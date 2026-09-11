# 🌻 Vale do Girassol

RPG de escolhas numa fazenda, feito 100% em Python (pygame) com pixel art desenhada em código.
Nenhuma imagem ou som externo: sprites, fonte pixelada e efeitos 8-bit são gerados pelo próprio jogo.

> 🎮 **Jogar agora (celular ou PC):** https://vale-do-girassol.netlify.app — deite o celular e toque na tela.
>
> 📦 **App Android (APK):** https://github.com/isabellaR-a6/vale-do-girassol/releases/tag/apk — gerado sozinho pelo GitHub Actions.
>
> 💻 **Vai trabalhar de outro notebook?** Veja o passo a passo em [COMO_TRABALHAR.md](COMO_TRABALHAR.md)
> (instalar, baixar do GitHub, rotina `git pull` / `git push` e publicação).

## Como rodar

```bash
git clone https://github.com/isabellaR-a6/vale-do-girassol.git
cd vale-do-girassol
pip install -r requirements.txt
python main.py
```

**Controles:** mouse ou toque, setas + ENTER/ESPAÇO ou teclas 1–9. **F11** alterna tela cheia. **M** liga/desliga a música.

**Música:** 4 trilhas chiptune compostas em código (`musica.py`): fazenda, cidade, floresta/lago e noite.
Elas trocam sozinhas conforme o lugar, com transição suave.

## Jogar no celular / no navegador

O [pygbag](https://pygame-web.github.io) transforma o jogo num site estático (Python rodando em WebAssembly).

**Publicação automática (ligada):** o site https://vale-do-girassol.netlify.app está ligado a este repositório;
cada `git push` gera e publica a versão web sozinho (a receita está no `netlify.toml`). Passo a passo em [COMO_TRABALHAR.md](COMO_TRABALHAR.md#6-versão-web-celular-e-publicação).

**Gerar à mão** (rode *dentro* desta pasta, para ele ler o `pygbag.ini`, que deixa o save de fora):

```bash
python -X utf8 -m pygbag --build --archive --title "Vale do Girassol" --template web/pagina.tmpl --icon web/icone.png .
```

Isso cria `build/web/` (o site) e `build/web.zip` (para o itch.io). O `-X utf8` é necessário no Windows por causa dos acentos.

- **Netlify manual:** abra <https://app.netlify.com/drop> e arraste a pasta `build/web`.
- **itch.io:** crie um projeto do tipo *HTML*, envie o `build/web.zip`, marque *"This file will be played in the browser"*,
  tamanho 1280×720, e ative *Mobile friendly* e *Fullscreen button*.

**Jogar:** abra o link no celular, **deite o celular** (modo paisagem) e toque na tela para começar.
Na web o save fica guardado no navegador (localStorage), separado do save do computador.

**Modo celular:** em telas de toque o jogo usa letra 2× maior e botões altos, e mostra
"Gire o celular" se ele estiver em pé (o jogo é só deitado). Para ver esse layout no PC: `python main.py --celular`.

## O jogo

Sua avó deixou a Fazenda Girassol e ¢500. Cada dia você tem ⚡ energia e decide o que fazer:
plantar, regar, colher, cuidar dos animais, ir à cidade, explorar a floresta, pescar ou visitar o vizinho.
Em 28 dias (4 estações) a vila avalia a sua fazenda no Concurso da Fazenda do Ano.

- 6 culturas, 4 animais, 8 construções e 6 receitas (pão, bolo, geleia, queijo, ração)
- Clima e estações (a terra congela no inverno sem estufa)
- Pedidos no quadro da cidade, preços que mudam todo dia
- Eventos surpresa: raposas, tempestades, viajante misterioso, filhote perdido, festival...
- Salva sozinho toda noite (`save_fazenda.json`)

## Arquivos

| Arquivo | O que faz |
|---|---|
| `main.py` | Janela, loop do jogo, sons e transições |
| `musica.py` | Músicas de fundo (melodias, acordes e sintetizador) |
| `config.py` | Paleta de cores e todos os números do jogo (preços, tempos, níveis) |
| `estado.py` | Regras da fazenda e save/load |
| `historia.py`, `cidade.py`, `eventos.py` | As telas de escolha e a narrativa |
| `tela.py` | Estrutura de uma tela (texto + opções) |
| `interface.py`, `fonte.py` | Caixa de diálogo, HUD e fonte pixelada |
| `cenario.py`, `cenario_locais.py`, `desenho.py`, `sprites.py` | Pixel art dos cenários, personagens e itens |
| `requirements.txt` | Bibliotecas: `pygame` (jogo) e `pygbag` (versão web) |
| `netlify.toml`, `pygbag.ini` | Receita da versão web e da publicação automática no Netlify |
| `COMO_TRABALHAR.md` | Guia para trabalhar de outro notebook |
