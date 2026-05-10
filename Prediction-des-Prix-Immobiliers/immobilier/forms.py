from django import forms
from .models import Property, PropertyFeature

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'property_type', 'address', 'city', 'postal_code', 
                 'surface', 'rooms', 'bedrooms', 'bathrooms', 'description', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'surface': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'rooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class PropertyFeatureForm(forms.ModelForm):
    class Meta:
        model = PropertyFeature
        exclude = ['property']
        widgets = {
            'has_garden': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_pool': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_garage': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_balcony': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_elevator': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_floors': forms.NumberInput(attrs={'class': 'form-control'}),
            'construction_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'energy_efficiency': forms.Select(attrs={'class': 'form-control'}),
        }

class PredictionForm(forms.Form):
    property_type = forms.ChoiceField(
        choices=Property.TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Type de bien"
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Ville"
    )
    surface = forms.FloatField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        label="Surface (m²)"
    )
    rooms = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Nombre de pièces"
    )
    bedrooms = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Nombre de chambres"
    )
    has_garden = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Jardin"
    )
    has_pool = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Piscine"
    )
    has_garage = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Garage"
    )
    has_elevator = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Ascenseur"
    )
