from django.db import models

class Skin(models.Model):
    name = models.CharField(max_length=100)
    sprite = models.CharField(max_length=200)  # Aquí se guarda la imagen
    lore = models.TextField()

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=100)
    lore = models.TextField()
    strength = models.IntegerField()
    magic = models.IntegerField()
    skin = models.ForeignKey(Skin, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
