from django.contrib.auth.forms import UserCreationForm,  UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from api.utils import name_check
# ---------------------EXCEPTIONS-----------------------------
from api.exceptions import creation_failed_exception, \
    retrieve_failed_exception
# ------------------------------------------------------------


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    first_name = forms.CharField(label='Enter First name', min_length=3, max_length=150)
    last_name = forms.CharField(label='Enter Last name', min_length=3, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        #---------------User Name check Validations-----------
        should_proceed = name_check(username)
        if should_proceed < 0:
            if should_proceed == -1:
                return creation_failed_exception("UserName is empty.")
            if should_proceed == -2:
                return creation_failed_exception("UserName is very large.")
            if should_proceed == -3:
                return creation_failed_exception("UserName have invalid_characters.")
        #--------------------------------------------------------
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def clean_first_name(self):
        if self.cleaned_data["first_name"].strip() == '':
            raise ValidationError("First name is required.")
        #---------------First Name check Validations-----------
        should_proceed = name_check(self.cleaned_data["first_name"])
        if should_proceed < 0:
            if should_proceed == -1:
                return creation_failed_exception("First Name is empty.")
            if should_proceed == -2:
                return creation_failed_exception("First Name is very large.")
            if should_proceed == -3:
                return creation_failed_exception("First Name have special_characters.")
        #--------------------------------------------------------
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        if self.cleaned_data["last_name"].strip() == '':
            raise ValidationError("Last name is required.")
        #---------------Last Name check Validations-----------
        should_proceed = name_check(self.cleaned_data["last_name"])
        if should_proceed < 0:
            if should_proceed == -1:
                return creation_failed_exception("Last Name is empty.")
            if should_proceed == -2:
                return creation_failed_exception("Last Name is very large.")
            if should_proceed == -3:
                return creation_failed_exception("Last Name have special_characters.")
        #--------------------------------------------------------
        return self.cleaned_data["last_name"]

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],

        )
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.is_superuser = True
            user.save()

        return user

class CustomUserEditForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )
