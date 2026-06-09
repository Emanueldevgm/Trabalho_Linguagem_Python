

CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    preco_unitario FLOAT NOT NULL,
    estoque_atual INTEGER DEFAULT 0,
    estoque_minimo INTEGER DEFAULT 5,
    lead_time_dias INTEGER DEFAULT 7
);

CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    perfil VARCHAR(20) DEFAULT 'operador',
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    valor_total FLOAT NOT NULL,
    FOREIGN KEY(produto_id) REFERENCES produtos(id) ON DELETE CASCADE
);

CREATE TABLE compras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    custo_total FLOAT NOT NULL,
    FOREIGN KEY(produto_id) REFERENCES produtos(id) ON DELETE CASCADE
);

CREATE TABLE previsoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_geracao DATETIME DEFAULT CURRENT_TIMESTAMP,
    produto_id INTEGER NOT NULL,
    periodo_inicio DATE NOT NULL,
    periodo_fim DATE NOT NULL,
    quantidade_prevista FLOAT NOT NULL,
    modelo_usado VARCHAR(100) DEFAULT 'RandomForest',
    FOREIGN KEY(produto_id) REFERENCES produtos(id) ON DELETE CASCADE
);
