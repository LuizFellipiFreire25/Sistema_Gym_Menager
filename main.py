
#opções de login, cadastro e sair
def cabeçalho():
    print("-=" * 30)
    print("              Sistema de Gestão Academia Gym...")
    print("-=" * 30)
    print("Opções: ")
    lista = ['1. Login', '2. Cadastrar', '3. Sair']
    for elemento in lista:
        print(elemento)

