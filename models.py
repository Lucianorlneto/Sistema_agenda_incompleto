from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=255, blank=False)
    data_nascimento = models.DateField(blank=False, null=True)
    def __str__(self):
        return str(self.id) + ' - ' + self.user.first_name + ' ' + self.user.last_name


class Papel(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Usuario_papel(models.Model):
    usuario_id = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    papel_id = models.ForeignKey(Papel, on_delete=models.CASCADE, default="")
    def __str__(self):
        return self.usuario_id.email + " - " + self.papel_id.nome

class Ficha(models.Model):
    paciente_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="paciente_ficha", default="")
    clinico_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clinico_ficha", default="")
    observacao = models.TextField(default="")
    data_criacao = models.DateField(blank=False, null=True)
    def __str__(self):
        return "Clinico: " + self.clinico_id.first_name + " " + self.clinico_id.last_name + " - Paciente: " +\
               self.paciente_id.first_name + " " + self.paciente_id.last_name + " - Data: "\
               + str(self.data_criacao)

# class Ficha_observacao(models.Model):
#     ficha_id = models.IntegerField()
#     observacao = models.TextField()


class Horario(models.Model):
    paciente_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="paciente_horario", default="")
    #clinico_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clinico_horario")
    dataHora = models.DateTimeField(blank=False, null=True)
    observacao = models.TextField(blank=True)

    def __str__(self):
        return "Paciente: " + self.paciente_id.first_name + " " + self.paciente_id.last_name + " - DataHora: "\
               + str(self.dataHora)

