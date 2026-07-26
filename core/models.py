from django.db import models


class Arquivo(models.Model):
    nome = models.CharField(max_length=255)
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    idade = models.IntegerField()

    def __str__(self):
        return self.nome

class Importacao(models.Model):
    arquivo = models.CharField(max_length=255)
    data = models.DateTimeField(auto_now_add=True)
    importados = models.IntegerField(default=0)
    ignorados = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.arquivo} - {self.data.strftime('%d/%m/%Y %H:%M')}"
