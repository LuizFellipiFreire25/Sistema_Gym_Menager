import Administrador  # Importando o módulo do administrador
import pandas as pd


def cabeçalho():
    print("-=" * 30)
    print("              Sistema de Gestão Academia Gym...")
    print("-=" * 30)
    print("Opções: ")
    lista = ['1. Login', '2. Cadastrar', '3. Sair']
    for elemento in lista:
        print(elemento)


# Simulando um banco de usuários para login
usuarios = {
    "admin@gym.com": {"senha": "admin123", "tipo": "administrador"},
    "aluno@gym.com": {"senha": "aluno123", "tipo": "aluno"}
}


def login():
    email = input("Digite seu email: ")
    senha = input("Digite sua senha: ")

    if email in usuarios and usuarios[email]["senha"] == senha:
        tipo_usuario = usuarios[email]["tipo"]
        print(f"Login bem-sucedido como {tipo_usuario.capitalize()}!")

        if tipo_usuario == "administrador":
            admin = Administrador.Administrador()  # Instanciando a classe
            admin.menu()  # Chamando o menu do administrador

        elif tipo_usuario == "aluno":
            print("Sistema para aluno ainda em construção...")
            # Aqui você pode chamar funções do módulo aluno.py futuramente

    else:
        print("Login inválido! Verifique suas credenciais.")


while True:
    cabeçalho()
    opcao = input("Digite o número da sua escolha: ").strip()

    if opcao == "1":
        login()
    elif opcao == "2":
        print("Sistema de cadastro ainda em desenvolvimento...")
    elif opcao == "3":
        print("Saindo do sistema...")
        break
    else:
        print("Opção inválida! Digite um número entre 1 e 3.")
