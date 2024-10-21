from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile,FeedbackRes

class RegistrationForm(UserCreationForm):
    DESIGNATION_CHOICES = [
        ('STUDENT', 'Student'),
        ('FACULTY', 'Faculty'),
    ]

    designation = forms.ChoiceField(choices=DESIGNATION_CHOICES, widget=forms.Select)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'designation']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name']

# form for getting responses
OPTION_CHOICES=[('5','Excellent'),('4','better'),('3','good'),('2','Average'),('1','BelowAverage')]

class OptionForm(forms.Form):
    options = forms.ChoiceField(
        choices=OPTION_CHOICES,
        widget=forms.RadioSelect
    )
class FeedBackForm(forms.ModelForm):
    class Meta:
        model=FeedbackRes
        fields = ['department', 'Response', 'Qno']


