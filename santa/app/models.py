from django.db import models

class Draw(models.Model):
    name = models.TextField(blank=False)

class Pairing(models.Model):
    participant_1 = models.ForeignKey("Participant", null=True)
    participant_2 = models.ForeignKey("Participant", null=True)
    draw = models.ForeignKey("Draw", null=False)

class Participant(models.Model):
    in_draw = models.ForeignKey("Draw", on_delete=models.SET_NULL, null=True)
    name = models.TextField(blank=False)
    pairing = models.ForeignKey("Pairing", null=True)