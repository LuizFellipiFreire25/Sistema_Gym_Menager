import pandas as pd
from time import sleep
import os
from datetime import datetime
import random


class Aluno:
    def __init__(self):
        # self.id_aluno = id_aluno
        # self.nome = nome
        self.dados_pessoais = "dados_alunos.csv"
        self.pagamento = False
        self.faturas = "faturas.csv"
        self.arquivo_treinos = "treinos.txt"
        self.progresso = "pregresso.csv"

    def cabecalho(self):
        """método que exibe as opções do cabeçalho para os alunos"""
        print("-="*30)
        print("              Sistema do aluno, Seja bem vindo!")
        print("-="*30)
        print("Opções: ")
        lista = ['1- Treinos', '2- Treinos Extra', '3- Avaliações',
                 '4- Meu progresso', '5- Faturas', '6- Arquivos', '7- Sair']
        for opções in lista:
            print(opções)
        print("-="*30)

    def Treinos(self):
        """método que atribui para o dia atual que o usuario esta logando um pacote específico de treinos
        primeiro estamos filtrando o dia da semana, depois estamos atribuindo para cada dia um tipo de treino do banco de dados, depois usamos o get para 
        "pegar" as informações do dia da semana no dicionario"""
        dia_da_semana = datetime.today().strftime("%A")

        categorias = {
            "Monday": "Hipertrofia - Treino A - Peito e Tríceps",
            "Tuesday": "Resistência - Treino Circuito 1",
            "Wednesday": "Emagrecimento - Treino HIIT 1",
            "Thursday": "Hipertrofia - Treino B - Costas e Bíceps",
            "Friday": "Resistência - Treino Circuito 2",
            "Saturday": "Hipertrofia - Treino C - Pernas",
            "Sunday": "Mobilidade - Treino de Alongamento 1"
        }
        treino_sugerido = categorias.get(dia_da_semana)
        print(f"Treino Suguerido para hoje: {dia_da_semana}:{treino_sugerido}")
        sleep(1)

        try:
            with open(self.arquivo_treinos, 'r', encoding='UTF-8') as file:
                treinos = file.read().split("# ")

            for treino in treinos:
                if treino_sugerido.split(" - ")[1] in treino:
                    print(f"{treino.strip()}")
                    return

        except FileNotFoundError:
            print("Erro! O Banco de dados nao foi encontrado...")

        except Exception as e:
            print(f"Erro: {e}")

    def Treinos_extra(self):
        """método que o aluno visualiza todos os treinos do banco de dados"""
        print("Os treinos cadastrados no banco de dados são: ")
        sleep(1)
        with open(self.arquivo_treinos, 'r', encoding='UTF-8') as file:
            treinos = file.read()
            print(treinos)

    def Avaliacao(self):
        return "função ainda em construção, sera capaz de marcar avaliação com um personal"


if __name__ == "__main__":
    user = Aluno()
    while True:
        user.cabecalho()
        opcao = int(input("Digite o numero da sua opção: "))
        if opcao == 1:
            user.Treinos()
        elif opcao == 2:
            user.Treinos_extra()
