import pandas as pd
import os
from Administrador import Administrador
from time import sleep


def opcoes():
    # mostrando as opções do main.py
    print("-="*30)
    print("                 Sistema de gestão Gym...")
    print("-="*30)
    print("Opções: ")
    lista = ['1. Login', '2. Cadastrar', '3. Sair']
    for elemento in lista:
        print(elemento)
    print("-="*30)


def login():
    # verificando se o arquivo existe
    if not os.path.exists('Visualizar_alunos.csv'):
        print("Nenhum usuário cadastrado ainda!")
        return
    # pedindo o email do usuário
    email = input("Digite seu email: ").strip()
    # abrindo o arquivo criado em Administrador.py em forma de tabela
    tabela = pd.read_csv('Visualizar_alunos.csv')

    if email in tabela['Email'].values:
        # Obtendo a linha correspondente, iloc[0] garante que estarei filtrando a primeira linha do dataframe
        usuario = tabela[tabela['Email'] == email].iloc[0]
        if usuario['Tipo'] == 'Administrador':
            print("Login bem-sucedido! Acessando o sistema do Administrador...")
            sleep(0.5)
            # nas proximas 20 linhas eu repito o cabeçalho criado em Administrador.py pois aquele criado só acessa se eu executar aquele modulo
            admin = Administrador()  # atribuindo a classe Administrador a uma variavel
            while True:
                admin.Cabeçalho()
                opcao = admin.tratando(
                    input("Digite o número da sua escolha: ").strip()[0])
                if opcao == 1:
                    admin.Cadastrar_Usuário()
                elif opcao == 2:
                    admin.Ver_Usuário()
                elif opcao == 3:
                    admin.Cadastrar_Plano()
                elif opcao == 4:
                    admin.Registrar_Pagamento()
                elif opcao == 5:
                    print("Função ainda em construção")
                elif opcao == 6:
                    print("Função ainda em construção")
                elif opcao == 7:
                    admin.Alterar_Informações_Alunos()
                elif opcao == 8:
                    print("Saindo do sistema...")
                    break
        else:
            print("Acesso negado! Você não é um administrador.")
    else:
        print("Usuário não encontrado! Tente novamente.")


while True:
    opcoes()
    opcao = input("Digite o número da sua opção: ").strip()
    if opcao == '1':
        login()
    elif opcao == '2':
        print("Função de cadastro ainda não implementada.")
    elif opcao == '3':
        print("Saindo do sistema...")
        break
    else:
        print("Opção inválida! Tente novamente.")
