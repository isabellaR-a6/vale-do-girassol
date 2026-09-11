"""Estrutura de uma "tela" de escolhas: texto da história + opções embaixo."""
from dataclasses import dataclass, field
from typing import Callable, Optional


@dataclass
class Opcao:
    texto: str
    acao: Callable[[], "Tela"]
    ativa: bool = True
    dica: str = ""        # aparece à direita (ex.: preço)
    icone: str = ""       # item do celeiro para mostrar antes do texto
    automatica: bool = False  # criada pela interface (ex.: "Sortear um nome"), não pela história


@dataclass
class Tela:
    texto: str
    opcoes: list = field(default_factory=list)
    titulo: str = ""              # etiqueta em cima da caixa (lugar ou quem fala)
    local: str = "fazenda"        # cenário desenhado em cima
    retrato: Optional[str] = None  # personagem que está falando
    entrada: Optional[Callable[[str], "Tela"]] = None  # pede um texto (ex.: nome)
    som: str = ""
    painel: str = ""              # painel extra sobre o cenário ("celeiro", "pedidos")
