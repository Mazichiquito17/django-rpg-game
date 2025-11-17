from django.db import models

class Character(models.Model):
    name = models.CharField(max_length=100)
    lore = models.TextField()
    strength = models.IntegerField()
    magic = models.IntegerField()

    def __str__(self):
        return self.name
