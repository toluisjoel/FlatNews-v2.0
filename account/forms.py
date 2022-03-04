from django import forms
from .models import Profile
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        passwords = self.cleaned_data
        if passwords['password1'] != passwords['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return passwords['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('GENDER_CHOICES', 'user')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
