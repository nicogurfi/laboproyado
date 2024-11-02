# experimento/models.py

from django.db import models

class ExperimentSession(models.Model):
    participant_id = models.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

class Block(models.Model):
    session = models.ForeignKey(ExperimentSession, on_delete=models.CASCADE)
    block_number = models.IntegerField()
    performance = models.FloatField(null=True, blank=True)

class Trial(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    trial_number = models.IntegerField()
    stimulus = models.CharField(max_length=10)
    response = models.CharField(max_length=10, null=True, blank=True)
    correct = models.BooleanField(null=True, blank=True)
    reaction_time = models.FloatField(null=True, blank=True)


class ExperimentResponse(models.Model):
    trial_id = models.IntegerField()  # El ID del trial, según cómo lo manejes
    response = models.CharField(max_length=10)  # La respuesta del usuario, por ejemplo "<" o ">"
    reaction_time = models.FloatField()  # Tiempo de reacción del usuario en segundos
    timestamp = models.DateTimeField(auto_now_add=True)  # Marca de tiempo de cuando se guardó la respuesta

    def __str__(self):
        return f'Trial {self.trial_id} - Response: {self.response}'