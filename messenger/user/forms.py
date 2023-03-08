from django import forms
from .models import User


class WriterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar']
        exclude = ['user_id']