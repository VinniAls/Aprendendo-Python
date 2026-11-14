import json
import os   
from dataclasses import asdict, dataclass
from pathlib import Path

ARQUIVO = Path(__file__).with_name('restaurante.json')

BANNER =  ('''
░██████╗░█████╗░██████╗░░█████╗░██████╗░  ███████╗██╗░░██╗██████╗░██████╗░███████╗░██████╗░██████╗
██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗  ██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝
╚█████╗░███████║██████╦╝██║░░██║██████╔╝  █████╗░░░╚███╔╝░██████╔╝██████╔╝█████╗░░╚█████╗░╚█████╗░
░╚═══██╗██╔══██║██╔══██╗██║░░██║██╔══██╗  ██╔══╝░░░██╔██╗░██╔═══╝░██╔══██╗██╔══╝░░░╚═══██╗░╚═══██╗
██████╔╝██║░░██║██████╦╝╚█████╔╝██║░░██║  ███████╗██╔╝╚██╗██║░░░░░██║░░██║███████╗██████╔╝██████╔╝
╚═════╝░╚═╝░░╚═╝╚═════╝░░╚════╝░╚═╝░░╚═╝  ╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░░╚═╝╚══════╝╚═════╝░╚═════╝░ 
''') 
@dataclass
class Restaurante:
    nome: str
    categoria: str
    ativo: bool = True

def carregar() -> list[Restaurante]:
    """Lê os restaurantes do arquivo JSON; usa os dados iniciais se não houver."""
    try:
        dados = json.loads(ARQUIVO.read_text(encoding='utf-8'))
        return [Restaurante(**item) for item in dados]
    except (json.JSONDecodeError, TypeError, OSError):
        print('Aviso: não foi possível ler o arquivo de dados. Usando dados iniciais.')
        return restaurantes_iniciais()

def salvar(restaurantes: list[Restaurante]) -> None:
    """Grava a lista de restaurantes no arquivo JSON."""
    conteudo = json.dumps(
        [asdict(r) for r in restaurantes], ensure_ascii=False, indent=2
    )
    ARQUIVO.write_text(conteudo, encoding='utf-8')


def buscar_restaurante(restaurantes: list[Restaurante], nome: str) -> Restaurante | None:
    """Procura um restaurante pelo nome, ignorando maiúsculas e espaços nas pontas."""
    nome_normalizado = nome.strip().casefold()
    for restaurante in restaurantes:
        if restaurante.nome.casefold() == nome_normalizado:
            return restaurante
    return None


def adicionar_restaurante(
    restaurantes: list[Restaurante], nome: str, categoria: str
) -> Restaurante:
    """Cadastra um restaurante ativo. Lança ValueError se os dados forem inválidos."""
    nome = nome.strip()
    categoria = categoria.strip()
    if not nome or not categoria:
        raise ValueError('O nome e a categoria não podem ficar vazios.')
    if buscar_restaurante(restaurantes, nome):
        raise ValueError(f'O restaurante {nome} já está cadastrado.')
    novo = Restaurante(nome, categoria)
    restaurantes.append(novo)
    return novo


def alternar_status(restaurantes: list[Restaurante], nome: str) -> Restaurante | None:
    """Inverte o status (ativo/inativo). Retorna None se não encontrar."""
    restaurante = buscar_restaurante(restaurantes, nome)
    if restaurante:
        restaurante.ativo = not restaurante.ativo
    return restaurante


# ---------------------------------------------------------------------------
# Interface de terminal
# ---------------------------------------------------------------------------

def limpar_tela() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def exibir_nome_do_programa() -> None:
    print(BANNER)


def exibir_subtitulo(texto: str) -> None:
    limpar_tela()
    linha = '*' * (len(texto) + 4)
    print(linha)
    print(texto)
    print(linha)
    print()


def pausar() -> None:
    input('\nAperte Enter para voltar ao menu principal...')


def cadastrar_novo_restaurante(restaurantes: list[Restaurante]) -> None:
    exibir_subtitulo('Cadastrar Restaurante')
    nome = input('Digite o nome do restaurante que deseja cadastrar: ')
    categoria = input(f'Digite a categoria do restaurante {nome.strip()}: ')
    try:
        novo = adicionar_restaurante(restaurantes, nome, categoria)
    except ValueError as erro:
        print(f'\n{erro}')
        return
    salvar(restaurantes)
    print(f'\nRestaurante {novo.nome} cadastrado com sucesso!')


def listar_restaurantes(restaurantes: list[Restaurante]) -> None:
    exibir_subtitulo('Listar Restaurantes')
    if not restaurantes:
        print('Nenhum restaurante cadastrado.')
        return

    cabecalho_nome = 'Nome do Restaurante'
    cabecalho_categoria = 'Categoria'
    largura_nome = max(len(cabecalho_nome), *(len(r.nome) for r in restaurantes))
    largura_categoria = max(len(cabecalho_categoria), *(len(r.categoria) for r in restaurantes))

    print(f'{cabecalho_nome.ljust(largura_nome)} | '
          f'{cabecalho_categoria.ljust(largura_categoria)} | Status')
    print('-' * (largura_nome + largura_categoria + 15))
    for r in restaurantes:
        status = 'Ativo' if r.ativo else 'Inativo'
        print(f'{r.nome.ljust(largura_nome)} | {r.categoria.ljust(largura_categoria)} | {status}')


def alterar_status_restaurante(restaurantes: list[Restaurante]) -> None:
    exibir_subtitulo('Alterar o Status do Restaurante')
    nome = input('Digite o nome do restaurante que deseja alterar o status: ')
    restaurante = alternar_status(restaurantes, nome)
    if restaurante is None:
        print(f'\nO restaurante {nome.strip()} não foi encontrado.')
        return
    salvar(restaurantes)
    situacao = 'ativo' if restaurante.ativo else 'inativo'
    print(f'\nO restaurante {restaurante.nome} agora está {situacao}.')


def finalizar_app() -> None:
    exibir_subtitulo('Finalizando o aplicativo...')


# Cada opção: número -> (texto do menu, função). Para criar uma opção nova,
# basta adicionar uma linha aqui.
MENU = {
    '1': ('Cadastrar restaurante', cadastrar_novo_restaurante),
    '2': ('Listar restaurantes', listar_restaurantes),
    '3': ('Alterar status do restaurante', alterar_status_restaurante),
}
OPCAO_SAIR = '4'


def exibir_opcoes() -> None:
    print()
    for numero, (texto, _) in MENU.items():
        print(f'    {numero}. {texto}')
    print(f'    {OPCAO_SAIR}. Sair')


def escolher_opcao(restaurantes: list[Restaurante]) -> bool:
    """Lê a opção do usuário e executa a ação. Retorna False quando for sair."""
    escolha = input('\nEscolha uma opção: ').strip()

    if escolha == OPCAO_SAIR:
        return False

    if escolha in MENU:
        _, acao = MENU[escolha]
        acao(restaurantes)
    else:
        print('Opção inválida! Por favor, escolha uma opção válida.')

    pausar()
    return True


def main() -> None:
    restaurantes = carregar()
    try:
        while True:
            limpar_tela()
            exibir_nome_do_programa()
            exibir_opcoes()
            if not escolher_opcao(restaurantes):
                break
    except (KeyboardInterrupt, EOFError):
        print()
    finalizar_app()

if __name__ == '__main__':
    main()