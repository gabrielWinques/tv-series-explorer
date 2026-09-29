CREATE TABLE IF NOT EXISTS favoritos (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    sinopse TEXT,
    generos TEXT[],
    avaliacao NUMERIC(3, 1),
    imagem_url VARCHAR(500),
    criado_em TIMESTAMP DEFAULT NOW()
);