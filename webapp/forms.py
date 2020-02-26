from django import forms
from .models import Content

LANGUAGES = (
    ('c','C'),
    ('python','Python'),
)

class InputForm(forms.ModelForm):

    inputData = forms.CharField(widget=forms.Textarea, label='')

    class Meta:
        model = Content
        fields = ('language', 'inputData')
    
    def __init__(self, *args, **kwargs):
        super(InputForm, self).__init__(*args, **kwargs)
        self.fields['inputData'].widget.attrs['placeholder'] = 'Enter Pseudocode'

