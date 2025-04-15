from django import forms
from .models import AppartmentsModel, AppartmentsPhotosModel, HomepageCounters
from django.forms.widgets import ClearableFileInput
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.utils.translation import gettext as _



import environ
env = environ.Env()
environ.Env.read_env()

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
            "name","address","city", "extra_desc",      
            ]
        labels = {
            'name':'Nazwa Lokalu',
            'address':'Adres lokalu',
            'city':'Miasto',
            'extra_desc':'Cechy/Atuty',
            }
        help_texts = {
            'extra_desc': 'Podaj cechy oddzielając je symbolem ";"',
        }
        
class CountersForm(forms.ModelForm):
    class Meta:
        model = HomepageCounters
        fields = [
            "appartments_amount", "locations_amount", "clients_amount",
        ]
        labels = {
            'appartments_amount' : "Ilość lokali",
            'locations_amount' : "Ilość miejscowości",
            'clients_amount' : 'Ilość klientów',
        }
        
# Login Form
class LoginForm(forms.Form):
    login = forms.CharField(label = '', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Login'}))
    haslo = forms.CharField(label = '', widget=forms.PasswordInput(attrs={'placeholder': 'Haslo'}), max_length=40)
    
# Register form
class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        # override Djangos default label
        self.fields['password1'].label = mark_safe('<strong>Hasło</strong>')
        self.fields['password2'].label = mark_safe('<strong>Potwierdź hasło</strong>')
        # override Djangos default helptext
        self.fields['password1'].help_text = mark_safe('<ul><li>Minimum 8 znaków.</li><li>Nie może być podobne do loginu.</li><li>Nie może być całkowicie złożone z cyfr.</li></ul>')
        self.fields['password2'].help_text = ' '
    
    # Add an access_code field for register form
    access_code = forms.CharField(
        label=mark_safe("<strong>Kod Dostepu</strong>"),
        help_text=mark_safe("<ul><li>Przyznany tylko administracji</li></ul>"),
    )
    usable_password = None
    class Meta:
        model = User
        fields = ['username','password1','password2','access_code']

        labels={
            'username' : mark_safe('<strong>Nazwa użytkownika</strong>'),
            'password' : mark_safe('Hasło'),
            'password2' : mark_safe('Potwierdź hasło'),
            'access_code' : mark_safe('Kod dostępu'),
        }
        help_texts= {
            'username' : mark_safe('<ul><li>Max długość 50 znaków.</li><li>Dozwolone litery, cyfry i symbole @/./+/-/_</li></ul>'),
        }
    
    # Create validation checks
    def clean(self):
        cleaned_data = super().clean()
        
        username = cleaned_data.get('username')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        access_code = cleaned_data.get('access_code')
        
        # If passwords don't match throw error
        if password1 != password2:
            self.add_error(None,forms.ValidationError(_("Hasła nie są takie same"),
                                  code="invalid",
                                  ))
        # If any of the passwords ( or both ) are empty, throw error
        if password1 == "" or password2 == "" or (password1 == "" and password2 == ""):
            self.add_error(None,forms.ValidationError(_("Pola haseł nie mogą być puste"),
                                  code="invalid",
                                  ))
        # If password shorter than 8 chars, throw error
        if len(password1) < 8:
            self.add_error(None,forms.ValidationError(_("Hasło za krótkie, minimalna długość 8 znaków"),
                                  code="invalid",
                                  ))
        
        # If username is empty, throw error
        if username is None:
            self.add_error(None,   
                           forms.ValidationError(
                               _("Użytkownik o takiej nazwie już istnieje"),
                                code="invalid",
                                )
                           )
        # If username is longer than 50 chars, throw error
        elif len(username) > 50:
            self.add_error(None,forms.ValidationError(_("Nazwa za długa, maksymalna długość - 50 znaków"),
                                  code="invalid",
                                  ))
        
        # If access_code is wrong, throw error
        if access_code not in [env("ADMIN_REGISTER_CODE")]:
            self.add_error(None,   
                           forms.ValidationError(
                               _("Podano zły kod dostępu"),
                                code="invalid",
                                )
                           )
        # If password is only numeric, throw error
        if password1.isdigit():
            self.add_error(None,   
                           forms.ValidationError(
                               _("Hasło nie może być złożone z samych cyfr"),
                                code="invalid",
                                )
                           )
        
        return cleaned_data
    
class ContactForm(forms.Form):
    email = forms.EmailField(label = "Adres E-mail", max_length=100)
    name = forms.CharField(label = "Imię")
    phone_number = forms.CharField(label = "Numer telefonu")
    message = forms.CharField(
        label = "Wiadomość",
        widget=forms.Textarea(attrs={
            'rows' : 10,
            'cols' : 50,     
        })
    )
     
    def clean(self):
        cleaned_data = super().clean()
            
        phone_number = cleaned_data.get('phone_number')
        
        if not phone_number[1:].isnumeric():
            self.add_error(None,forms.ValidationError(_("Podano niepoprawny format numeru telefonu."),
                                    code="invalid",
                                    ))