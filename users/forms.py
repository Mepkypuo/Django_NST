from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="",
                               widget=forms.TextInput(attrs={'class': 'css_input', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label="",
                               widget=forms.PasswordInput(attrs={'class': 'css_input', 'placeholder': 'Пароль'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'css_input', 'placeholder': 'Имя пользователя'})
    )
    email = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'css_input', 'placeholder': 'E-mail'})
    )
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={'class': 'css_input', 'placeholder': 'Пароль'})
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={'class': 'css_input', 'placeholder': 'Повтор пароля'})
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }
