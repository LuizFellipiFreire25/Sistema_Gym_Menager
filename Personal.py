import pandas as pd
import matplotlib.pyplot as plt
from time import sleep
import os


class Personal:
    def __init__(self):
        self.avaliacoes = "Avaliacoes.csv"
        self.progresso = "pregresso.csv"
        self.presencas = "presencas.csv"
        self.treinos_personalizados = "treinos_personalizados.csv"
        self.anotacoes = "anotacoes_personal.csv"
        self.relatorio_frequencia = "relatorio_frequencia.csv"

    def cabecalho(self):
        print("-=" * 30)
        print("               Sistema do Personal Trainer")
        print("-="*30)
        lista = ['1- Acessar Avaliações dos alunos', '2- Visualizar Progresso dos alunos', '3- Visualizar presenças',
                 '4- Atribuir treinos personalizados', '5- Anotações sobre os alunos', '6- Sair']
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


Personal().Visualizar_presencas()
