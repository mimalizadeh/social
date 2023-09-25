from django import forms
from django.contrib.auth.models import User
from django.core.validators import ValidationError
from account.models import UserProfile


class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-3', 'placeholder': "Username"}),
                               label='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control py-3', 'placeholder': "Email"}),
                             label='')
    password1 = forms.CharField(label='',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control py-3', 'placeholder': "Password"}))
    password2 = forms.CharField(label="",
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control py-3', 'placeholder': "Confirm password"}))

    def clean_email(self):
        """
        email validation
        """
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email is already exists')
        return email

    def clean_username(self):
        """
        username validation
        """
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if user:
            raise ValidationError('This username already exists')
        return username

    def clean(self):
        """
        password validation
        """

        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError('Password must match')


class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-3', 'placeholder': 'Username', }),
        label='')
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control py-3', 'placeholder': 'Password'}),
        label='')


class UserEditProfileForm(forms.ModelForm):
    name = forms.CharField(max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Firstname'}),
                           label="")
    family = forms.CharField(max_length=100,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lastname'}),
                             label="")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                             label="")

    class Meta:
        model = UserProfile
        fields = ['age', 'bio', 'phone', 'address']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'bio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bio'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'address': forms.Textarea(attrs={'class': 'form-control ', 'rows': 3, 'placeholder': 'Address'})
        }
        labels = {
            'age': "",
            'bio': "",
            'phone': "",
            'address': "",
        }
