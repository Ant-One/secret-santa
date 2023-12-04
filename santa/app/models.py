from django.db import models

class Draw(models.Model):
    draw_name = models.TextField(blank=False)
    is_drawn = models.BooleanField(default=False)

class Pairing(models.Model):
    gifter = models.ForeignKey("Participant", on_delete=models.SET_NULL, null=True, related_name="participants_1")
    giftee = models.ForeignKey("Participant", on_delete=models.SET_NULL, null=True, related_name="participants_2")
    draw = models.ForeignKey("Draw", on_delete=models.CASCADE, null=False)

class Participant(models.Model):
    in_draw = models.ForeignKey("Draw", on_delete=models.CASCADE, null=True, related_name="participants")
    name = models.TextField(blank=False)
    to_gift = models.ForeignKey("Pairing",on_delete=models.SET_NULL, null=True)