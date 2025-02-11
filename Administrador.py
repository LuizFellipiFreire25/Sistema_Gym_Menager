import pandas as pd
import os
from time import sleep
from datetime import date
import matplotlib.pyplot as plt


class Administrador:
    def __init__(self):
        self.arquivo = 'Visualizar_alunos.csv'
        self.planos_arquivo = 'planos.txt'
        self.treinos_arquivo = 'treinos.txt'
        self.presencas_arquivo = 'presencas.csv'
        # chamando o método que vai tratar a tabela
        self.Carregar_Dados()

    # método que vai abrir a tabela
    def Carregar_Dados(self):
        # Carrega os dados do arquivo CSV ou cria uma nova tabela se o arquivo não existir
        if os.path.exists(self.arquivo):
            self.tabela = pd.read_csv(self.arquivo)
        else:
            # mais pra frente gerar id aleatoriamente
            colunas = ['ID', 'Nome', 'Email', 'Tipo de plano', 'Tipo']
            self.tabela = pd.DataFrame(columns=colunas)

    # método que vai salvar os dados sempre que preciso no arquivo
    def salvar(self):
        """
        aqui ele somente salva o arquivo usando o tabela.to_csv e o index = False é para nao salvar o índice, somente o conteúdo

        """
        self.tabela.to_csv(self.arquivo, index=False)
        print("SALVAMENTO CONCLUÍDO...")

    # este método vai exibir as opções presentes no programa
    def Cabeçalho(self):
        print('-=' * 30)
        print("                 Sistema do Administrador ")
        print('-=' * 30)
        print("Opções: ")
        lista = ['1. Cadastrar Usuário', '2. Ver Usuário', '3. Cadastrar Plano',
                 '4. Registrar Pagamento', '5. Registrar Presença', '6. Gerar Relatório Frequência', '7. Alterar Informações de Alunos', '8. Sair']
        for elemento in lista:
            print(elemento)
        print('-=' * 30)

    # este é o método responsável por cadastrar os usuários no banco de dados
    def Cadastrar_Usuário(self):
        # pedindo o email do usuario para verificá-lo no banco de dados
        email = input("Digite o email: ")
        # verificando se o usuario ja esta cadastrado
        if email in self.tabela['Email'].values:
            return 'já cadastrado!'

        # se nao estiver cadastrado, deve cadastrar
        else:
            id = input("Digite o ID: ")
            nome = input("Digite o Nome: ")
            senha = input("Digite uma Senha para o primeiro acesso: ")
            plano = input(
                "Digite o tipo de plano, (se for Administrador digite Nenhum): ")
            tipo = input(
                "O usuário será Administrador ou Aluno? (A para Admin, L para Aluno) ").strip().upper()[0]
            tipo = "Administrador" if tipo == "A" else "Aluno"
            novo = {'Nome': nome, 'ID': id,
                    'Tipo de Plano': plano, 'Email': email, 'Tipo': tipo}
            self.tabela = self.tabela._append(novo, ignore_index=True)
            self.tabela.loc[self.tabela['Nome'] == nome,
                            'Tipo de Plano'] = plano if tipo == 'L' else "Nenhum"
            self.salvar()

    # método responsável por promover a visualização de um aluno
    def Ver_Usuário(self):
        # solicitando o id do aluno para verificação
        nome = (input("Digite o nome do Aluno que você deseja filtrar: "))
        # verificando se existe o id
        # .astype(str) serve para passar todos os argumentos para string, para nao dar erro na comparação
        # se toda comparação for feita considerando o Id ser uma string então nao tem erro
        if nome in self.tabela['Nome'].values:
            print("Aluno encontrado...")
            sleep(1)
            aluno = self.tabela.loc[self.tabela['Nome'] == nome]
            print(aluno)
            sleep(1)
            print()
        # avisando se nao encontrar o aluno
        else:
            print("Aluno não encontrado!")

    # função que mostra os planos existentes e cadastra planos de treino em um arquivo
    def Cadastrar_Plano(self):
        # abrindo o arquivo com os planos já criados
        with open(self.planos_arquivo, 'r') as arquivo:
            print("Os tipos de planos criados são...")
            print("")
            print(arquivo.read())

        # perguntado se o usuário deseja criar mais  plano
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
            with open(self.planos_arquivo, 'a', encoding='utf-8') as arquivo:
                arquivo.write(novo_plano)
                print("Novo plano salvo com sucesso! ")

        else:
            return 'Saindo...'

    # método que registra o pagamento ou nao de cada aluno
    def Registrar_Pagamento(self):
        # filtrando o aluno pelo email
        email = input(
            "Digite o Email do aluno que você quer registrar o pagamento: ")
        # se o aluno tiver no banco de dados ele registra o pagamento
        if email in self.tabela['Email'].values:
            print("Aluno encontrado! ")
            # adicionando a coluna pago
            self.tabela.loc[self.tabela['Email']
                            == email, 'Pagamento'] = 'Pago'
            # garantindo que os alunos que nao pagaram nao vao estar como pago
            self.tabela['Pagamento'] = self.tabela['Pagamento'].fillna(
                "Não Pago")
            # salvando
            self.salvar()
        else:
            print("Aluno não encontrado!")

    # método que gera relatorio da frequencia dos alunos
    def Registrar_Presença(self):
        # verificando se exite o aquivo, se existir devo abrir ele
        if os.path.exists(self.presencas_arquivo):
            presencas_df = pd.read_csv(self.presencas_arquivo)
        # se nao existir vou criar ele
        else:
            colunas = ['ID', 'Nome', 'Segunda', 'Terça',
                       'Quarta', 'Quinta', 'Sexta', 'Sábado']
            presencas_df = pd.DataFrame(columns=colunas)
            presencas_df.to_csv(self.presencas_arquivo, index=False)

        email = input("Digite o email para registrar presença: ")
        if email not in self.tabela['Email'].values:
            print("Aluno não encontrado...")
            sleep(0.5)
            return

        # filtrando a linha onde o email é igual ao email fornecido
        aluno = self.tabela.loc[self.tabela['Email'] == email]
        # como aluno é um Df contendo a linha onde o email é igual ao email fornecido vou usar o iloc para filtrar o nome e id
        nome_aluno = aluno.iloc[0]['Nome']
        id_aluno = aluno.iloc[0]['ID']
        # Estabelecendo os dias da semana
        dia_semana = date.today().strftime('%A')
        # dicionario contendo os dias traduzidos
        dias_traduzidos = {
            'Monday': 'Segunda', 'Tuesday': 'Terça', 'Wednesday': 'Quarta',
            'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado'
        }

        if dia_semana not in dias_traduzidos:
            return 'Hoje nao é dia de treino, pois é domingo'
        # acessando o dicionario na chave do dia atual
        dia_atual = dias_traduzidos[dia_semana]
        # adicionando "Presente" para o aluno no dia atual
        if id_aluno in presencas_df['ID'].values:
            presencas_df.loc[presencas_df['ID'] ==
                             id_aluno, dia_atual] = "Presente"
        # caso seja a vez do aluno na lista de presenças
        else:
            novo = {"ID": id_aluno, 'Nome': nome_aluno, dia_atual: "Presente"}
            presencas_df = presencas_df._append(novo, ignore_index=True)

        presencas_df.to_csv(self.presencas_arquivo, index=False)
        print("Presença registrada!")

    def Gerar_Relatório_Frequência(self):
        # verificando se existe o arquivo das presenças
        if not os.path.exists(self.presencas_arquivo):
            return f"Arquivo de presença nao encontrado"

        # carregando os dados das presenças
        presencas_df = pd.read_csv(self.presencas_arquivo)

        # contabilizando as presenças por aluno
        # iloc[:, 2:] seleciona todas as linhas e apartir da terceira coluna, pois as duas primeiras nao sao as presenças
        # apply(lambda row: ..., axis=1): Aplica uma função a cada linha do DataFrame (o parâmetro axis=1 indica que a operação é feita por linha).
        # lambda row: row.eq('Presente').sum() verifica os valores igual a presente retronando uma serie de True ou False, axis = 1 aplica linha por linha
        presencas_df['Total de Presenças'] = presencas_df.iloc[:, 2:].apply(
            lambda row: row.eq('Presente').sum(), axis=1)

        # salvando o relatório
        relatorio = 'relatorio_frequencia.csv'
        presencas_df.to_csv(relatorio, index=False)
        print("Relatório de frequência gerado com sucesso!")

        # verificando se o usuário deseja ver os gráficos
        resp = input(
            "Você deseja visualizar os gráficos de análise? (Digite S para sim e N para não): ").strip().upper()[0]
        if resp in "N":
            print("Você optou por nao visualizar os gráficos")
            sleep(0.5)
            print("Obrigado!")

        # montando os gráficos
        grafico = presencas_df.plot(x='Nome', y='Total de Presenças', kind='bar', color='darkblue', figsize=(
            10, 5), xlabel='Alunos', ylabel='Presenças', title='Gráfico de Presenças')
        plt.show()

    # método responsável por alterar as informações de alunos
    def Alterar_Informações_Alunos(self):
        # filtrando o aluno pelo nome
        aluno = input(
            "Digite o nome do aluno ou administrador que você deseja alterar informções: ")
        # verificando se o aluno existe no banco de dados
        if aluno in self.tabela['Nome'].values:
            print("Aluno encontrado!")
            print("Digite as novas informações que serão solicitadas abaixo ou pressione enter para manter as atuais!")
            # solicitando as novas informações
            id = input("Digite o novo Id: ").strip()
            email = input("Digite o novo Email: ").strip()
            tipo_plano = input(
                "Digite o novo Tipo de Plano, (se for adiministrador digite Nenhum): ").strip()
            pagamento = input(
                "Digite [1] para adicionar 'Pago' ou [2] para adicionar 'Não Pago' ao aluno: ").strip()
            # só vai considerar os campos se for não vazio
            if id:
                self.tabela.loc[self.tabela['Nome'] == aluno, 'ID'] = id
            if email:
                self.tabela.loc[self.tabela['Nome'] == aluno, 'Email'] = email
            if tipo_plano:
                self.tabela.loc[self.tabela['Nome'] ==
                                aluno, 'Tipo de Plano'] = tipo_plano
            if pagamento:
                self.tabela.loc[self.tabela['Nome'] == aluno,
                                'Pagamento'] = 'Pago' if pagamento in '1' else 'Não Pago'
            # salvando as info
            self.salvar()
        else:
            print("Aluno não encontrado")

    def tratando(self, n):
        while True:
            try:
                n = int(n)
                if n in [1, 2, 3, 4, 5, 6, 7, 8]:
                    return n
                else:
                    n = input("Opção Inválida, digite novamente de 1 a 8: ")
            except (ValueError, TypeError):
                n = input("Opção inválida digite novamente: ")


# aqui em diante garante que o codigo seja executado somente se eu executar Administrador.py (if __name__ == "__main__")
# para eu chamar as funções da classe Administrador eu tenho que criar o cabeçalho novamente no módulo que eu for chamar, ficará exatamente igual tirando a parte comentada acima
if __name__ == "__main__":
    admin = Administrador()
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
            print("Saindo do sistema...")
            sleep(1)
            print("Obrigado!")
            break

# tenho que separar a parte da senha e pensar em algo para o pagamento
