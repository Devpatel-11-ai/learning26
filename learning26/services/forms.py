from django import forms
from .models import service

class serviceForm(forms.ModelForm):
    class Meta:
        model = service
        fields = '__all__'