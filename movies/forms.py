from django import forms
from django.core.exceptions import ValidationError
from .models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'repeat_password']

    def clean(self):
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']
        if password != repeat_password:
            raise ValidationError("Пароли должны совпадать.")

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError(f"Имя пользователя {username} уже используется, пожалуйста, придумайте другое.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError("Адрес электронной почты не может быть пустым.")
        return email