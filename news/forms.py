from .models import *
from django.forms import *


class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ['title', 'text', 'picture', 'tags']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'text': Textarea(attrs={'class': 'form-control',
                                    'required': 'true', 'rows': '3'}),
            'tags': SelectMultiple(attrs={'class': 'form-select form-select-lg',
                                          'required': 'true', 'multiple': 'true'}),
            'picture': FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}),
        }
