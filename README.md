# 🌻 Vale do Girassol

RPG de escolhas numa fazenda, feito 100% em Python (pygame) com pixel art desenhada em código.
Nenhuma imagem ou som externo: sprites, fonte pixelada e efeitos 8-bit são gerados pelo próprio jogo.

> 📱 **App de iPhone:** veja [COMO-POR-APP-PYTHON-NO-IPHONE.md](COMO-POR-APP-PYTHON-NO-IPHONE.md)
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

## Jogar no celular

Dois caminhos, os dois gerados sozinhos pelo GitHub Actions:

- **Android (APK):** baixe da [release `apk`](https://github.com/isabellaR-a6/vale-do-girassol/releases/tag/apk),
  abra o arquivo e permita "instalar apps desconhecidos". É o jeito mais fácil de passar para alguém.
- **iPhone (.ipa):** passo a passo em [COMO-POR-APP-PYTHON-NO-IPHONE.md](COMO-POR-APP-PYTHON-NO-IPHONE.md).

> A versão web (pygbag + Netlify) foi aposentada em 12/09/2026 — ficava bugada demais para valer a manutenção.
> A pasta `web/` continua existindo porque guarda o ícone e a tela de abertura usados pelo iPhone e pelo Android.

**Modo celular:** em telas de toque o jogo usa letra 2× maior e botões altos, e mostra
o jogo girado se ele estiver em pé: é só virar o celular de lado, mesmo com a rotação travada. Para ver esse layout no PC: `python main.py --celular`.

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
| `requirements.txt` | Bibliotecas: `pygame` |
| `web/icone.png`, `web/abertura.png` | Ícone e tela de abertura usados pelo iPhone e pelo Android |
| `COMO_TRABALHAR.md` | Guia para trabalhar de outro notebook |
