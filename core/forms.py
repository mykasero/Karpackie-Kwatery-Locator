from django import forms
from .models import AppartmentsModel, AppartmentsPhotosModel
from django.forms.widgets import ClearableFileInput

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class AppartmentForm(forms.ModelForm):
    images = MultipleFileField()
    class Meta:
        model = AppartmentsModel
        fields = [
            "name","address","city",
            "description", "extra_desc",      
            ]
        labels = {
            'name':'Nazwa Lokalu',
            'address':'Adres lokalu',
            'city':'Miasto',
            'description':'Opis lokalu',
            'extra_desc':'Cechy/Atuty',
            }
        help_texts = {
            'extra_desc': 'Podaj cechy oddzielając je symbolem ";"',
        }
        
        
    # def clean(self):
    #     cleaned_data = super().clean()
    #     if 'images' not in self.files:
    #         self.add_error('images', 'No file was submitted. Check the encoding type on the form.')
    #     return cleaned_data