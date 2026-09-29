from core.entities import Serie
from core.repositories import SerieExternalRepository, FavoritoRepository


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