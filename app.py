import json
import os   
from dataclasses import asdict, dataclass
from pathlib import Path

ARQUIVO = Path(__file__).with_name('restaurante.json')

restaurantes = [{'nome': 'Sabor Mineiro', 'categoria': 'Comida Mineira', 'ativo': True}, 
                {'nome': 'Pizza Express', 'categoria': 'Pizza', 'ativo': False}, 
                {'nome': 'Habbib', 'categoria': 'Árabe', 'ativo': True}
]

def exibir_nome_do_programa():
    print ('''
░██████╗░█████╗░██████╗░░█████╗░██████╗░  ███████╗██╗░░██╗██████╗░██████╗░███████╗░██████╗░██████╗
██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗  ██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝
╚█████╗░███████║██████╦╝██║░░██║██████╔╝  █████╗░░░╚███╔╝░██████╔╝██████╔╝█████╗░░╚█████╗░╚█████╗░
░╚═══██╗██╔══██║██╔══██╗██║░░██║██╔══██╗  ██╔══╝░░░██╔██╗░██╔═══╝░██╔══██╗██╔══╝░░░╚═══██╗░╚═══██╗
██████╔╝██║░░██║██████╦╝╚█████╔╝██║░░██║  ███████╗██╔╝╚██╗██║░░░░░██║░░██║███████╗██████╔╝██████╔╝
╚═════╝░╚═╝░░╚═╝╚═════╝░░╚════╝░╚═╝░░╚═╝  ╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░░╚═╝╚══════╝╚═════╝░╚═════╝░ 
''') 

def exibir_opcoes():
    print ('''
    1. Cadastrar restaurante
    2. Listar restaurantes
    3. Alterar status do restaurante
    4. Sair ''')

def voltar_ao_menu_principal():
    input ('Aperte Enter para voltar ao menu principal...')
    main()

def opcao_invalida():
    print ('Opção inválida! Por favor, escolha uma opção válida.')
    voltar_ao_menu_principal()

def exibir_subtitulo(texto):
    os.system('cls')
    linha = '*' * (len(texto) + 4)
    print (linha)
    print (texto)
    print (linha)
    print() 

def cadastrar_novo_restaurante():
    exibir_subtitulo('Cadastrar Restaurante: ')
    nome_do_restaurante = input('Digite o nome do restaurante que deseja cadastrar: ')
    categoria = input(f'Digite a categoria do restaurante {nome_do_restaurante}: ')
    dados_do_restaurante = {'nome':nome_do_restaurante, 
                            'categoria':categoria, 
                            'ativo':True}
    restaurantes.append(dados_do_restaurante)
    print (f'Restaurante {nome_do_restaurante} cadastrado com sucesso!')
    voltar_ao_menu_principal()

def listar_restaurantes():
    exibir_subtitulo('Listar Restaurantes: ')

    print(f'{"Nome do Restaurante".ljust(22)} | {"  Categoria".ljust(20)} | Status')
    for restaurante in restaurantes:
        nome_restaurante = restaurante['nome']
        categoria = restaurante['categoria']
        ativo = restaurante['ativo']
        print(f'- {nome_restaurante.ljust(20)} | {categoria.ljust(20)} | {"Ativo" if ativo else "Inativo"}')
    voltar_ao_menu_principal()

def alterar_status_restaurante():
    exibir_subtitulo('Alterar o Status do Restaurante: ')
    nome_restaurante = input('Digite o nome do restaurante que deseja alterar o status: ')
    restaurante_encontrado = False
    for restaurante in restaurantes:
        if nome_restaurante == restaurante['nome']:
            restaurante_encontrado = True
            restaurante['ativo'] = not restaurante['ativo']
            mensagem = ( f'O Restaurante {nome_restaurante} agora está ativo.'
            if restaurante['ativo'] else f'O Restaurante {nome_restaurante} agora está inativo. '
            )
            print(mensagem)
    if not restaurante_encontrado:
        print(f'O Restaurante {nome_restaurante} não foi encontrado.')        
    voltar_ao_menu_principal()

def finalizar_app():
    exibir_subtitulo('Finalizando o aplicativo...')
        

def escolher_opcao():
    try:
        opcao_escolhida = int(input('\nEscolha uma opção: '))

        if opcao_escolhida == 1:
            cadastrar_novo_restaurante()
        elif opcao_escolhida == 2:
            listar_restaurantes()
        elif opcao_escolhida == 3:
            alterar_status_restaurante()          
        elif opcao_escolhida == 4: 
            finalizar_app()  
        else:
            opcao_invalida()
    except ValueError:
        print ('Opção inválida! Por favor, escolha uma opção válida.')
        input ('Aperte Enter para voltar ao menu principal...')
        main()

def main():
    os.system('cls')
    exibir_nome_do_programa()
    exibir_opcoes()
    escolher_opcao()

if __name__ == '__main__':
    main()