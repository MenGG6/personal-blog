from django import forms
from .models import Custom

class CustomForm(forms.ModelForm):
	
	class Meta:
		model = Custom
		fields = ('name','phone')
	
