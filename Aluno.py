import pandas as pd
from time import sleep
import os
from datetime import datetime
import matplotlib.pyplot as plt


class Aluno:
    def __init__(self):
        # self.id_aluno = id_aluno
        # self.nome = nome
        self.dados_pessoais = "dados_alunos.csv"
        self.pagamento = False
        self.faturas = "Faturas.csv"
        self.arquivo_treinos = "treinos.txt"
        self.progresso = "pregresso.csv"
        self.arquivo_avaliacoes = "Avaliacoes.csv"
        self.arquivo = 'Visualizar_alunos.csv'
        self.treinos_personalizados = "treinos_personalizados.csv"
        self.treinos = "treinos.txt"
        self.duvidas_arquivos = 'duvidas_alunos.csv'

    def cabecalho(self):
        """método que exibe as opções do cabeçalho para os alunos"""
        print("-="*30)
        print("              Sistema do aluno, Seja bem vindo!")
        print("-="*30)
        print("Opções: ")
        lista = ['1- Treinos', '2- Treinos Extra', '3- Avaliações', '4- Ver Status de avaliação',
                 '5- Meu progresso', '6- Faturas', '7- Arquivos', '8- Redefinir senha', '9- Sair']
        for opções in lista:
            print(opções)
        print("-="*30)

    def Treinos(self):
        '''método que mostra para o aluno o treino que foi inferido para ele'''
        # verificando se existe os arquivos
        if not os.path.exists(self.arquivo):
            print("Arquivo principal não encontrado! ")
            return

        if not os.path.exists(self.treinos_personalizados):
            print("Arquivos de treinos personalizados não encontrado! ")
            return

        # vendo se se o aluno existe no arquivo de treinos personalizados
        nome_aluno = input("Digite seu nome: ").strip().title()
        tabela = pd.read_csv(self.treinos_personalizados)

        if nome_aluno in tabela['Nome'].values:
            aluno_infos = tabela[tabela['Nome'] == nome_aluno].iloc[-1]
            print(f"\nOs treinos Atribuídos para {nome_aluno} são: \n")
            sleep(0.5)
            treino_nome = aluno_infos['Treino']
            print()
            with open(self.treinos, 'r', encoding='UTF-8') as file:
                treinos = file.read().split("# ")

            for treino in treinos:
                if treino_nome in treino:
                    print(treino)
                    return

        else:
            print("Aluno não encontrado!")
            return

    def Treinos_extra(self):
        """método que o aluno visualiza todos os treinos do banco de dados"""
        print("Os treinos cadastrados no banco de dados são: ")
        sleep(1)
        with open(self.arquivo_treinos, 'r', encoding='UTF-8') as file:
            treinos = file.read()
            print(treinos)

    def Avaliacao(self):
        try:
            tabela = pd.read_csv("Visualizar_alunos.csv")
            nome = input("Digite seu nome completo: ").strip().title()

            if tabela[(tabela["Nome"] == nome) & (tabela["Tipo"] == 'Aluno')].empty:
                return "Erro aluno nao encontrado!"

            else:
                dias_disponiveis = input(
                    "Informe o dia disponível na semana ou datas específicas, separando-os por vírgula (Ex: Segunda, Terça ou 12/01/25): ")
                horarios_disponiveis = input(
                    "Informe os horários disponíveis, (ex: 18:00): ")

                datas = {
                    "Nome": [nome],
                    "Disponibilidade": [dias_disponiveis],
                    "Horário": [horarios_disponiveis]
                }

                df_Avaliacao = pd.DataFrame(datas)

                if os.path.exists(self.arquivo_avaliacoes):
                    df_Avaliacao.to_csv(
                        self.arquivo_avaliacoes, mode='a', header=False, index=False)
                    return "Avaliação agendada com sucesso!"

                else:
                    df_Avaliacao.to_csv(
                        self.arquivo_avaliacoes, mode='w', header=True, index=False)
                    return "Avaliação agendada com sucesso!"

        except FileNotFoundError:
            print('Pasta de dados não encontrada')

        except Exception as e:
            print(f"Erro: {e}")

    def Ver_status_avaliacao(self):
        # verificando se o df de avaliação existe
        if not os.path.exists(self.arquivo_avaliacoes):
            print("Não existe o arquivo de avaliações! ")
            return
        # se existe
        tabela = pd.read_csv(self.arquivo_avaliacoes)
        nome_aluno = input(
            "Digite seu nome para visualizar o Status de avaliação: ").strip().title()

        # verificando se o aluno existe no df de avaliações
        aluno_info = tabela[tabela['Nome'] == nome_aluno].iloc[0]

        if aluno_info.empty:
            print("Não encontramos seu nome nos dados de avaliações, provavelmente você ainda não marcou uma avaliação!")
            return

        if nome_aluno not in aluno_info.values:
            print("Não encontramos seu nome nos dados de avaliações, provavelmente você ainda não marcou uma avaliação!")
            return

        # se existe
        print("Vamos exibir seu status abaixo: ")
        sleep(0.5)
        if pd.isna(aluno_info["Status"]):
            print("Sua solicitação ainda não foi respondida por um personal!")
        else:
            print(aluno_info['Status'])

    def Meu_progresso(self):
        '''metodo que atualiza o progresso do aluno, gera um data frame para os dados e plota gráficos de anáilise'''
        nome = input("Digite o seu nome: ").strip().title()
        # tenteando acessar a tabela principal para ver se o aluno esta cadastrado
        try:
            tabela = pd.read_csv("Visualizar_alunos.csv")
            if tabela[(tabela['Nome'] == nome) & (tabela['Tipo'] == "Aluno")].empty:
                print("Aluno não encontrado! ")
                return

        except FileNotFoundError:
            print("Banco de dados não encontrado!")
            return
        # tentando acessar o data frame do progresso dos alunos e atribuindo o nome do aluno para uma variável
        try:
            df_progresso = pd.read_csv(self.progresso)
            aluno_progresso = df_progresso[df_progresso['Nome'] == nome]
        # se ele nao achar o arquivo, vou iniciar as duas variaveis abaixo como um data fframe
        except FileNotFoundError:
            df_progresso = pd.DataFrame()
            aluno_progresso = pd.DataFrame()
        # uniciando as variaveis que vou usar, como um dataframe
        novo_progresso = pd.DataFrame()
        progresso_atual = pd.DataFrame()
        # se o aluno da vez estiver com o progresso vazio, vou coletar seus dados, tranformar em data frame e mandar para uma variável
        if aluno_progresso.empty:
            print("Você ainda não tem os dados cadastrados no sistema! ")
            peso = float(input("Digite o peso (Kg): "))
            altura_str = input("Digite a altura (M): ")
            altura = float(altura_str.replace(',', '.'))
            imc = round(peso/(altura**2), 2)
            dados = {
                "Nome": [nome],
                "Altura": [altura],
                "Peso": [peso],
                "IMC": [imc],
                "Data": [datetime.today().strftime('%Y-%m-%d')]
            }
            progresso_atual = pd.DataFrame(dados)
        # se o aluno não estiver com o progresso vazio eu pego o novo peso, filtro a nova altura e faço o mesmo processo anterior
        else:
            print("Você ja tem alguns dados cadastrados! ")
            peso_novo = input("Digite o seu peso atual (Kg): ")
            altura_novo = aluno_progresso['Altura'].values[0]
            # Converte os valores para float para garantir que sejam numéricos
            peso_novo = float(peso_novo.replace(',', '.')) if isinstance(
                peso_novo, str) else float(peso_novo)
            # Garante que altura_novo seja uma string antes de substituir e converter para float
            altura_novo = float(str(altura_novo).replace(',', '.'))
            imc_novo = round(peso_novo / (altura_novo ** 2), 2)

            novos_dados = {
                "Nome": [nome],
                "Altura": [altura_novo],
                "Peso": [peso_novo],
                "IMC": [imc_novo],
                "Data": [datetime.today().strftime('%Y-%m-%d')]
            }
            novo_progresso = pd.DataFrame(novos_dados)

        # concat nos permite agrupar mais de um dataframe no mesmo arquivo
        df_progresso = pd.concat(
            [df_progresso, progresso_atual, novo_progresso], ignore_index=True)
        # salvando o dataframe no arquivo principal do progresso
        df_progresso.to_csv(self.progresso, index=False)

        # plotando os gráficos
        opcao = input(
            "Quer visualizar os gráficos? digite S para sim e N para não: ").strip().upper()[0]
        if opcao == 'S':
            plt.figure(figsize=(10, 6))
            df_progresso[df_progresso['Nome'] == nome].plot(kind='bar',
                                                            x='Data', y='Peso', linestyle='-')
            plt.title("Gráfico de Análise de evolução do peso (Kg)")
            plt.xlabel("Data")
            plt.ylabel("Peso (Kg)")
            plt.grid(color='darkblue', alpha=0.7)
            plt.tight_layout()
            plt.show()
            return

    def Faturas(self):
        # verificando se existe o arquivo da fatura
        if os.path.exists(self.faturas):
            tabela = pd.read_csv(self.faturas)

        else:
            return "Não existe o arquivo das faturas"

        email = input("Digite seu email: ").strip()
        sleep(0.5)
        print("Gerando suas faturas...")
        sleep(1)

        # filtrando o mes atual
        mes_atual = datetime.today().strftime('%m/%Y')

        # filtrando a linha correspondente ao email e mes atuais
        fatura = tabela[(tabela['Email'] == email) &
                        (tabela['Mês'] == mes_atual)]

        # verificando se tem fatura registrada no mes atual para o aluno
        if fatura.empty:
            print(
                f"Olá, não encontramos pagamento registrado para o mês: {mes_atual}")
            print("Por favor, verifique sua situação com a Adiministração!")
            return

        else:
            nome = fatura.iloc[0]['Nome']
            status = fatura.iloc[0]['Status']
            print(
                f"Olá, {nome}. Sua fatura referente ao mês {mes_atual} esta com o Status: {status}")

    def arquivos(self):
        nome = input("Digite seu nome completo: ").strip().title()

        # verificando se existe o arquivo de duvidas
        if os.path.exists(self.duvidas_arquivos):
            tabela = pd.read_csv(self.duvidas_arquivos)
            # verificando se tem duvidas pendentes
            pendente = tabela[(tabela["Nome"] == nome) &
                              (tabela["Status"] == 'Pendente')]
            # verificando se o aluno nao tem nenhuma duvida pendente
            if not pendente.empty:
                print(
                    "Você ja tem uma duvida pendente, aguarde o personal responder sua duvida antes de enviar outra...")
                return
        else:
            tabela = pd.DataFrame(
                columns=['Nome', 'Data', 'Dúvida', 'Anexo', 'Resposta', 'Status'])

        # coletando uma dúvida e verificando se é não vazia
        duvida = input("Digite sua dúvida: ").strip()

        if not duvida:
            print("Não é permitido dúvidas vazias!")
            return

        # criando a nova duvida no df
        nova = {
            "Nome": nome,
            "Data": datetime.today().strftime("%d/%m/%Y"),
            "Dúvida": duvida,
            "Resposta": 'Agurdando Resposta do Personal',
            "Status": 'Pendente'
        }

        # salvando tudo
        tabela = tabela._append(nova, ignore_index=True)
        tabela.to_csv(self.duvidas_arquivos, index=False)

        print("Sua dúvida foi enviada para o personal")

    def redefinir_senha(self):
        # verificando se o arquivo principal nao existe
        if not os.path.exists(self.arquivo):
            print("Arquivo de banco de dados não encontrado! ")
            return

        # se existir vou  ler
        tabela = pd.read_csv(self.arquivo)

        email = input("Digite seu email: ").strip()

        # verifica se o aluno exite no df
        aluno = tabela[(tabela["Email"] == email) &
                       (tabela["Tipo"] == "Aluno")]

        # se nao existe
        if aluno.empty:
            print("Nome não encontrado! ")
            return

        senha_atual = input("Digite a sua senha atual: ").strip()
        senha_nova = input("Digite a nova senha: ").strip()

        # se a senha atual confere
        if aluno.iloc[0]['Senha'] == senha_atual:
            tabela.loc[tabela['Email'] == email, 'Senha'] = senha_nova
            tabela.to_csv(self.arquivo, index=False)
            print("Senha redefinida com sucesso! ")

        # senao
        else:
            print("Senha atual não confere! ")
            sleep(1)
            return


if __name__ == "__main__":
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
            user.Ver_status_avaliacao()
        elif opcao == 5:
            user.Meu_progresso()
        elif opcao == 6:
            user.Faturas()
        elif opcao == 7:
            user.arquivos()
        elif opcao == 8:
            user.redefinir_senha()
        else:
            print("Saindo do sistema...")
            break
