import flet as ft
from database import Database
from pessoa import Pessoa
from pessoa_repository import PessoaRepository

def main(page: ft.Page):
    # Configuração da página
    page.title = "Sistema de Cadastro de Pessoas"
    page.window_width = 800
    page.window_height = 600
    page.scroll = "adaptive"
    page.padding = 20
    
    # Inicializa o banco de dados e repositório
    db = Database()
    repositorio = PessoaRepository(db)
    
    # Componentes da UI
    titulo = ft.Text("Sistema de Cadastro de Pessoas", size=24, weight="bold")
    
    # Container para exibir mensagens
    mensagem = ft.Text("", color=ft.colors.RED)
    
    # Formulário para cadastro/edição
    id_controle = ft.TextField(label="ID", read_only=True, visible=False)
    nome = ft.TextField(label="Nome")
    email = ft.TextField(label="Email")
    idade = ft.TextField(label="Idade", keyboard_type=ft.KeyboardType.NUMBER)
    
    # Botões
    btn_salvar = ft.ElevatedButton("Salvar", icon=ft.icons.SAVE)
    btn_limpar = ft.ElevatedButton("Limpar", icon=ft.icons.CLEAR)
    
    # Tabela para exibir resultados
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Email")),
            ft.DataColumn(ft.Text("Idade")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[],
    )
    
    # Funções de manipulação de dados
    def limpar_formulario(e):
        id_controle.value = ""
        id_controle.visible = False
        nome.value = ""
        email.value = ""
        idade.value = ""
        page.update()
    
    def carregar_pessoas():
        pessoas = repositorio.listar()
        tabela.rows.clear()
        
        for pessoa in pessoas:
            def criar_editar_callback(p):
                return lambda e: editar_pessoa(p.id)
            
            def criar_excluir_callback(p):
                return lambda e: excluir_pessoa(p.id)
            
            tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(pessoa.id))),
                        ft.DataCell(ft.Text(pessoa.nome)),
                        ft.DataCell(ft.Text(pessoa.email)),
                        ft.DataCell(ft.Text(str(pessoa.idade))),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    icon_color=ft.colors.BLUE,
                                    tooltip="Editar",
                                    on_click=criar_editar_callback(pessoa)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    icon_color=ft.colors.RED,
                                    tooltip="Excluir",
                                    on_click=criar_excluir_callback(pessoa)
                                )
                            ])
                        ),
                    ]
                )
            )
        
        mensagem.value = f"{len(pessoas)} pessoas encontradas" if pessoas else "Nenhuma pessoa cadastrada"
        mensagem.color = ft.colors.GREEN
        page.update()
    
    def editar_pessoa(id_pessoa):
        pessoa = repositorio.listar_por_id(id_pessoa)
        
        if pessoa:
            id_controle.value = str(pessoa.id)
            id_controle.visible = True
            nome.value = pessoa.nome
            email.value = pessoa.email
            idade.value = str(pessoa.idade)
            
            mensagem.value = "Pessoa carregada para edição!"
            mensagem.color = ft.colors.GREEN
        else:
            mensagem.value = "Pessoa não encontrada!"
            mensagem.color = ft.colors.RED
        
        page.update()
    
    def salvar_pessoa(e):
        if not nome.value:
            mensagem.value = "O nome é obrigatório!"
            mensagem.color = ft.colors.RED
            page.update()
            return
        
        try:
            pessoa = Pessoa(nome.value, int(idade.value), email.value)
            
            if id_controle.value:  # Edição
                pessoa.id = int(id_controle.value)
                repositorio.atualizar(pessoa)
                mensagem.value = "Pessoa atualizada com sucesso!"
            else:  # Inserção
                repositorio.inserir(pessoa)
                mensagem.value = "Pessoa cadastrada com sucesso!"
            
            mensagem.color = ft.colors.GREEN
            limpar_formulario(e)
            carregar_pessoas()
        except ValueError:
            mensagem.value = "Idade deve ser um número válido!"
            mensagem.color = ft.colors.RED
        finally:
            page.update()
    
    def excluir_pessoa(id_pessoa):
        try:
            repositorio.deletar(id_pessoa)
            mensagem.value = f"Pessoa com ID {id_pessoa} foi excluída com sucesso!"
            mensagem.color = ft.colors.GREEN
        except Exception as ex:
            mensagem.value = f"Erro ao excluir pessoa: {str(ex)}"
            mensagem.color = ft.colors.RED
        
        limpar_formulario(None)
        carregar_pessoas()
    
    # Atribuir eventos aos botões
    btn_salvar.on_click = salvar_pessoa
    btn_limpar.on_click = limpar_formulario
    
    # Carrega as pessoas ao iniciar
    carregar_pessoas()
    
    # Layout da página
    page.add(
        ft.Column(
            [
                titulo,
                ft.Row([mensagem]),
                ft.Divider(),
                ft.Text("Formulário de Cadastro", weight="bold"),
                id_controle,
                nome,
                email,
                idade,
                ft.Row(
                    [
                        btn_salvar,
                        btn_limpar,
                    ],
                    spacing=10,
                ),
                ft.Divider(),
                ft.Text("Lista de Pessoas", weight="bold"),
                ft.Column([tabela], scroll="always", height=400),
            ],
            spacing=20,
        )
    )


# Para executar o app
if __name__ == "__main__":
    ft.app(target=main)