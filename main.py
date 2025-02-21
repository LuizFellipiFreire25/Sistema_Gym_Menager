import pandas as pd
import os
from Administrador import Administrador
from time import sleep
from Aluno import Aluno


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


def funcoes_administrador():
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
            admin.Registrar_Presença()
        elif opcao == 6:
            admin.Gerar_Relatório_Frequência()
        elif opcao == 7:
            admin.Alterar_Informações_Alunos()
        elif opcao == 8:
            admin.Visualizar_pagos()
        elif opcao == 9:
            print("Saindo do sistema...")
            break


def funcoes_aluno():
    print("Login bem-sucedido! Acessando o sistema do Aluno...")
    sleep(0.5)
    user = Aluno()
    while True:
        user.cabecalho()
        opcao = int(input("Digite o numero da sua opção: "))
        if opcao == 1:
            user.Treinos()
        elif opcao == 2:
            user.Treinos_extra()
        elif opcao == 3:
            user.Avaliacao()
        elif opcao == 4:
            user.Meu_progresso()
        elif opcao == 5:
            user.Faturas()
        elif opcao == 6:
            print("Ainda em construção")
        else:
            print("Saindo do sistema...")
            break


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
            funcoes_administrador()

        elif usuario['Tipo'] == 'Aluno':
            funcoes_aluno()

        else:
            print("Acesso negado!")

    else:
        print("Usuário não encontrado! Tente novamente.")


def cadastro():
    print("Somente Administradores podem cadastrar no nosso sistema...")
    sleep(1)
    print("Vamos verificar se você é um Admiministrador!")
    sleep(1)
    arquivo = "Visualizar_alunos.csv"

    # verificando se o arquivo principal existe
    if not os.path.exists(arquivo):
        return "Arquivo de banco de dados não encontrado"

    tabela = pd.read_csv(arquivo)
    email = input("Digite o seu email: ")
    # primeiro vou verificar se o email existe no df
    if email in tabela['Email'].values:
        usuario = tabela[tabela["Email"] == email].iloc[0]
        if usuario['Tipo'] == 'Administrador':
            print(
                "Você é um administrador! Estamos te encaminhando para o sistema do Administradores...")
            sleep(1)
            print(
                "Para cadastrar um usuário, basta escolher a opção correspondente do cabeçalho...")
            sleep(1)
            funcoes_administrador()
        else:
            print("Acesso negado! Você não é um administrador")
            return
    else:
        return "Usuário não encontrado"


while True:
    opcoes()
    opcao = input("Digite o número da sua opção: ").strip()
    if opcao == '1':
        login()
    elif opcao == '2':
        cadastro()
    elif opcao == '3':
        print("Saindo do sistema...")
        break
    else:
        print("Opção inválida! Tente novamente.")

# tenho que separar a parte da senha para login e cadastro e futuramente chamar as funções do personal
