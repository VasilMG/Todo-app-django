from django.db import models

# Create your models here.

class Assignment(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description = models.TextField(blank=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Name: {self.name} --> Description: {self.description}"




