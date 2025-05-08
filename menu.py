from database import Database
from pessoa import Pessoa
from pessoa_repository import PessoaRepository

def exibir_menu():
    print("\n--- MENU ---")
    print("1. Inserir pessoa")
    print("2. Listar pessoas")
    print("3. Listar pessoa por ID")
    print("4. Editar pessoa")
    print("5. Deletar pessoa")
    print("0. Sair")

def main():

    db = Database()
    repositorio = PessoaRepository(db)

    while True:

        exibir_menu()
        opcao = int(input('Escolha uma Opção: '))

        if opcao == 1:

            nome = input('Digite o nome: ')
            email = input('Digite o email: ')
            idade = input('Digite a idade: ')
            pessoa = Pessoa(nome, email, idade)
            repositorio.inserir(pessoa)
            print('Pessoa Cadastrada com Sucesso!')

        elif opcao == 2:

            pessoas = repositorio.listar()
            print(pessoas)

        elif opcao == 3:
            id = int(input('Digite o ID da pessoa: '))
            pessoa = repositorio.listar_por_id(id)
            print(pessoa)

        elif opcao == 4:
            id = int(input('Digite o ID da pessoa: '))
            pessoa = repositorio.listar_por_id(id)
            if pessoa:
                pessoa.nome = input('Digite o nome: ') or pessoa.nome
                pessoa.email = input('Digite o email: ') or pessoa.email
                pessoa.idade = input('Digite a idade: ') or pessoa.idade
                repositorio.atualizar(pessoa)
                print("Pessoa atualizada")
            else:
                print("Pessoa não localizada!")

        elif opcao == 5:
            id = int(input('Digite o ID da pessoa: '))
            pessoa = repositorio.listar_por_id(id)
            print(pessoa)
            if pessoa:
                repositorio.deletar(id)
                print(f"Pessoa com ID {id} foi deletada!")
            else:
                print("Pessoa não localizada!")

        elif opcao == 0:
            print("Encerrando...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
