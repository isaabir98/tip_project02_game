from django import forms
from .models import User, Role

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'role']  

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['role'].queryset = Role.objects.all()  # Fetch all roles

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user
