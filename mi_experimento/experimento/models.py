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
    id = models.BigAutoField(primary_key=True)
    block = models.ForeignKey('experimento.Block', on_delete=models.CASCADE)
    trial_id = models.IntegerField()  # Use trial_id if that’s your requirement
    stimulus = models.CharField(max_length=10)
    response = models.CharField(max_length=10, null=True, blank=True)
    correct = models.BooleanField(null=True, blank=True)
    reaction_time = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)