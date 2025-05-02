import sqlite3
from time import sleep
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


class Personal:
    def __init__(self):
        self.conexao = sqlite3.connect('academia.db')
        self.treinos = 'treinos.txt'
        self.cursor = self.conexao.cursor()

    def conectar_banco(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def salvar(self):
        self.conexao.commit()

    def cabecalho(self):
        print("-=" * 30)
        print("               Sistema do Personal Trainer")
        print("-=" * 30)
        lista = ['1- Acessar Avaliações', '2- Visualizar Progresso', '3- Visualizar Presenças',
                 '4- Atribuir Treinos', '5- Responder Dúvidas', '6- Redefinir Senha', '7- Sair']
        print("Opções")
        for elemento in lista:
            print(elemento)
        print("-=" * 30)

    def acessar_avaliacoes(self):
        self.cursor.execute(
            'SELECT * FROM avaliacoes WHERE personal_id IS NULL')
        avaliacoes = self.cursor.fetchall()

        if not avaliacoes:
            print("Nenhuma avaliação pendente.")
            return

        for avaliacao in avaliacoes:
            print(
                f"ID: {avaliacao[0]}, Aluno ID: {avaliacao[1]}, Disponibilidade: {avaliacao[2]}, Horário: {avaliacao[3]}")

        avaliacao_id = input(
            "Digite o ID da avaliação que deseja aceitar (se não aceitar nenhuma clique em enter nesse e nos proximos passos): ")
        personal_id = input("Digite seu ID de personal: ")

        self.cursor.execute(
            "SELECT disponibilidade, horario FROM avaliacoes WHERE id = ?", (avaliacao_id,))
        avaliacao = self.cursor.fetchone()

        if avaliacao:
            dias_disponiveis = avaliacao[0].split(',')
            horarios_disponiveis = avaliacao[1].split(',')

            print("Dias disponíveis:", dias_disponiveis)
            print("Horários disponíveis:", horarios_disponiveis)

            dia_escolhido = input("Escolha um dia: ")
            horario_escolhido = input("Escolha um horário: ")

            if dia_escolhido in dias_disponiveis and horario_escolhido in horarios_disponiveis:
                status = f"Avaliação marcada para {dia_escolhido} às {horario_escolhido} pelo Personal {personal_id}"
                self.cursor.execute("UPDATE avaliacoes SET status = ?, personal_id = ? WHERE id = ?",
                                    (status, personal_id, avaliacao_id))
                self.salvar()
                print("Avaliação aceita com sucesso!")
            else:
                print("Dia ou horário inválido.")

    def visualizar_progresso(self):
        nome = input("Digite o nome do aluno: ").strip().title()
        # Extraindo o id corretamente
        resultado = self.cursor.execute(
            'SELECT id FROM usuarios WHERE nome = ?', (nome,)
        ).fetchone()

        if resultado is None:
            print("Aluno não encontrado!")
            return

        # O valor do id está na primeira posição do resultado
        aluno_id = resultado[0]

        # Consultando os dados de progresso
        self.cursor.execute(
            "SELECT data, peso, imc FROM progresso WHERE aluno_id = ?", (
                aluno_id,)
        )
        progresso = self.cursor.fetchall()

        if not progresso:
            print("Nenhum dado de progresso encontrado!")
            return

        df = pd.DataFrame(progresso, columns=['Data', 'Peso', 'IMC'])
        print(df)

        opcao = input(
            "Deseja visualizar o gráfico de progresso? (S/N): ").strip().upper()
        if opcao == 'S':
            plt.figure(figsize=(10, 6))
            plt.plot(df['Data'], df['Peso'], marker='o',
                     linestyle='-', color='b')
            plt.xlabel("Data")
            plt.ylabel("Peso (Kg)")
            plt.title("Evolução do Peso")
            plt.grid(True)
            plt.show()

    def visualizar_presencas(self):
        nome = input("Digite o nome do aluno: ").strip().title()
        # Extraindo o id corretamente
        aluno_id = self.cursor.execute(
            'SELECT id FROM usuarios WHERE nome = ?', (nome, )).fetchone()

        if aluno_id is None:
            print("Aluno não encontrado!")
            return

        self.cursor.execute(
            'SELECT data, status FROM presencas WHERE usuario_id = ?', (aluno_id))
        presencas = self.cursor.fetchall()

        if not presencas:
            print("Nenhuma presença encontrada! ")
            return

        for presenca in presencas:
            print(f"Data: {presenca[0]}, Status: {presenca[1]}")

    def atribuir_treino(self):
        nome = input("Digite o nome do aluno: ").strip().title()
        # Extraindo o id corretamente
        aluno_id = self.cursor.execute(
            'SELECT id FROM usuarios WHERE nome = ?', (nome, )).fetchone()

        if aluno_id is None:
            print("Aluno não encontrado!")
            return

        # Acessando o valor correto da tupla
        aluno_id = aluno_id[0]

        print("Os treinos disponíveis são: \n")
        with open(self.treinos, 'r') as file:
            content = file.read()

        print(content)

        treino = input(
            f"\nDigite o nome do treino que quer atribuir para o aluno {nome}: \n")
        data_atual = datetime.today().strftime('%Y-%m-%d')

        self.cursor.execute("INSERT INTO treinos_personalizados (aluno_id, treino, data_atribuicao) VALUES (?, ?, ?)",
                            (aluno_id, treino, data_atual))
        self.salvar()
        print("Treino atribuído com sucesso!")

    def responder_duvida(self):
        # Recuperar todas as dúvidas pendentes
        self.cursor.execute(
            "SELECT id, aluno_id, duvida, status FROM duvidas WHERE status = 'Pendente'"
        )
        duvidas = self.cursor.fetchall()

        # Verificar se há dúvidas pendentes
        if not duvidas:
            print("Não há dúvidas pendentes no momento!")
            return

        # Exibir as dúvidas pendentes
        for duvida in duvidas:
            print(
                f'ID aluno: {duvida[1]}, Dúvida: {duvida[2]}, Status: {duvida[3]}')

        # Solicitar o ID da dúvida e validar o tipo de entrada
        try:
            duvida_id = int(
                input("Digite o ID da dúvida que deseja responder: ").strip())
        except ValueError:
            print("O ID deve ser um número inteiro.")
            return

        # Solicitar a resposta e atualizar o status da dúvida
        resposta = input("Digite a resposta: ")
        self.cursor.execute(
            "UPDATE duvidas SET resposta = ?, status = 'Respondida' WHERE aluno_id = ?",
            (resposta, duvida_id),
        )

        # Salvar as alterações no banco de dados
        self.salvar()
        print("Dúvida respondida com sucesso!")

    def redefinir_senha(self, email):
        senha_nova = input("Digite a nova senha: ").strip()

        self.cursor.execute(
            "UPDATE usuarios SET senha = ? WHERE email = ?", (senha_nova, email))
        self.salvar()
        print("Senha alterada com sucesso!")

    def tratar_entrada(self):
        while True:
            entrada = input(
                "Digite o número da sua escolha (1 a 7): ").strip()
            if entrada.isdigit():  # Verifica se a entrada é composta apenas por números
                numero = int(entrada)
                if 1 <= numero <= 7:  # Verifica se está no intervalo permitido
                    return numero
            print("Entrada inválida! Por favor, digite um número de 1 a 7.")

    def fechar_conexao(self):
        self.conn.close()


if __name__ == "__main__":
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
            email = input("Digite seu email para redefinir a senha: ").strip()
            personal.redefinir_senha(email)
        elif opcao == 7:
            print("Saindo do sistema...")
            break