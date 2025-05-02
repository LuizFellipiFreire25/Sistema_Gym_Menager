import sqlite3
from time import sleep
from Administrador import Administrador
from Aluno import Aluno
from Personal import Personal


def conectar_banco():
    return sqlite3.connect("academia.db")


def opcoes():
    print("-=" * 30)
    print("                 Sistema de gestão Gym...")
    print("-=" * 30)
    print("Opções: ")
    lista = ['1. Login', '2. Cadastrar', '3. Sair']
    for elemento in lista:
        print(elemento)
    print("-=" * 30)


def login():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    email = input("Digite seu email: ").strip()
    senha = input("Digite a sua senha: ").strip()

    cursor.execute(
        "SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    usuario = cursor.fetchone()

    if usuario:
        tipo_usuario = usuario[4]  # Coluna do tipo do usuário

        if tipo_usuario == 'Administrador':
            funcoes_administrador()
        elif tipo_usuario == 'Aluno':
            funcoes_aluno(email)
        elif tipo_usuario == 'Personal':
            funcoes_personal(email)
        else:
            print("Acesso negado!")
    else:
        print("Usuário não encontrado! Tente novamente.")

    conexao.close()


def cadastro():
    print("Somente Administradores podem cadastrar no nosso sistema...")
    sleep(1)
    print("Vamos verificar se você é um Administrador!")
    sleep(1)

    email = input("Digite seu email: ").strip()
    senha = input("Digite sua senha: ").strip()

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE email = ? AND senha = ? AND tipo = 'Administrador'", (email, senha))
    usuario = cursor.fetchone()

    if usuario:
        print("Você é um administrador! Acessando o sistema...")
        sleep(1)
        admin = Administrador()
        admin.cadastrar_usuario()
    else:
        print("Acesso negado! Você não é um administrador")

    conexao.close()


def funcoes_administrador():
    admin = Administrador()
    while True:
        admin.cabecalho()
        opcao = admin.tratar_entrada()
        if opcao == 1:
            admin.cadastrar_usuario()
        elif opcao == 2:
            admin.ver_usuario()
        elif opcao == 3:
            admin.cadastrar_plano()
        elif opcao == 4:
            admin.registrar_pagamento()
        elif opcao == 5:
            admin.registrar_presenca()
        elif opcao == 6:
            admin.gerar_relatorio_frequencia()
        elif opcao == 7:
            admin.alterar_informacoes_alunos()
        elif opcao == 8:
            admin.visualizar_pagos()
        elif opcao == 9:
            admin.redefinir_senha()
        elif opcao == 10:
            print("Saindo do sistema...")
            admin.fechar_conexao()
            break


def funcoes_aluno(email):
    aluno = Aluno()
    while True:
        aluno.cabecalho()
        opcao = aluno.tratar_entrada()
        if opcao == 1:
            aluno.treinos(email)
        elif opcao == 2:
            aluno.avaliacao(email)
        elif opcao == 3:
            aluno.ver_status_avaliacao(email)
        elif opcao == 4:
            aluno.meu_progresso(email)
        elif opcao == 5:
            aluno.faturas(email)
        elif opcao == 6:
            aluno.enviar_duvida(email)
        elif opcao == 7:
            aluno.redefinir_senha(email)
        elif opcao == 8:
            print("Saindo do sistema...")
            aluno.fechar_conexao()
            break


def funcoes_personal(email):
    personal = Personal()
    while True:
        personal.cabecalho()
        opcao = personal.tratar_entrada()
        if opcao == 1:
            personal.acessar_avaliacoes()
        elif opcao == 2:
            personal.visualizar_progresso()
        elif opcao == 3:
            personal.visualizar_presencas()
        elif opcao == 4:
            personal.atribuir_treino()
        elif opcao == 5:
            personal.responder_duvida()
        elif opcao == 6:
            personal.redefinir_senha(email)
        elif opcao == 7:
            print("Saindo do sistema...")
            break


if __name__ == "__main__":
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