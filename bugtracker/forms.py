from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class FileTicketForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.TextInput, required=True)
