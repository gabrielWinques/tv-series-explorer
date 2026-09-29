import requests
from typing import Optional
from core.entities import Serie
from core.repositories import SerieExternalRepository


class TVMazeRepository(SerieExternalRepository):
    BASE_URL = "https://api.tvmaze.com"

    def buscar_por_nome(self, nome: str) -> list[Serie]:
        resposta = requests.get(f"{self.BASE_URL}/search/shows", params={"q": nome})
        resposta.raise_for_status()

        dados = resposta.json()
        return [self._mapear_para_serie(item["show"]) for item in dados]

    def _mapear_para_serie(self, dados: dict) -> Serie:
        return Serie(
            id=dados["id"],
            nome=dados["name"],
            sinopse=self._limpar_html(dados.get("summary")),
            generos=dados.get("genres", []),
            avaliacao=dados.get("rating", {}).get("average"),
            imagem_url=dados.get("image", {}).get("medium") if dados.get("image") else None,
        )

    def _limpar_html(self, texto: Optional[str]) -> Optional[str]:
        if not texto:
            return None
        import re
        return re.sub(r"<[^>]+>", "", texto)