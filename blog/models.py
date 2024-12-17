# blog/models.py
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    cuerpo = models.TextField()

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class EA_Respuestas(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    APT1 = models.CharField(max_length=50, blank=True, null=True)  # Guarda el resultado del primer test
    APT2 = models.CharField(max_length=50, blank=True, null=True)  # Guarda el resultado del segundo test

    def __str__(self):
        return f"{self.usuario.username} - Test_CHAE: {self.APT1}, Test_VARK: {self.APT2}"

class Emotions_Activities(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=50, blank=True, null=True)  # Guarda el resultado del primer test
    emotion = models.CharField(max_length=50, blank=True, null=True)  # Guarda el resultado del segundo test
    APT1 = models.CharField(max_length=50, blank=True, null=True)  # Guarda el resultado del primer test
    APT2 = models.CharField(max_length=50, blank=True, null=True)  # Guarda el resultado del segundo test

    def __str__(self):
        return f"{self.usuario.username} - Test_CHAE: {self.APT1}, Test_VARK: {self.APT2}, Activity: {self.activity}, Emotion: {self.emotion}"