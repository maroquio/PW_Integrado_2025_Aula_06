# Programação para a Web

#### Aula 6 - Introdução ao Uso de Banco de Dados com Python

#### Prof. Ricardo Maroquio

Olá! Hoje, vamos aprimorar nossos conhecimentos sobre o uso de banco de dados com Python. Veremos como manipular dados de um banco de dados SQLite, executando comandos SQL, implementando o padrão *repositório* para operações CRUD e criação de tabela. Além disso, utilizaremos o Pydantic 2 para validação de dados diretamente nas classes de domínio. Ao final, construiremos um programa de console interativo que permitirá ao usuário gerenciar produtos por meio de um menu.​

## Objetivos da Aula 
 
a) Definir a entidade `Produto` com validações personalizadas usando Pydantic 2;

b) Separar comandos SQL em constantes em um módulo dedicado;

c) Implementar a classe `ProdutoRepo` para gerenciar operações CRUD;

d) Desenvolver um programa de console interativo com um menu para gerenciar produtos;

e) Garantir tratamento adequado de exceções e validação de entradas do usuário;

## 1. Definindo a Entidade `Produto` com Validações Personalizadas

Criaremos a classe `Produto` no arquivo `produto.py`, utilizando Pydantic 2 para validação de dados. As validações personalizadas serão implementadas com métodos decorados com `@field_validator`.
​[Welcome to Pydantic - Pydantic](https://docs.pydantic.dev/2.0/usage/validators/) 

```python
# arquivo /produto/produto.py

from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional

class Produto(BaseModel):
    id: Optional[int] = None
    nome: str
    preco: float
    estoque: int

    @field_validator('nome')
    def validar_nome(cls, v):
        if not v.strip():
            raise ValueError('O nome do produto não pode ser vazio.')
        if len(v) > 100:
            raise ValueError('O nome do produto não pode exceder 100 caracteres.')
        return v

    @field_validator('preco')
    def validar_preco(cls, v):
        if v <= 0:
            raise ValueError('O preço deve ser maior que zero.')
        return v

    @field_validator('estoque')
    def validar_estoque(cls, v):
        if v < 0:
            raise ValueError('O estoque não pode ser negativo.')
        return v
```

**Explicação:** 
 
- **Validações Personalizadas:**  Utilizamos o decorador `@field_validator` para criar métodos que validam os campos `nome`, `preco` e `estoque`. Essas validações garantem que os dados atendam aos critérios estabelecidos antes de serem processados ou armazenados.​

## 2. Separando Comandos SQL em Constantes 

Para manter nosso código organizado, armazenaremos os comandos SQL em constantes no arquivo `produto_sql.py`.​

```python
# arquivo /produto/produto_sql.py

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
SELECT id, nome, preco, estoque FROM produtos
WHERE id = ?
'''

SELECT_TODOS_PRODUTOS = '''
SELECT id, nome, preco, estoque 
FROM produtos
'''

UPDATE_PRODUTO = '''
UPDATE produtos SET nome = ?, preco = ?, estoque = ? 
WHERE id = ?
'''

DELETE_PRODUTO = '''
DELETE FROM produtos 
WHERE id = ?
'''
```

**Explicação:** 
 
- **Constantes SQL:**  Definimos constantes para cada comando SQL necessário, facilitando a manutenção e evitando a repetição de strings SQL no código principal.​

## 3. Implementando a Classe `ProdutoRepo`
A classe `ProdutoRepo`, localizada no arquivo `produto_repo.py`, será responsável por gerenciar as operações CRUD utilizando os comandos SQL definidos.​

```python
# arquivo /produto/produto_repo.py

import sqlite3
from contextlib import contextmanager
from typing import List, Optional
from produto import Produto
import produto_sql as sql

@contextmanager
def get_db_connection(db_name='produtos.db'):
    conn = sqlite3.connect(db_name)
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()

class ProdutoRepo:
    def __init__(self, db_name='produtos.db'):
        self.db_name = db_name
        self._criar_tabela()

    def _criar_tabela(self):
        with get_db_connection(self.db_name) as conn:
            conn.execute(sql.CREATE_TABLE)

    def adicionar(self, produto: Produto) -> int:
        with get_db_connection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(sql.INSERT_PRODUTO, (produto.nome, produto.preco, produto.estoque))
            return cursor.lastrowid

    def obter(self, produto_id: int) -> Optional[Produto]:
        with get_db_connection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(sql.SELECT_PRODUTO, (produto_id,))
            row = cursor.fetchone()
            if row:
                return Produto(id=row[0], nome=row[1], preco=row[2], estoque=row[3])
            return None

    def obter_todos(self) -> List[Produto]:
        with get_db_connection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(sql.SELECT_TODOS_PRODUTOS)
            rows = cursor.fetchall()
            return [Produto(id=row[0], nome=row[1], preco=row[2], estoque=row[3]) for row in rows]

    def atualizar(self, produto: Produto) -> bool:
        with get_db_connection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(sql.UPDATE_PRODUTO, (produto.nome, produto.preco, produto.estoque, produto.id))
            return cursor.rowcount > 0

    def excluir(self, produto_id: int) -> bool:
        with get_db_connection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(sql.DELETE_PRODUTO, (produto_id,))
            return cursor.rowcount > 0
```

**Explicação:** 
 
- **Gerenciador de Conexão:**  A função `get_db_connection` utiliza o decorador `@contextmanager` para gerenciar a conexão com o banco de dados, garantindo que as operações sejam commitadas e a conexão fechada adequadamente.​
 
- **Métodos CRUD:**  Cada método (`adicionar`, `obter`, `obter_todos`, `atualizar`, `excluir`) executa operações específicas no banco de dados, utilizando os comandos SQL definidos no módulo `produto_sql.py`.​


## 4. Desenvolvendo o Programa de Console Interativo 

​Continuando com a implementação, faremos o console interativo para gerenciar produtos. Vamos desenvolver a função principal que apresenta um menu ao usuário e permite realizar operações como cadastrar, listar, alterar e excluir produtos. Cada opção do menu chamará uma função específica que executa a tarefa correspondente, garantindo tratamento adequado de exceções e validação de entradas para evitar interrupções abruptas do programa.​

Antes de prosseguir, instale o pacote `tabulate` para exibir os dados dos produtos em formato de tabela.​

```bash
pip install tabulate
```

Agora vamos ao código do programa principal, localizado no arquivo `main.py`.​

```python
# arquivo /main.py

from tabulate import tabulate
from produto_repo import ProdutoRepo
from produto import Produto, ValidationError

def exibir_menu():
    print("\nMenu de Gerenciamento de Produtos")
    print("a) Cadastrar Produto")
    print("b) Listar Produtos")
    print("c) Alterar Produto")
    print("d) Excluir Produto")
    print("e) Sair")

def obter_entrada_usuario(mensagem, tipo=str):
    while True:
        entrada = input(mensagem)
        try:
            if tipo == float:
                return float(entrada)
            elif tipo == int:
                return int(entrada)
            else:
                return entrada.strip()
        except ValueError:
            print(f"Entrada inválida. Por favor, insira um valor do tipo {tipo.__name__}.")

def cadastrar_produto(repo):
    print("\nCadastro de Novo Produto")
    nome = obter_entrada_usuario("Nome: ")
    preco = obter_entrada_usuario("Preço: ", float)
    estoque = obter_entrada_usuario("Estoque: ", int)

    try:
        novo_produto = Produto(nome=nome, preco=preco, estoque=estoque)
        produto_id = repo.adicionar(novo_produto)
        print(f"Produto cadastrado com sucesso! ID: {produto_id}")
    except ValidationError as e:
        print(f"Erro de validação: {e}")

def listar_produtos(repo: ProdutoRepo):
    produtos = repo.obter_todos()
    if produtos:
        # Preparando os dados para o tabulate
        tabela = [[produto.id, produto.nome, f"R$ {produto.preco:.2f}", produto.estoque] for produto in produtos]
        # Definindo os cabeçalhos das colunas
        cabecalhos = ["ID", "Nome", "Preço", "Estoque"]
        # Exibindo a tabela formatada
        print(tabulate(tabela, headers=cabecalhos, tablefmt="grid", numalign="right", stralign="left"))
    else:
        print("Nenhum produto cadastrado.")

def alterar_produto(repo):
    print("\nAlteração de Produto")
    produto_id = obter_entrada_usuario("ID do produto a ser alterado: ", int)
    produto = repo.obter(produto_id)
    if produto:
        print(f"Produto atual: Nome: {produto.nome}, Preço: {produto.preco}, Estoque: {produto.estoque}")
        nome = obter_entrada_usuario("Novo Nome (deixe em branco para manter o atual): ") or produto.nome
        preco = obter_entrada_usuario("Novo Preço (deixe em branco para manter o atual): ", float) or produto.preco
        estoque = obter_entrada_usuario("Novo Estoque (deixe em branco para manter o atual): ", int) or produto.estoque

        try:
            produto_atualizado = Produto(id=produto.id, nome=nome, preco=preco, estoque=estoque)
            if repo.atualizar(produto_atualizado):
                print("Produto atualizado com sucesso.")
            else:
                print("Falha ao atualizar o produto.")
        except ValidationError as e:
            print(f"Erro de validação: {e}")
    else:
        print("Produto não encontrado.")

def excluir_produto(repo):
    print("\nExclusão de Produto")
    produto_id = obter_entrada_usuario("ID do produto a ser excluído: ", int)
    if repo.excluir(produto_id):
        print("Produto excluído com sucesso.")
    else:
        print("Produto não encontrado.")

def main():
    repo = ProdutoRepo()
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").lower()
        if opcao == 'a':
            cadastrar_produto(repo)
        elif opcao == 'b':
            listar_produtos(repo)
        elif opcao == 'c':
            alterar_produto(repo)
        elif opcao == 'd':
            excluir_produto(repo)
        elif opcao == 'e':
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
```

**Explicação:** 
 
- **Função `exibir_menu`:**  Exibe as opções disponíveis para o usuário no console.​
 
- **Função `obter_entrada_usuario`:**  Solicita a entrada do usuário, convertendo-a para o tipo especificado (`str`, `float` ou `int`). Em caso de erro na conversão, solicita nova entrada, garantindo que o programa não seja interrompido por exceções não tratadas.​
 
- **Função `cadastrar_produto`:**  Coleta os dados do novo produto, valida-os usando a classe `Produto` do Pydantic e, se válidos, adiciona o produto ao repositório. Em caso de erro de validação, informa o usuário.​
 
- **Função `listar_produtos`:**  Recupera e exibe todos os produtos cadastrados. Se não houver produtos, informa o usuário. Essa função é especial, pois usa a biblioteca `tabulate`. A tabela é construída em três etapas:​

    a) Preparação dos Dados: Criamos uma lista de listas chamada tabela, onde cada sublista contém os atributos de um produto: id, nome, preco (formatado como moeda brasileira) e estoque.​

    b) Definição dos Cabeçalhos: A lista cabecalhos contém os títulos das colunas que serão exibidos no topo da tabela.​

    c) Exibição da Tabela: Utilizamos a função tabulate para formatar e exibir os dados. O parâmetro tablefmt="grid" define o estilo da tabela com bordas, numalign="right" alinha os números à direita, e stralign="left" alinha os textos à esquerda.​
 
- **Função `alterar_produto`:**  Solicita o ID do produto a ser alterado, exibe suas informações atuais e permite ao usuário fornecer novos valores. Se o usuário deixar um campo em branco, o valor atual é mantido. Após validação, atualiza o produto no repositório.​
 
- **Função `excluir_produto`:**  Solicita o ID do produto a ser excluído e, se encontrado, remove-o do repositório.​
 
- **Função `main`:**  Inicializa o repositório e exibe o menu em um loop contínuo, permitindo ao usuário interagir com o sistema até optar por sair.​

**Observações Importantes:** 
 
- **Validação de Entrada:**  A função `obter_entrada_usuario` garante que as entradas do usuário sejam do tipo esperado, evitando exceções durante a execução.​
 
- **Tratamento de Exceções:**  As funções que interagem com o repositório tratam exceções, como `ValidationError`, informando o usuário sobre erros sem interromper abruptamente o programa.​
 
- **Uso do Pydantic:**  A classe `Produto` utiliza validadores personalizados para assegurar que os dados atendam aos critérios definidos antes de serem processados ou armazenados.​

Com essa estrutura, o programa oferece uma interface de console robusta e amigável para o gerenciamento de produtos, garantindo que as operações sejam realizadas de forma segura e eficiente.​