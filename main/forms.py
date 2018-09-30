from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(label="Login", max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
