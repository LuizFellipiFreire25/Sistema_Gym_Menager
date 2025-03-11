import sqlite3
from time import sleep
from datetime import datetime
import random
import pandas as pd


class Administrador:
    def __init__(self, db_path='academia.db'):
        self.db_path = db_path
        self.conectar_banco()

    # método que vai criar a conexão com o banco de dados
    def conectar_banco(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    # método que vai interromper a conexão com o banco de dados
    def fechar_conexao(self):
        self.conn.close()

    # método que vai salvar as alterações
    def salvar(self):
        self.conn.commit()

    # cabeçalho
    def cabecalho(self):
        print('-=' * 30)
        print("                 Sistema do Administrador ")
        print('-=' * 30)
        print("Opções: ")
        lista = ['1. Cadastrar Usuário', '2. Ver Usuário', '3. Cadastrar Plano',
                 '4. Registrar Pagamento', '5. Registrar Presença', '6. Gerar Relatório Frequência',
                 '7. Alterar Informações de Alunos', '8. Visualizar Pagamentos', '9. Redefinir Senha', '10. Sair']
        for elemento in lista:
            print(elemento)
        print('-=' * 30)

    # método que vai cadastrar os usuários
    def cadastrar_usuario(self):
        email = input("Digite o email: ").strip()
        self.cursor.execute(
            'SELECT * FROM usuarios WHERE email = ?', (email, ))

        if self.cursor.fetchone():
            print("Já cadastrado! ")
            return

        while True:
            id = random.randint(1000, 9999)
            self.cursor.execute(
                'SELECT * FROM usuarios WHERE email = ?', (email, ))
            if not self.cursor.fetchone():
                break

        nome = input("Digite o Nome: ").strip().title()
        senha = input("Digite uma Senha: ").strip()
        plano = input(
            "Digite o tipo de plano (se for Administrador ou personal digite Nenhum): ").strip()
        tipo = input(
            "O usuário será Administrador, Personal ou Aluno? (A para Admin, L para Aluno e P para Personal): ").strip().upper()
        tipo = "Administrador" if tipo == "A" else "Aluno" if tipo == "L" else "Personal"

        print("Gerando um ID...")
        sleep(2)
        print(f"{nome}, seu ID é: {id}")
        sleep(2)

        self.cursor.execute(
            'INSERT INTO usuarios (id, nome, email, senha, tipo, plano) VALUES (?,?,?,?,?,?)', (id, nome, email, senha, tipo, plano))

        self.salvar()
        print("Usuário cadastrado com sucesso")

    # método que vai visualizar um usuário
    def ver_usuario(self):
        nome = input(
            "Digite o nome do usuário que você deseja filtrar: ").strip().title()
        self.cursor.execute('SELECT * FROM usuarios WHERE nome = ?', (nome, ))
        usuario = self.cursor.fetchone()
        if usuario:
            print("Usuário encontrado! ")
            sleep(1)
            print(usuario)
            sleep(1)

        print("Usuário não encontrado...")

    # método que vai cadastrar algum plano
    def cadastrar_plano(self):
        visualizar_planos = input(
            "Deseja visualizar os planos existentes antes de adicionar um novo? (s/n): ").strip().lower()[0]
        if visualizar_planos == 's':
            self.cursor.execute('SELECT * FROM planos')
            planos = self.cursor.fetchall()

            if planos:
                print("Planos existentes: ")
                for plano in planos:
                    print(
                        f"ID: {plano[0]}, Nome: {plano[1]}, Duração: {plano[2]}, Valor: {plano[3]}, Benefícios: {plano[4]}")

            else:
                print("Não há planos cadastrados! ")

            nome_plano = input("Digite o nome do novo plano: ").title().strip()
            duracao = input("Digite a duração do novo plano: ").title().strip()
            valor = input("Digite o valor do novo Plano: ").strip()
            beneficios = input(
                "Digite os benefícios do novo plano (separados por vírgula): ").strip()

            self.cursor.execute('INSERT INTO planos (nome, duracao, valor, beneficios) VALUES (?,?,?,?)', (
                nome_plano, duracao, valor, beneficios))
            self.salvar()

            print("Novo plano salvo com sucesso! ")

    # método que vai registrar pagamento para a data atual
    def registrar_pagamento(self):
        email = input("Digite o email do aluno: ").strip()
        self.cursor.execute(
            "SELECT id, nome FROM usuarios WHERE email = ? AND tipo = 'Aluno'", (email,))
        aluno = self.cursor.fetchone()

        if not aluno:
            print("Aluno não encontrado!")
            return

        id_aluno, nome = aluno
        data_pagamento = datetime.today().strftime('%d/%m/%Y')
        mes_referencia = datetime.today().strftime('%m/%Y')

        self.cursor.execute(
            "SELECT * FROM faturas WHERE id_aluno = ? AND mes = ?", (id_aluno, mes_referencia))
        if self.cursor.fetchone():
            print("Pagamento já registrado para este mês!")
            return

        self.cursor.execute("INSERT INTO faturas (id_aluno, nome, email, mes, data_pagamento, status) VALUES (?, ?, ?, ?, ?, 'Pago')",
                            (id_aluno, nome, email, mes_referencia, data_pagamento))
        self.salvar()
        print("Pagamento registrado com sucesso!")

    # método que vai visualizar os pagos
    def visualizar_pagos(self):
        self.cursor.execute("SELECT * FROM faturas")
        pagamentos = self.cursor.fetchall()
        if pagamentos:
            for pagamento in pagamentos:
                print(pagamento)
        else:
            print("Nenhum pagamento registrado!")

    # método que vai registrar presenças
    def registrar_presenca(self):
        email = input("Digite o email do aluno: ").strip()

        # Verifica se o aluno existe
        self.cursor.execute(
            "SELECT id, nome FROM usuarios WHERE email = ? AND tipo = 'Aluno'", (email,))
        aluno = self.cursor.fetchone()

        if not aluno:
            print("Aluno não encontrado!")
            return

        id_aluno, nome = aluno
        dia_semana = datetime.today().strftime('%A')

        # Tradução dos dias para português
        dias_traduzidos = {
            'Monday': 'Segunda', 'Tuesday': 'Terça', 'Wednesday': 'Quarta',
            'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado'
        }

        if dia_semana not in dias_traduzidos:
            print("Hoje não é dia de treino (Domingo).")
            return

        dia_atual = dias_traduzidos[dia_semana]

        # Verifica se a presença já foi registrada
        self.cursor.execute(
            "SELECT * FROM presencas WHERE id_aluno = ? AND dia = ?", (id_aluno, dia_atual))
        if self.cursor.fetchone():
            print("Presença já registrada para hoje!")
            return

        # Registra a presença na tabela
        self.cursor.execute("INSERT INTO presencas (id_aluno, nome, email, dia, status) VALUES (?, ?, ?, 'Presente')",
                            (id_aluno, nome, dia_atual))

        self.salvar()
        print(f"Presença registrada para {nome} no dia {dia_atual}.")

    # método que vai redefinir a senha do usuario
    def redefinir_senha(self):
        email = input("Digite seu email: ").strip()
        self.cursor.execute(
            "SELECT senha FROM usuarios WHERE email = ?", (email, ))
        usuario = self.cursor.fetchone()

        if not usuario:
            print("Usuário não encontrado!")
            return

        nova_senha = input("Digite sua nova senha: ").strip()
        self.cursor.execute(
            "UPDATE usuarios SET senha = ? WHERE email = ?", (nova_senha, email))
        self.salvar()
        print("Senha redefinida com sucesso!")

    def __del__(self):
        self.fechar_conexao()

    # método que vai contar o total de presencas e salvar em um arquivo csv
    def gerar_relatorio_frequencia(self):
        self.cursor.execute(
            "SELECT id_aluno, nome, COUNT(*) as total_presencas FROM presencas GROUP BY id_aluno")
        frequencias = self.cursor.fetchall()

        if not frequencias:
            print("Nenhuma presença registrada ainda!")
            return

        print("\n📊 Relatório de Frequência dos Alunos 📊")
        print("-" * 50)
        for id_aluno, nome, total in frequencias:
            print(f"Aluno: {nome} | Total de Presenças: {total}")

        # Opcional: Salvar em um arquivo CSV
        opcao = input(
            "Deseja salvar o relatório em um arquivo CSV? (S/N): ").strip().upper()
        if opcao == "S":
            df = pd.DataFrame(frequencias, columns=[
                              "ID_Aluno", "Nome", "Total_Presenças"])
            df.to_csv("relatorio_frequencia.csv", index=False)
            print("Relatório salvo como 'relatorio_frequencia.csv'.")

        print("-" * 50)

    # método que vai alterar as informações dos alunos
    def alterar_informacoes_alunos(self):
        nome = input(
            "Digite o nome do aluno que deseja alterar: ").strip().title()

        # Verifica se o aluno existe
        self.cursor.execute(
            "SELECT id FROM usuarios WHERE nome = ? AND tipo = 'Aluno'", (nome,))
        aluno = self.cursor.fetchone()

        if not aluno:
            print("Aluno não encontrado!")
            return

        print("Aluno encontrado! Digite as novas informações ou pressione Enter para manter as atuais.")

        novo_email = input("Novo email: ").strip()
        novo_plano = input("Novo tipo de plano: ").strip()
        nova_senha = input("Nova senha: ").strip()

        if novo_email:
            self.cursor.execute(
                "UPDATE usuarios SET email = ? WHERE nome = ?", (novo_email, nome))

        if novo_plano:
            self.cursor.execute(
                "UPDATE usuarios SET plano = ? WHERE nome = ?", (novo_plano, nome))

        if nova_senha:
            self.cursor.execute(
                "UPDATE usuarios SET senha = ? WHERE nome = ?", (nova_senha, nome))

        self.salvar()
        print("Informações do aluno atualizadas com sucesso!")

    # método que vai alterar informações de alunos
if __name__ == "__main__":
    admin = Administrador()
    while True:
        admin.cabecalho()
        opcao = input("Digite o número da sua escolha: ").strip()
        if opcao == '1':
            admin.cadastrar_usuario()
        elif opcao == '2':
            admin.ver_usuario()
        elif opcao == '3':
            admin.cadastrar_plano()
        elif opcao == '4':
            admin.registrar_pagamento()
        elif opcao == '5':
            admin.registrar_presenca()
        elif opcao == '6':
            admin.gerar_relatorio_frequencia()
        elif opcao == '7':
            admin.alterar_informacoes_alunos()
        elif opcao == '8':
            admin.visualizar_pagos()
        elif opcao == '9':
            admin.redefinir_senha()
        elif opcao == '10':
            print("Saindo do sistema...")
            break
