from django import forms
from .models import User, Role

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'role']  # Include the role field

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['role'].queryset = Role.objects.all()  # Fetch all roles
        self.fields['password'].widget = forms.PasswordInput()  # Password input

