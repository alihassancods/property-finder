from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Agent,Property, Community

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'location', 'description','images']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'images': forms.FileInput(attrs={'class': 'form-control'}),
        }

class PropertyForm(forms.ModelForm):
    forms.FileField(widget = forms.TextInput(attrs={
            "name": "images",
            "type": "File",
            "class": "form-control",
            "multiple": "True",
        }), label = "")
    # images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    class Meta:
        model = Property
        exclude = ['created_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'facility_type': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.NumberInput(attrs={'class': 'form-control'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'facilities': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'community': forms.Select(attrs={'class': 'form-control'}),
            'agent': forms.Select(attrs={'class': 'form-control'}),
            'is_for_sale': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_for_rent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name','last_name','password1', 'password2', 'role', 'contact_number']

class AgentProfileForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = [
            'full_name',
            'country',
            'phone',
            'whatsapp_number',
            'profile_picture',
            'about',
            'email',
            'languages',
        ]
