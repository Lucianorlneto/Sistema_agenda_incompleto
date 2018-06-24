from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from .models import *
from functools import partial


User = get_user_model()

DateInput = partial(forms.DateInput, {'id': 'datepicker'})



class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Esse usuário não existe")

            if not user.check_password(password):
                raise forms.ValidationError("senha incorreta")

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email Adress')
    first_name = forms.CharField(label='Nome')
    last_name = forms.CharField(label='Sobrenome')
    email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password*')

    class Meta:
        model = User
        fields = ['username', 'email', 'email2', 'first_name', 'last_name', 'password', 'password2']

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("Emails não coincidem")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("Esse email já está registrado")
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Senhas não coincidem")
        return password

class StaffUserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email Adress')
    first_name = forms.CharField(label='Nome')
    last_name = forms.CharField(label='Sobrenome')
    email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password*')
    escolhas = (
        (1, ("Paciente")),
        (3, ("Recepcionista")),
        (2, ("Clinico")),
    )
    groups = forms.ChoiceField(widget=forms.Select(), choices=escolhas)

    class Meta:
        model = User
        fields = ['username', 'email', 'email2', 'first_name', 'last_name', 'password', 'password2', 'groups']

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("Emails não coincidem")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("Esse email já está registrado")
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Senhas não coincidem")
        return password

class UsuarioForm(forms.ModelForm):

    data_nascimento = forms.DateField(widget=forms.TextInput(attrs={'type': 'text', 'id': 'datepicker'}))

    class Meta:
        model = Usuario
        fields = ['telefone', 'data_nascimento']

    # def clean_data(self):
    #     data_nascimento = self.cleaned_data.get('data_nascimento')
    #     return data_nascimento

class FichaForm(forms.ModelForm):
    paciente_id = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='paciente'))

    class Meta:
        model = Ficha
        fields = ['paciente_id', 'observacao']

class SessoesForm(forms.ModelForm):
    dias = (
        (0, "Segunda"),
        (1, "Terça"),
        (2, "Quarta"),
        (3, "Quinta"),
        (4, "Sexta"),
    )
    horas = (
        (14, "14:00"),
        (16, "16:00"),
        (18, "18:00"),
    )
    numeros = (
        (10, "10"),
        (15, "15"),
        (20, "20"),
    )

    paciente_id = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='paciente'))
    dias_semana = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=dias)
    data_inicial = forms.DateField(widget=forms.TextInput(attrs={'type': 'text', 'id': 'datepicker1'}), label="Data de início")
    # hora = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'id': 'timeformatExample1', 'class':'time'}))
    hora = forms.ChoiceField(widget=forms.Select(), choices=horas)
    numero_sessoes = forms.ChoiceField(widget=forms.Select(), choices=numeros)

    class Meta:
        model = Horario
        fields = ['paciente_id', 'data_inicial', 'dias_semana', 'hora', 'numero_sessoes', 'observacao']

class PacienteSessoesForm(forms.ModelForm):
    dias = (
        (0, "Segunda"),
        (1, "Terça"),
        (2, "Quarta"),
        (3, "Quinta"),
        (4, "Sexta"),
    )
    horas = (
        (14, "14:00"),
        (16, "16:00"),
        (18, "18:00"),
    )
    numeros = (
        (10, "10"),
        (15, "15"),
        (20, "20"),
    )

    dias_semana = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=dias)
    data_inicial = forms.DateField(widget=forms.TextInput(attrs={'type': 'text', 'id': 'datepicker1'}), label="Data de início")
    # hora = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'id': 'timeformatExample1', 'class':'time'}))
    hora = forms.ChoiceField(widget=forms.Select(), choices=horas)
    numero_sessoes = forms.ChoiceField(widget=forms.Select(), choices=numeros)

    class Meta:
        model = Horario
        fields = ['data_inicial', 'dias_semana', 'hora', 'numero_sessoes', 'observacao']