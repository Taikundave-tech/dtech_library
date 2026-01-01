from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, LibrarySession, Reservation, Resource

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'phone_number']

class SessionBookForm(forms.ModelForm):
    # Only show available resources
    resource = forms.ModelChoiceField(queryset=Resource.objects.filter(is_available=True),
    empty_label ="select an available resource")
    
    class Meta:
        model = LibrarySession
        fields = ['resource']

class ReservationForm(forms.ModelForm):
    reservation_date = forms.DateTimeField(
        widget=forms.TextInput(attrs={'type': 'datetime-local'}),
        label="Date & Time"
    )
    class Meta:
        model = Reservation
        fields = ['resource', 'reservation_date']
