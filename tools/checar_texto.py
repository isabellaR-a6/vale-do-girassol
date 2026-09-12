"""Procura, no texto que o jogo escreve, caracteres que a fonte nao sabe desenhar.

A fonte tem 87 glifos mais quatro icones (¢ ♥ ★ ⚡). Qualquer outro caractere
vira "?" na tela, **sem erro e sem aviso**: o jogo roda normal e o jogador le uma
interrogacao no meio da frase. O travessao (—) e o caso mais comum, porque
editor e teclado trocam o hifen por ele sozinhos.

Olha so o conteudo das aspas, via `ast`, e so os caracteres **fora do ASCII**.
Varrer tudo acusaria colchete e chaves de f-string, que sao sintaxe e nunca
chegam a tela. O que de fato escapa e o caractere tipografico: travessao,
meia-risca, reticencias, aspas curvas — os que o editor troca sozinho.

O proprio fonte.py fica de fora: ele e feito de "#" porque desenha as letras.

Rodar (na pasta do projeto):  python tools/checar_texto.py
Sai com 1 se achou algo, entao serve para CI.
"""
import ast
import io
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame  # noqa: E402

pygame.init()
import fonte  # noqa: E402

CONHECIDOS = set(fonte.FontePixel().glifos) | set(fonte.ICONES)


def textos(arquivo):
    """Devolve (linha, texto) de cada string literal do arquivo, docstrings fora."""
    arvore = ast.parse(io.open(arquivo, encoding="utf-8").read())
    docs = set()
    for no in ast.walk(arvore):
        if isinstance(no, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            corpo = getattr(no, "body", None)
            if corpo and isinstance(corpo[0], ast.Expr) and isinstance(corpo[0].value, ast.Constant) \
                    and isinstance(corpo[0].value.value, str):
                docs.add(id(corpo[0].value))
    for no in ast.walk(arvore):
        if isinstance(no, ast.Constant) and isinstance(no.value, str) and id(no) not in docs:
            yield no.lineno, no.value


def main():
    problemas = []
    for nome in sorted(f for f in os.listdir(RAIZ) if f.endswith(".py") and f != "fonte.py"):
        for linha, texto in textos(os.path.join(RAIZ, nome)):
            for ch in texto:
                if ord(ch) < 128 or ch in CONHECIDOS:
                    continue
                problemas.append((nome, linha, ch, texto.strip()[:60]))
    if not problemas:
        print("OK: tudo que o jogo escreve, a fonte sabe desenhar.")
        return 0
    print(f"{len(problemas)} caractere(s) que virariam '?' na tela:\n")
    for nome, linha, ch, trecho in problemas:
        print(f"  {nome}:{linha}  {ch!r} (U+{ord(ch):04X})  ...{trecho}...")
    return 1


if __name__ == "__main__":
    sys.exit(main())
