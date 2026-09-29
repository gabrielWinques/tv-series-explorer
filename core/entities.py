from dataclasses import dataclass
from typing import Optional


@dataclass
class Serie:
    id: int
    nome: str
    sinopse: Optional[str] = None
    generos: Optional[list[str]] = None
    avaliacao: Optional[float] = None
    imagem_url: Optional[str] = None