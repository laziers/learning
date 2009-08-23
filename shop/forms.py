from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    login = forms.CharField(label='Login', required=True)
    first_name = forms.CharField(label='Imie')
    last_name = forms.CharField(label='Nazwisko')
    email = forms.EmailField(required=True)
    passwd = forms.CharField(label='Haslo')
    passwd_reply = forms.CharField(label='Potwierdzenie hasla')
    
    def clean_login(self):
        username = self.cleaned_data['login']
        
        try:
            user = User.objects.all().get(username=username)
        except User.DoesNotExist:
            return username
        else:
             raise forms.ValidationError('Uzytkownik ' + user.username + ' juz istnieje')
    
class LoginForm(forms.Form):
    username = forms.CharField(label='Login', required=True)
    password = forms.CharField(label='Haslo', required=True, widget=forms.PasswordInput)
    
    def clean(self):
        from django.contrib.auth import authenticate
        user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        if user is None:
            raise forms.ValidationError('Podany login lub haslo nie istnieje')
        

    