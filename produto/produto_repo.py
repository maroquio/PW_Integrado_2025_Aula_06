from typing import List, Optional
from produto.produto import Produto
from produto import produto_sql as sql
from util import get_db_connection


class ProdutoRepo:
    def __init__(self):
        self._criar_tabela()

    def _criar_tabela(self):
        with get_db_connection() as conn:
            conn.execute(sql.CREATE_TABLE)

    def adicionar(self, produto: Produto) -> int:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql.INSERT_PRODUTO, (produto.nome, produto.preco, produto.estoque))
            return cursor.lastrowid

    def obter(self, produto_id: int) -> Optional[Produto]:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql.SELECT_PRODUTO, (produto_id,))
            row = cursor.fetchone()
            if row:
                return Produto(id=row[0], nome=row[1], preco=row[2], estoque=row[3])
            return None

    def obter_todos(self) -> List[Produto]:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql.SELECT_TODOS_PRODUTOS)
            rows = cursor.fetchall()
            return [Produto(id=row[0], nome=row[1], preco=row[2], estoque=row[3]) for row in rows]

    def atualizar(self, produto: Produto) -> bool:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql.UPDATE_PRODUTO, (produto.nome, produto.preco, produto.estoque, produto.id))
            return cursor.rowcount > 0

    def excluir(self, produto_id: int) -> bool:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql.DELETE_PRODUTO, (produto_id,))
            return cursor.rowcount > 0