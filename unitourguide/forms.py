from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Tour

class SignupForm(forms.Form):
    username = forms.CharField(label='User name', max_length=20)
    firstname = forms.CharField(label='first name', max_length=20)
    lastname = forms.CharField(label='Last name', max_length=20)
    password = forms.CharField(label='Pass Word', max_length=20, widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="PasswordConfirmation")
    class Meta:
        fields = ("username", "firstname", "lastname", "password")
    def clean_username(self):
        username = self.cleaned_data.get('username')
        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            raise ValidationError("Username already exists, please choose another one")
        return username
    def clean_password1(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if password and password1 and password != password1:
            raise ValidationError("Password did n't match")
        return password1

class UploadImageFormID(forms.Form):
    image_ID = forms.ImageField()

class UploadImageFormUni(forms.Form):
    image_uni = forms.ImageField()

class UploadImageFormPhoto(forms.Form):
    image_photo = forms.ImageField()

class ReviewForm(forms.ModelForm):
    class Meta:        
        model = Tour        
        fields = ['rating','feedback']
    def clean(self):
        cleaned_data = self.cleaned_data
        feedback = cleaned_data['feedback']
        rating = cleaned_data['rating']
        if not feedback:
            raise ValidationError("Please enter your feedback.")
        if not rating:
            raise ValidationError("Please enter your rating.")
        if rating>5 or rating<0:
            raise ValidationError("Rating should between 0 and 5.")
        return cleaned_data

    