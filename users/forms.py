from django import forms


class LoginUserForm(forms.Form):
    username = forms.CharField(label="",
                               widget=forms.TextInput(attrs={'class': 'css_input', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label="",
                               widget=forms.PasswordInput(attrs={'class': 'css_input', 'placeholder': 'Пароль'}))
