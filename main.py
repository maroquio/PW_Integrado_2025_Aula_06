from pydantic import ValidationError
from tabulate import tabulate
from produtos.produto_repo import ProdutoRepo
from produtos.produto import Produto

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