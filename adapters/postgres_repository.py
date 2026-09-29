import os
import psycopg2
from psycopg2.extras import RealDictCursor
from core.entities import Serie
from core.repositories import FavoritoRepository


class PostgresRepository(FavoritoRepository):
    def __init__(self):
        self.database_url = os.environ["DATABASE_URL"]

    def _conectar(self):
        return psycopg2.connect(self.database_url, cursor_factory=RealDictCursor)

    def salvar(self, serie: Serie) -> None:
        with self._conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO favoritos (id, nome, sinopse, generos, avaliacao, imagem_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        nome = EXCLUDED.nome,
                        sinopse = EXCLUDED.sinopse,
                        generos = EXCLUDED.generos,
                        avaliacao = EXCLUDED.avaliacao,
                        imagem_url = EXCLUDED.imagem_url
                    """,
                    (serie.id, serie.nome, serie.sinopse, serie.generos, serie.avaliacao, serie.imagem_url),
                )
                conn.commit()

    def buscar_favoritas(self) -> list[Serie]:
        with self._conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM favoritos ORDER BY nome")
                linhas = cursor.fetchall()
                return [self._mapear_para_serie(linha) for linha in linhas]

    def _mapear_para_serie(self, linha: dict) -> Serie:
        return Serie(
            id=linha["id"],
            nome=linha["nome"],
            sinopse=linha["sinopse"],
            generos=linha["generos"],
            avaliacao=linha["avaliacao"],
            imagem_url=linha["imagem_url"],
        )