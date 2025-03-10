import pandas as pd
import matplotlib.pyplot as plt
from time import sleep
import os
from datetime import datetime


class Personal:
    def __init__(self):
        self.arquivo = 'Visualizar_alunos.csv'
        self.avaliacoes = "Avaliacoes.csv"
        self.progresso = "pregresso.csv"
        self.presencas = "presencas.csv"
        self.treinos_personalizados = "treinos_personalizados.csv"
        self.anotacoes = "anotacoes_personal.csv"
        self.relatorio_frequencia = "relatorio_frequencia.csv"
        self.treinos = "treinos.txt"
        self.duvidas = 'duvidas_alunos.csv'

    def cabecalho(self):
        print("-=" * 30)
        print("               Sistema do Personal Trainer")
        print("-="*30)
        lista = ['1- Acessar Avaliações dos alunos', '2- Visualizar Progresso dos alunos', '3- Visualizar presenças',
                 '4- Atribuir treinos personalizados', '5- Anotações sobre os alunos', '6- Redefinir senha', '7- Sair']
        print("Opções")
        for elemento in lista:
            print(elemento)

        print("-=" * 30)

    def acessar_avaliacoes(self):
        # se o arquivo de evaliações existe, vou abrir ele
        if os.path.exists(self.avaliacoes):
            tabela = pd.read_csv(self.avaliacoes)

        # se nao existe vou retornar isso
        else:
            print("Arquivo de avaliações nao existente!")
            return

        # verificando se o df esta vazio
        if tabela.empty:
            print("Nenhuma avaliação solicitada ainda!")
            return

        # se nao estiver
        print("Avaliações disponiveis: ")
        print(tabela)

        # pedindo o nome do aluno
        nome_aluno = input(
            "Digite o nome do aluno que deseja aceitar a avaliação (Se nao quiser aceitar nenhum, digite Nenhum): ").strip().title()

        # verificando se o aluno nao esta no df
        if nome_aluno not in tabela['Nome'].values:
            print("Aluno não encontrado!")
            return

        # se ele estiver, vou filtrar os dados da avaliação
        avaliacao = tabela[tabela['Nome'] == nome_aluno].iloc[0]

        # tambem vou filtrar os dias e horarios disponiveis
        dias_disponiveis = avaliacao['Disponibilidade'].split(',')
        horarios_disponiveis = avaliacao['Horário'].split(',')

        # printando as disponibilidades novamente
        print(f"Dias disponíveis do {nome_aluno}: ", dias_disponiveis)
        print(f"Horários disponíveis do {nome_aluno}: ", horarios_disponiveis)

        # filtrando o dia escolhido
        dia_escolhido = input(
            "Digite o dia que deseja marcar a avaliação (digite da mesma maneira que o aluno digitou): ").strip()

        # verificando se o dia existe no df
        if dia_escolhido not in dias_disponiveis:
            print("O dia que você digitou nao confere com a disponibilidade do aluno!")
            return

        # se existe, vou pedir o horario da mesma maneira
        horario_escolhido = input(
            "Digite o horario que deseja marcar a avaliação (digite da mesma maneira que o aluno digitou): ").strip()

        # verificando se o horario existe
        if horario_escolhido not in horarios_disponiveis:
            print(
                f"O horário que você digitou nao confere com a disponibilidade do aluno!")

        # se existe, vou salvar as info
        nome_personal = input(
            "Digite o seu nome para confirmar a avaliação: ").strip()

        status = f'Avaliação marcada para {dia_escolhido} ás {horario_escolhido} com o personal {nome_personal}'
        tabela.loc[tabela['Nome'] == nome_aluno, 'Status'] = status

        tabela.to_csv(self.avaliacoes, index=False)

        print(
            f"Avaliação com o {nome_aluno} marcada para {dia_escolhido} ás {horario_escolhido} com o personal {nome_personal}")

    def Visualizar_progresso_alunos(self):
        # primeiro vou verificar se o dataframe nao existe
        if not os.path.exists(self.progresso):
            print(
                "Arquivo de progressos não encontrado, impossivel disponibilizar as informações! ")
            sleep(0.5)

        # abrindo o arquivo de progressos em forma de tabela
        tabela = pd.read_csv(self.progresso)
        # filtrando o nome do aluno
        nome_aluno = input(
            "Digite o nome do aluno que você deseja filtrar: ").strip().title()
        informacoes_aluno = tabela[tabela['Nome'] == nome_aluno]

        # verificando se as informações não estão vazias
        if informacoes_aluno.empty:
            print(
                f"O aluno {nome_aluno} ainda não cadastrou nenhuma informação de progresso!")
            return

        print("A seguir será exibido o historico de progresso do aluno, contendo as principais informações...")
        print(informacoes_aluno)
        print()

        # mostrando os gráficos
        opcao = input(
            "Quer visualizar os gráficos? digite S para sim e N para não: ").strip().upper()[0]

        if opcao != 'S':
            return

        else:
            plt.figure(figsize=(10, 7))
            tabela.plot(kind='bar', x='Data', y='Peso', color='skyblue')
            plt.title(f"Evolução do Aluno {nome_aluno}")
            plt.xlabel("Data")
            plt.ylabel("Peso (Kg)")
            plt.grid()
            plt.tight_layout()
            plt.show()
            return

    def Visualizar_presencas(self):
        # verificando se nao existe o arquivo das presenças
        if not os.path.exists(self.presencas):
            print("Arquivo de frequências não foi encontrado! ")
            return

        # se existe, vou pedir o nome do aluno para filtrar
        tabela = pd.read_csv(self.presencas)
        nome_aluno = input(
            "Digite o nome do aluno que você deseja verificar as presenças: ").strip().title()
        info_aluno = tabela[tabela['Nome'] ==
                            nome_aluno].iloc[0]
        # fillna substitui o vazio por ausente
        info_aluno = info_aluno.fillna('Ausente')
        info_aluno = info_aluno.copy()
        print(f"Presenças de {nome_aluno}")
        print(info_aluno)

    def Atribuir_treinos_personalizados(self):
        # verificando se o arquivo dos alunos existe
        if not os.path.exists(self.arquivo):
            print("Arquivo de banco de dados não encontrado! ")
            return

        # se existe
        tabela = pd.read_csv(self.arquivo)
        nome_personal = input("Personal, digite o seu nome: ").strip().title()
        if nome_personal not in tabela["Nome"].values:
            print("Não encontramos você no banco de dados")
            return

        nome_aluno = input(
            "Digite o nome do aluno que você deseja atribuir um treino: ").strip().title()

        if nome_aluno not in tabela['Nome'].values:
            print("Aluno não encontrado!")
            return

        # verificando se o arquivo de treino existe
        if not os.path.exists(self.treinos):
            print("Banco de dados dos treinos não foi encontrado! ")
            return

        print("\nTreinos disponiveis: \n")

        # exibindo os treinos
        with open(self.treinos, 'r', encoding='UTF-8') as file:
            treinos = file.read().split("# ")

        # vou agora fazer um for para percorrer a lista de treinos
        # basicamente o enumerate vai pegar a partir da segunda linha ignorando a primeira vazia e o enumerate começará em 1
        for i, treino in enumerate(treinos[1:], start=1):
            # aqui vou pegar somente o primeiro elemento separado por \n, ou seja somente o nome do treino
            print(f"{i}. {treino.split('\n')[0]}")

        # agora vou pedir um treino
        try:
            escolha = int(
                input(f"Digite o numero do treino escolhido para o {nome_aluno}: "))
            # verificando se a escolha nao ultrapassa o limite dos treinos
            if escolha < 1 or escolha > len(treinos) - 1:
                print("Erro: Escolha inválida")
                return
            escolha = treinos[escolha].strip()

        except ValueError:
            print("Erro: Digite um número inteiro válido! ")
            return

        # agora vou criar o df dos treinos personalizados
        treino_info = {
            "Nome": nome_aluno,
            "Treino": escolha.split('\n')[0],  # pegando somente o titulo
            "Data de atribuição": datetime.today().strftime('%d/%m/%Y'),
            "Atribuido por": nome_personal
        }

        if os.path.exists(self.treinos_personalizados):
            tabela = pd.read_csv(self.treinos_personalizados)
            tabela = tabela._append(treino_info, ignore_index=True)
        else:
            tabela = pd.DataFrame([treino_info])

        tabela.to_csv(self.treinos_personalizados, index=False)
        print(
            f"\nTreino: '{treino_info['Treino']}' atribuido com sucesso para {nome_aluno}")

    def tratando(self, n):
        while True:
            try:
                n = int(n)
                if n in [1, 2, 3, 4, 5, 6, 7]:
                    return n
                else:
                    n = input("Opção Inválida, digite novamente de 1 a 6: ")
            except (ValueError, TypeError):
                n = input("Opção inválida digite novamente: ")

    def Anotacoes_sobre_alunos(self):
        nome_personal = input("Personal, digite seu nome: ").strip().title()
        arquivo = pd.read_csv(self.arquivo)
        if nome_personal not in arquivo.values:
            print(f"{nome_personal}, não encontramos o seu nome cadastrado! ")
            sleep(1)
            return

        # verificando se o arquivo de duvidas existe
        if not os.path.exists(self.duvidas):
            print("Arquivo das dúvidas não existe!")
            return

        # se existe vou filtrar as duvidas que ainda estão pendentes
        tabela = pd.read_csv(self.duvidas)
        duvidas_pendentes = tabela[tabela['Status'] == 'Pendente']

        # verificando se ha duvidas pendentes
        if duvidas_pendentes.empty:
            print("Não há dúvidas pendentes...")
            return

        # se nao houver, vou exibir as duvidas
        print("\nDúvidas pendentes: ")
        print(duvidas_pendentes[['Nome', 'Data', 'Dúvida']])

        # perguntando o aluno que o personal deseja responder
        opcao = input(
            "Deseja responder alguma dúvida? (S/N): ").strip().upper()[0]
        nome_aluno = input(
            "Digite o nome do aluno que você deseja responder (Se quiser cancelar a operação digite Cancelar): ").strip().title()

        if opcao == 'N':
            print("Saindo...")
            sleep(1)
            return

        if nome_aluno == 'Cancelar':
            print("Saindo...")
            sleep(1)
            return

        # verificando se nao encontra a duvida do aluno
        if nome_aluno not in duvidas_pendentes["Nome"].values:
            print("Aluno não encontrado ou não há dúvida pendente...")
            sleep(1)
            return

        # obtendo a duvida
        duvida = duvidas_pendentes[duvidas_pendentes['Nome']
                                   == nome_aluno]
        print(f"Dúvida do aluno {nome_aluno}: {duvida['Dúvida']}")

        # Obtendo a resposta
        resposta = input(
            f"Digite a resposta para o dúvida do aluno {nome_aluno}: ").strip()

        sleep(1)
        # verificando se é nao vazio
        if not resposta:
            print("Não é permitido dúvidas vazias!")
            sleep(1)
            return

        # se for nao vazia vou atualizar o df
        tabela.loc[tabela['Nome'] == nome_aluno, 'Resposta'] = resposta
        tabela.loc[tabela['Nome'] == nome_aluno,
                   'Status'] = f'Respondido pelo personal: {nome_personal}'

        # salvando as mudanças
        tabela.to_csv(self.duvidas, index=False)

        print(f"\nResposta enviada para {nome_aluno}, obrigado!")

    def redefinir_senha(self):
        # verificando se o arquivo principal nao existe
        if not os.path.exists(self.arquivo):
            print("Arquivo de banco de dados não encontrado! ")
            return

        # se existir vou  ler
        tabela = pd.read_csv(self.arquivo)

        email = input("Digite seu email: ").strip()

        # verifica se o aluno exite no df
        personal = tabela[(tabela["Email"] == email) &
                          (tabela["Tipo"] == "Personal")]

        # se nao existe
        if personal.empty:
            print("Nome não encontrado! ")
            return

        senha_atual = input("Digite a sua senha atual: ").strip()
        senha_nova = input("Digite a nova senha: ").strip()

        # se a senha atual confere
        if personal.iloc[0]['Senha'] == senha_atual:
            tabela.loc[tabela['Email'] == email, 'Senha'] = senha_nova
            tabela.to_csv(self.arquivo, index=False)
            print("Senha redefinida com sucesso! ")

        # senao
        else:
            print("Senha atual não confere! ")
            sleep(1)
            return


if __name__ == "__main__":
    while True:
        per = Personal()
        per.cabecalho()
        opcao = per.tratando(
            input("Digite o número da sua opção: ").strip()[0])
        if opcao == 1:
            per.acessar_avaliacoes()
        elif opcao == 2:
            per.Visualizar_progresso_alunos()
        elif opcao == 3:
            per.Visualizar_presencas()
        elif opcao == 4:
            per.Atribuir_treinos_personalizados()
        elif opcao == 5:
            per.Anotacoes_sobre_alunos()
        elif opcao == 6:
            per.redefinir_senha()
        else:
            print("Saindo do sistema...")
            sleep(1)
            print("Obrigado!")
            break
