from django import forms
from .models import Story


class StoryForms(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['topic', 'picture', 'content']
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ContactForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "Podaj e-mail", 'class': 'form-control'})
    )
    subject = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Wpisz temat", 'class': 'form-control'}))
    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Twoja wiadomość", 'class': 'form-control', 'style': 'height: 170px;'})
    )

