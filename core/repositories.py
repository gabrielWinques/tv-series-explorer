from abc import ABC, abstractmethod
from core.entities import Serie


class SerieExternalRepository(ABC):
    @abstractmethod
    def buscar_por_nome(self, nome: str) -> list[Serie]:
        """Busca séries numa fonte externa (ex: TVMaze)"""


class FavoritoRepository(ABC):
    @abstractmethod
    def salvar(self, serie: Serie) -> None:
        """Salva/atualiza um favorito"""

    @abstractmethod
    def buscar_favoritas(self) -> list[Serie]:
        """Retorna todas as séries favoritadas"""


class InsightRepository(ABC):
    @abstractmethod
    def gerar_insight(self, sinopse: str, generos: list[str]) -> str:
        """Gera um insight curto sobre uma série"""