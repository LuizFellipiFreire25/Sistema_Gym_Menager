import sqlite3
from time import sleep
from datetime import datetime
import matplotlib.pyplot as plt


class Aluno:
    def __init__(self):
        self.conexao = sqlite3.connect('academia.db')
        self.cursor = self.conexao.cursor()

    def salvar(self):
        self.conexao.commit()

    def cabecalho(self):
        print("-=" * 30)
        print("              Sistema do aluno, Seja bem vindo!")
        print("-=" * 30)
        print("Opções: ")
        lista = ['1- Treinos', '2- Avaliações', '3- Ver Status de avaliação', '4- Meu progresso',
                 '5- Faturas', '6- Enviar dúvida', '7- Redefinir senha', '8- Sair']
        for opcoes in lista:
            print(opcoes)
        print("-=" * 30)

    def treinos(self, email):
        usuario_id = self.cursor.execute(
            'SELECT id FROM usuarios WHERE email = ?', (email, )).fetchone()

        if usuario_id is not None:
            usuario_id = usuario_id[0]
            self.cursor.execute(
                'SELECT treino FROM treinos_personalizados WHERE aluno_id = ? ORDER BY data_atribuicao DESC LIMIT 1', (usuario_id, ))
            treino = self.cursor.fetchone()

            if treino:
                print(f"Treino atribuído: {treino[0]}")

            else:
                print("Nenhum treino personalizado encontrado.")
        else:
            print("Usuario nao encontrado!")

    def avaliacao(self, email):
        # Obtendo o ID do aluno com base no email
        self.cursor.execute(
            "SELECT id FROM usuarios WHERE email = ? AND tipo = 'Aluno'", (email,))
        aluno = self.cursor.fetchone()

        if not aluno:
            print("Aluno não encontrado!")
            return

        aluno_id = aluno[0]  # Pegamos o ID do aluno encontrado

        # Coletando informações da avaliação
        dias_disponiveis = input(
            "Informe os dias disponíveis separados por vírgula: ").strip()
        horarios_disponiveis = input(
            "Informe os horários disponíveis: ").strip()

        # Inserindo a avaliação com status pendente e sem personal atribuído ainda (NULL)
        self.cursor.execute("""
            INSERT INTO avaliacoes (aluno_id, disponibilidade, horario, status, personal_id)
            VALUES (?, ?, ?, ?, NULL)
        """, (aluno_id, dias_disponiveis, horarios_disponiveis, "Pendente"))

        self.salvar()
        print("Avaliação agendada com sucesso!")

    def ver_status_avaliacao(self, email):
        usuario_id = self.cursor.execute(
            'SELECT id FROM usuarios WHERE email = ?', (email, )).fetchone()

        if usuario_id is not None:
            usuario_id = usuario_id[0]
            self.cursor.execute(
                "SELECT status FROM avaliacoes WHERE aluno_id = ? ORDER BY id DESC LIMIT 1", (usuario_id,))
            status = self.cursor.fetchone()

            if status:
                print(f"Status da avaliação: {status[0]}")
            else:
                print("Nenhuma avaliação encontrada.")

    def meu_progresso(self, email):
        while True:
            try:
                peso = float(
                    input("Digite seu peso atual (Kg): ").replace(',', '.'))
                break
            except ValueError:
                print("Valor inválido! Por favor, digite um número para o peso.")

        while True:
            try:
                altura = float(
                    input("Digite sua altura (m): ").replace(',', '.'))
                break
            except ValueError:
                print("Valor inválido! Por favor, digite um número para a altura.")

        self.cursor.execute(
            "SELECT id FROM usuarios WHERE email = ? AND tipo = 'Aluno'", (email,))
        aluno = self.cursor.fetchone()
        aluno_id = aluno[0]  # Pegamos o ID do aluno encontrado

        imc = round(peso / (altura ** 2), 2)
        data_atual = datetime.today().strftime('%Y-%m-%d')

        self.cursor.execute("INSERT INTO progresso (aluno_id, data, peso, altura, imc) VALUES (?, ?, ?, ?, ?)",
                            (aluno_id, data_atual, peso, altura, imc))

        self.salvar()

        self.cursor.execute(
            "SELECT data, peso FROM progresso WHERE aluno_id = ?", (aluno_id,))
        progresso = self.cursor.fetchall()

        if not progresso:
            print("Nenhum dado de progresso encontrado!")
            return

        self.cursor.execute(
            "SELECT * FROM progresso WHERE aluno_id = ?", (aluno_id,))
        informacoes = self.cursor.fetchall()
        print(informacoes)

        if progresso:
            datas, pesos = zip(*progresso)
            plt.figure(figsize=(10, 6))
            plt.bar(datas, pesos, color='b', alpha=0.7)
            plt.xlabel("Data")
            plt.ylabel("Peso (Kg)")
            plt.title("Evolução do Peso")
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.show()
        else:
            print("Nenhum dado de progresso encontrado!")

    def faturas(self, email):
        usuario_id = self.cursor.execute(
            'SELECT id FROM usuarios WHERE email = ?', (email, )).fetchone()

        if usuario_id is not None:
            usuario_id = usuario_id[0]
            mes_atual = datetime.today().strftime("%m/%Y")
            status = self.cursor.execute(
                'SELECT status FROM faturas WHERE usuario_id = ? AND mes_referencia = ?', (usuario_id, mes_atual)).fetchone()

            if status is not None:
                status = status[0]
                print(f'Status da fatura: {status}')
            else:
                print('Nenhuma fatura encontrada para este mês.')
        else:
            print('Email não encontrado.')

    def enviar_duvida(self, email):
        usuario_id = self.cursor.execute(
            'SELECT id FROM usuarios WHERE email = ?', (email, )).fetchone()

        if usuario_id is not None:
            usuario_id = usuario_id[0]
            self.cursor.execute(
                "SELECT status FROM duvidas WHERE aluno_id = ? ORDER BY id DESC LIMIT 1", (usuario_id, ))
            pendente = self.cursor.fetchone()

            if pendente and pendente[0] == 'Pendente':
                print(
                    "Você já tem uma dúvida pendente. Aguarde a resposta antes de enviar outra.")
                return

            else:
                duvida = input("Digite sua dúvida: ").strip()
                data_atual = datetime.today().strftime("%Y-%m-%d")
                self.cursor.execute("INSERT INTO duvidas (aluno_id, data, duvida, resposta, status) VALUES (?, ?, ?, ?, ?)",  (
                    usuario_id, data_atual, duvida, "Aguardando resposta do personal", "Pendente"))
                self.salvar()
                print("Sua dúvida foi enviada!")

        else:
            print("Usuário não encontrado!")

    def redefinir_senha(self, email):
        senha_nova = input("Digite a nova senha: ").strip()
        sleep(1)
        self.cursor.execute(
            "UPDATE usuarios SET senha = ? WHERE email = ?", (senha_nova, email))
        self.salvar()
        print("Senha alterada com sucesso!")

    def fechar_conexao(self):
        self.conexao.close()

    def tratar_entrada(self):
        while True:
            entrada = input(
                "Digite o número da sua escolha (1 a 8): ").strip()
            if entrada.isdigit():  # Verifica se a entrada é composta apenas por números
                numero = int(entrada)
                if 1 <= numero <= 8:  # Verifica se está no intervalo permitido
                    return numero
            print("Entrada inválida! Por favor, digite um número de 1 a 8.")


if __name__ == "__main__":
    user = Aluno()
    email = input("Digite seu email para login: ").strip()
    sleep(1)
    while True:
        user.cabecalho()
        opcao = user.tratar_entrada()
        if opcao == 1:
            user.treinos(email)
        elif opcao == 2:
            user.avaliacao(email)
        elif opcao == 3:
            user.ver_status_avaliacao(email)
        elif opcao == 4:
            user.meu_progresso(email)
        elif opcao == 5:
            user.faturas(email)
        elif opcao == 6:
            user.enviar_duvida(email)
        elif opcao == 7:
            user.redefinir_senha(email)
        elif opcao == 8:
            print("Saindo do sistema...")
            user.fechar_conexao()
            break
