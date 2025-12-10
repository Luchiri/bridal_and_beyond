from django import forms
from .models import Board, BoardItem, Profile
from django.contrib.auth.models import User

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'description', 'category']

class BoardItemForm(forms.ModelForm):
    class Meta:
        model = BoardItem
        fields = ['name', 'image_url']

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", required=False)
    last_name = forms.CharField(label="Last Name", required=False)
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_picture', 'bio', 'phone_number', 'location',
            'instagram', 'facebook', 'twitter', 'gender'
        ]