from django import forms
from .models import Story


class StoryForms(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['topic', 'picture', 'content']
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
        }
