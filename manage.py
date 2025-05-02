#!/usr/bin/env python
import os
import sys

print("manage.py está sendo executado...")  # Log inicial

if __name__ == "__main__":
    print("Entrando no bloco principal...")  # Log para verificar o bloco principal
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "progymmanager_api.settings")
    print("DJANGO_SETTINGS_MODULE configurado...")  # Log após configurar o módulo de configurações
    try:
        from django.core.management import execute_from_command_line
        print("Importação de execute_from_command_line bem-sucedida...")  # Log após importação
    except ImportError as exc:
        print("Erro ao importar Django:", exc)  # Log de erro
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    print("Executando o comando do Django...")  # Log antes de executar o comando
    execute_from_command_line(sys.argv)
