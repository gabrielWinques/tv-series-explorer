import os

import httpx

from core.repositories import InsightRepository


class HuggingFaceRepository(InsightRepository):
    API_URL = "https://router.huggingface.co/v1/chat/completions"
    MODEL = "openai/gpt-oss-20b"
    TIMEOUT = 30

    def __init__(self, http_client: httpx.Client | None = None):
        self.http_client = http_client or httpx.Client(timeout=self.TIMEOUT)

    def gerar_insight(self, sinopse: str, generos: list[str]) -> str:
        token = os.getenv("HF_TOKEN")
        if not token:
            raise RuntimeError("HF_TOKEN não está configurado")

        response = self.http_client.post(
            self.API_URL,
            headers={"Authorization": f"Bearer {token}"},
            json={
                "model": self.MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": "Você gera insights curtos sobre séries de TV em português.",
                    },
                    {"role": "user", "content": self._montar_prompt(sinopse, generos)},
                ],
                "max_tokens": 300,
                "temperature": 0.3,
            },
        )
        response.raise_for_status()

        content = response.json()["choices"][0]["message"].get("content")
        if not content or not content.strip():
            raise ValueError("O Hugging Face não retornou nenhum insight")
        return content.strip()

    @staticmethod
    def _montar_prompt(sinopse: str, generos: list[str]) -> str:
        return (
            "Escreva exatamente uma frase curta, em português, com um insight "
            "sobre esta série. Sem preâmbulo, sem tópicos, sem mencionar que "
            "você é uma IA. Retorne apenas a frase.\n\n"
            f"Sinopse: {sinopse or 'Nenhuma'}\n"
            f"Gêneros: {', '.join(generos) or 'Nenhum'}"
        )