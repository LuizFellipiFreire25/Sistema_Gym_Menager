from django.db import models


class Usuario(models.Model):
    TIPOS_USUARIO = [
        ('ADMIN', 'Administrador'),
        ('ALUNO', 'Aluno'),
        ('PERSONAL', 'Personal Trainer'),
    ]
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    tipo = models.CharField(max_length=10, choices=TIPOS_USUARIO)

    def __str__(self):
        return f"{self.nome} ({self.tipo})"


class Plano(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


class Treino(models.Model):
    aluno = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, limit_choices_to={'tipo': 'ALUNO'})
    descricao = models.TextField()
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Treino de {self.aluno.nome} - {self.data}"


class Pagamento(models.Model):
    aluno = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, limit_choices_to={'tipo': 'ALUNO'})
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    data_pagamento = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Pagamento de {self.aluno.nome} - {self.valor} R$"


class Presenca(models.Model):
    aluno = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, limit_choices_to={'tipo': 'ALUNO'})
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Presença: {self.aluno.nome} - {self.data}"
