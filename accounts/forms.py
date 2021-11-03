  
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

def email(value):
    if  User.objects.filter(email=email).exists():
        raise forms.ValidationError("You have forgotten about Fred!")

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields =('first_name','last_name','password','email','username')
        widgets = {'password':forms.PasswordInput}
        
    def clean(self):
        super(RegistrationForm, self).clean()
        # extract the username and text field from the data
        email= self.cleaned_data.get('email')
        print("HWE")
        # conditions to be met for the username length
        if User.objects.filter(email=email).exists():
            print("1")
            self._errors['email'] = self.error_class([
                'Minimum 5 characters required'])
        # return any errors if found
        print("2")
        return self.cleaned_data
        print("3")
    # def clean(self):
    #     cleaned_data = super().clean()
    #     email = cleaned_data.get("email")
    #     # email = value.cleaned_data.get('email')
    #     if User.objects.filter(email=email).exists():
    #         raise ValidationError("You have forgotten about Fred!")
    #         print("error")
    #     return self.cleaned_data
# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm

# class RegistrationForm(UserCreationForm):

#     class Meta:
#         model = User
#         fields = ['username',
#                   'email',
#                   'first_name',
#                   'last_name',
#                   ]