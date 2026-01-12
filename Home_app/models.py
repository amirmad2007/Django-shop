from django.db import models

# Create your models here.
class Message(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=50)
    text = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.subject}"