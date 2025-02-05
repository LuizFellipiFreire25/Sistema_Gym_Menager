import pandas as pd
import os
from time import sleep
from datetime import date

arquivo = 'Visualizar_alunos.csv'


# verificando se o arquivo existe
if os.path.exists(arquivo):
    tabela = pd.read_csv(arquivo)
else:
    # mais pra frente gerar id aleatoriamente
    colunas = ['ID', 'Nome', 'Email', 'Tipo de plano']
    tabela = pd.DataFrame(columns=colunas)


def salvar():
    """
    aqui ele somente salva o arquivo usando o tabela.to_csv e o index = False é para nao salvar o índice, somente o conteúdo

    """
    tabela.to_csv(arquivo, index=False)
    print("SALVAMENTO CONCLUÍDO...")


def Cabeçalho():
    print('-=' * 30)
    print("                 Sistema do Administrador ")
    print('-=' * 30)
    print("Opções: ")
    lista = ['1. Cadastrar Usuário', '2. Ver Usuário', '3. Cadastrar Plano',
             '4. Registrar Pagamento', '5. Registrar Presença', '6. Gerar Relatório Frequência', '7. Alterar Informações de Alunos', '8. Sair']
    for elemento in lista:
        print(elemento)
    print('-=' * 30)


# cadastrando um usuário


def Cadastrar_Usuário():

    # chamando a variavle global tabela e o arquivo
    global tabela

    # pedindo o email do usuario
    email = input("Digite o email do aluno: ")

    # verificando se o usuario ja esta cadastrado
    if email in tabela['Email'].values:
        return 'Aluno já cadastrado!'

    # se nao estiver cadastrado, deve cadastrar
    else:
        id = input("Digite o ID do aluno: ")
        nome = input("Digite o Nome do aluno: ")
        senha = input("Digite uma Senha para o primeiro acesso do aluno: ")
        plano = input("Digite o tipo de plano do Aluno: ")
        novo = {'Nome': nome, 'ID': id, 'Tipo de Plano': plano, 'Email': email}
        tabela = tabela._append(novo, ignore_index=True)
        salvar()


# visualizando as informações de um usuário
def Ver_Usuário():
    global tabela
    id = int(input("Digite o id do Aluno que você deseja filtrar: "))
    # verificando se existe o id
    if id in tabela['ID'].values:
        print("Aluno encontrado...")
        sleep(1)
        aluno = tabela.loc[tabela['ID'] == id]
        print(aluno)
        sleep(1)
        print()

    else:
        print("Aluno não encontrado!")

# função que mostra os planos existentes e cadastra planos de treino em um arquivo


def Cadastrar_Plano():
    # abrindo o arquivo com os planos já criados
    with open('planos.txt', 'r') as arquivo:
        print("Os tipos de planos criados são...")
        print("")
        abrir = arquivo.read()
        print(abrir)

    # perguntado se o usuário deseja criar mais algum
    criar = input(
        "Você realmente deseja criar outro plano? digite S para sim e N para não: ").strip().upper()[0]

    # se realmente ele quiser
    if criar in 'S':

        # perguntando as informações necessárias
        nome_plano = input("Digite o nome do novo plano: ").title().strip()
        duracao = input("Digite a duração do novo plano: ").title().strip()
        valor = input("Digite o valor do novo Plano: ").title().strip()
        beneficios = []
        print("Digite os benefícios do novo plano: (digite 'fim' para parar)")

        # organizando as inputs e colocando cada palavra em capitalize
        while True:
            beneficio = input('- ').title()
            if beneficio.upper() == 'FIM':
                break
            beneficios.append(beneficio)

        # organizando o novo plano
        novo_plano = f'\n\n{nome_plano}\nDuração: {duracao}\nValor: {
            valor}\nBenefícios: \n' + "\n".join(f'- {b}' for b in beneficios)

        # adicionar o plano novo ao arquivo ja criado
        with open('planos.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(novo_plano)
            print("Novo plano salvo com sucesso! ")

    else:
        return 'Saindo...'


def Registrar_Pagamento():
    global tabela
    # filtrando o aluno pelo email
    email = input(
        "Digite o Email do aluno que você quer registrar o pagamento: ")
    if email in tabela['Email'].values:
        print("Id encontrado! ")
        # adicionando a coluna pago
        tabela.loc[tabela['Email'] == email, 'Pagamento'] = 'Pago'
        # garantindo que os alunos que nao pagaram nao vao estar como pago
        tabela['Pagamento'] = tabela['Pagamento'].fillna("Não Pago")
        # salvando
        salvar()
    else:
        print("Aluno não encontrado!")


# ainda nao sei como vou compor ela
# def Registrar_Presença():


# ainda nao sei como vou compor ela
# def Gerar_Relatório_Frequência():

def Alterar_Informações_Alunos():
    global tabela
    # filtrando o aluno pelo nome
    aluno = input(
        "Digite o nome do aluno que você deseja alterar informções: ")
    # verificando se ele existe
    if aluno in tabela['Nome'].values:
        print("Aluno encontrado!")
        print("Digite as novas informações que serão solicitadas abaixo ou pressione enter para manter as atuais!")
        # pegando as novas informações
        id = input("Digite o novo Id do aluno: ").strip()
        email = input("Digite o novo Email do aluno: ").strip()
        tipo_plano = input("Digite o novo Tipo de Plano do aluno: ").strip()
        pagamento = input(
            "Digite [1] para adicionar 'Pago' ou [2] para adicionar 'Não Pago' ao aluno: ").strip()
        # só vai considerar os campos se for não vazio
        if id:
            tabela.loc[tabela['Nome'] == aluno, 'ID'] == id
        if email:
            tabela.loc[tabela['Nome'] == aluno, 'Email'] == email
        if tipo_plano:
            tabela.loc[tabela['Nome'] == aluno, 'Tipo de Plano'] == tipo_plano
        if pagamento:
            tabela.loc[tabela['Nome'] == aluno,
                       'Pagamento'] == 'Pago' if pagamento == 1 else 'Não Pago'
        salvar()
    else:
        print("Aluno não encontrado")


def tratando(n):
    while True:
        try:
            n = int(n)
            if n in [1, 2, 3, 4, 5, 6, 7, 8]:
                return n
            else:
                n = input("Opção Inválida, digite novamente de 1 a 8: ")
        except (ValueError, TypeError):
            n = input("Opção inválida digite novamente: ")


while True:
    Cabeçalho()
    opcao = tratando(input("Digite a opção: ").strip()[0])
    if opcao == 1:
        Cadastrar_Usuário()
    elif opcao == 2:
        Ver_Usuário()
    elif opcao == 3:
        Cadastrar_Plano()
    elif opcao == 4:
        Registrar_Pagamento()
    elif opcao == 5:
        print("Função ainda em construção")
    elif opcao == 6:
        print("Função ainda em contrução")
    elif opcao == 7:
        Alterar_Informações_Alunos()
    elif opcao == 8:
        print("Saindo do sistema...")
        sleep(1)
        print("Obrigado!")
        break
print("Ainda em desenvolvimento!")
print("Teste")
