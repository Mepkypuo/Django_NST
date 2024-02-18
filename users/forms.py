from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


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
    training_organization = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'css_input', 'placeholder': 'Название ОО'})
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
        fields = ['username', 'email', 'training_organization', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='', widget=forms.TextInput(attrs={'class': 'css_input'}))
    email = forms.CharField(disabled=True, label='', widget=forms.TextInput(attrs={'class': 'css_input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'training_organization', 'first_name', 'last_name']
        labels = {
            'training_organization': '',
            'first_name': '',
            'last_name': '',
        }
        widgets = {
            'training_organization': forms.TextInput(attrs={'class': 'css_input', 'placeholder': 'Название ОО'}),
            'first_name': forms.TextInput(attrs={'class': 'css_input', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'css_input', 'placeholder': 'Фамилия'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="",
                                   widget=forms.PasswordInput(attrs={'class': 'css_input', 'placeholder': 'Старый пароль'}))
    new_password1 = forms.CharField(label="",
                                    widget=forms.PasswordInput(attrs={'class': 'css_input', 'placeholder': 'Новый пароль'}))
    new_password2 = forms.CharField(label="",
                                    widget=forms.PasswordInput(attrs={'class': 'css_input', 'placeholder': 'Повторите пароль'}))
