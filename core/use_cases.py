import logging

from core.entities import Serie
from core.repositories import (
    FavoritoRepository,
    InsightRepository,
    SerieExternalRepository,
)

logger = logging.getLogger(__name__)

INSIGHT_INDISPONIVEL = "Insight indisponível no momento."


class BuscarSerieUseCase:
    def __init__(self, repository: SerieExternalRepository):
        self.repository = repository

    def executar(self, nome: str) -> list[Serie]:
        if not nome or not nome.strip():
            raise ValueError("O nome da série não pode ser vazio")

        return self.repository.buscar_por_nome(nome.strip())


class FavoritarSerieUseCase:
    def __init__(self, repository: FavoritoRepository):
        self.repository = repository

    def executar(self, serie: Serie) -> None:
        self.repository.salvar(serie)


class ListarFavoritasUseCase:
    def __init__(self, repository: FavoritoRepository):
        self.repository = repository

    def executar(self) -> list[Serie]:
        return self.repository.buscar_favoritas()


class GerarInsightUseCase:
    def __init__(self, repository: InsightRepository):
        self.repository = repository

    def executar(self, serie: Serie) -> str:
        try:
            return self.repository.gerar_insight(serie.sinopse or "", serie.generos or [])
        except Exception:
            logger.exception("Falha ao gerar insight para a série %s", serie.id)
            return INSIGHT_INDISPONIVEL