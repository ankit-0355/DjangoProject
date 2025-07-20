from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class GreenIdea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='idea_images/', blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title