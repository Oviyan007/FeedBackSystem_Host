from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile,FeedbackRes,Faculty

# class RegistrationForm(UserCreationForm):
#     DESIGNATION_CHOICES = [
#         ('STUDENT', 'Student'),
#         ('FACULTY', 'Faculty'),
#     ]
#     name = forms.CharField(max_length=50, required=True)
#     designation = forms.ChoiceField(choices=DESIGNATION_CHOICES, widget=forms.Select)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2', 'designation']

class RegistrationForm(UserCreationForm):
    name = forms.CharField()
    designation = forms.ChoiceField(choices=[('student', 'Student'), ('faculty', 'Faculty')])
    faculty_code = forms.CharField(required=False)  # Only required if designation is faculty

    class Meta:
        model = User
        fields = ['username', 'password1', 'email', 'name', 'designation', 'faculty_code','password2' ]
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        designation = cleaned_data.get("designation")
        faculty_code = cleaned_data.get("faculty_code")

        if designation == "faculty" and not faculty_code:
            raise forms.ValidationError("Faculty code is required for faculty registration.")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name']

# form for getting responses
OPTION_CHOICES=[('5','Excellent'),('4','Better'),('3','Good'),('2','Average'),('1','Below Average')]

class OptionForm(forms.Form):
    options = forms.ChoiceField(
        choices=OPTION_CHOICES,
        widget=forms.RadioSelect
    )
class FeedBackForm(forms.ModelForm):
    class Meta:
        model=FeedbackRes
        fields = ['department', 'Response', 'Qno']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'designation', 'batch']
        widgets = {
            'designation': forms.Select(attrs={'class': 'form-control'}),
            'batch': forms.Select(attrs={'class': 'form-control'}),
        }