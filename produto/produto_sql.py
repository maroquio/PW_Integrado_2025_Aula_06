CREATE_TABLE = '''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    estoque INTEGER NOT NULL
)
'''

INSERT_PRODUTO = '''
INSERT INTO produtos (nome, preco, estoque)
VALUES (?, ?, ?)
'''

SELECT_PRODUTO = '''
SELECT id, nome, preco, estoque 
FROM produtos
WHERE id = ?
'''

SELECT_TODOS_PRODUTOS = '''
SELECT id, nome, preco, estoque 
FROM produtos
'''

UPDATE_PRODUTO = '''
UPDATE produtos 
SET nome = ?, preco = ?, estoque = ? 
WHERE id = ?
'''

DELETE_PRODUTO = '''
DELETE FROM produtos 
WHERE id = ?
'''