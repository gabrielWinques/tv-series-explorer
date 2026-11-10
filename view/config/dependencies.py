from dataclasses import dataclass

from adapters.huggingface_repository import HuggingFaceRepository
from adapters.postgres_repository import PostgresRepository
from adapters.tvmaze_repository import TVMazeRepository
from core.use_cases import (
    BuscarSerieUseCase,
    FavoritarSerieUseCase,
    GerarInsightUseCase,
    ListarFavoritasUseCase,
)


@dataclass
class Dependencias:
    buscar_serie: BuscarSerieUseCase
    favoritar_serie: FavoritarSerieUseCase
    listar_favoritas: ListarFavoritasUseCase
    gerar_insight: GerarInsightUseCase


def criar_dependencias() -> Dependencias:
    tvmaze = TVMazeRepository()
    postgres = PostgresRepository()
    huggingface = HuggingFaceRepository()

    return Dependencias(
        buscar_serie=BuscarSerieUseCase(tvmaze),
        favoritar_serie=FavoritarSerieUseCase(postgres),
        listar_favoritas=ListarFavoritasUseCase(postgres),
        gerar_insight=GerarInsightUseCase(huggingface),
    )