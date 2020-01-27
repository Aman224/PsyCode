from django import forms
from .models import Content

class InputForm(forms.ModelForm):

    class Meta:
        model = Content
        fields = ('inputData', )