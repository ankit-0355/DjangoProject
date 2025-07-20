from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import GreenIdea

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

class GreenIdeaForm(forms.ModelForm):
    class Meta:
        model = GreenIdea
        fields = ['title', 'description', 'category', 'image']