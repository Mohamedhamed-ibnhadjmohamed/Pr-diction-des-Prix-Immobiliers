from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, UserProfile, Property, PropertyFeature, Message, PropertyRating

W = {'class': 'form-control'}
WC = {'class': 'form-check-input'}


# ─── Authentification ───────────────────────────────────────────────────────

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs=W))
    password2 = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput(attrs=W))

    class Meta:
        model  = CustomUser
        fields = ['first_name', 'last_name', 'email', 'role', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs=W),
            'last_name':  forms.TextInput(attrs=W),
            'email':      forms.EmailInput(attrs=W),
            'role':       forms.Select(attrs=W),
            'phone':      forms.TextInput(attrs=W),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs=W))
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs=W))


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model  = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'bio', 'profile_picture']
        widgets = {
            'first_name':      forms.TextInput(attrs=W),
            'last_name':       forms.TextInput(attrs=W),
            'phone':           forms.TextInput(attrs=W),
            'bio':             forms.Textarea(attrs={**W, 'rows': 3}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model  = UserProfile
        fields = ['company', 'license_number', 'website']
        widgets = {
            'company':        forms.TextInput(attrs=W),
            'license_number': forms.TextInput(attrs=W),
            'website':        forms.URLInput(attrs=W),
        }


# ─── Bien immobilier ────────────────────────────────────────────────────────

class PropertyForm(forms.ModelForm):
    class Meta:
        model  = Property
        fields = ['title', 'property_type', 'address', 'city', 'postal_code',
                  'surface', 'rooms', 'bedrooms', 'bathrooms', 'description', 'price']
        widgets = {
            'title':         forms.TextInput(attrs=W),
            'property_type': forms.Select(attrs=W),
            'address':       forms.Textarea(attrs={**W, 'rows': 2}),
            'city':          forms.TextInput(attrs=W),
            'postal_code':   forms.TextInput(attrs=W),
            'surface':       forms.NumberInput(attrs={**W, 'step': '0.1', 'min': '1'}),
            'rooms':         forms.NumberInput(attrs={**W, 'min': '1'}),
            'bedrooms':      forms.NumberInput(attrs={**W, 'min': '0'}),
            'bathrooms':     forms.NumberInput(attrs={**W, 'min': '1'}),
            'description':   forms.Textarea(attrs={**W, 'rows': 3}),
            'price':         forms.NumberInput(attrs={**W, 'step': '0.01', 'min': '0'}),
        }


class PropertyFeatureForm(forms.ModelForm):
    class Meta:
        model   = PropertyFeature
        exclude = ['property']
        widgets = {
            'has_garden':        forms.CheckboxInput(attrs=WC),
            'has_pool':          forms.CheckboxInput(attrs=WC),
            'has_garage':        forms.CheckboxInput(attrs=WC),
            'has_balcony':       forms.CheckboxInput(attrs=WC),
            'has_elevator':      forms.CheckboxInput(attrs=WC),
            'floor':             forms.NumberInput(attrs={**W, 'min': '0'}),
            'total_floors':      forms.NumberInput(attrs={**W, 'min': '0'}),
            'construction_year': forms.NumberInput(attrs={**W, 'min': '1900', 'max': '2024'}),
            'energy_efficiency': forms.Select(attrs=W),
        }


# ─── Prédiction ─────────────────────────────────────────────────────────────

class PredictionForm(forms.Form):
    CITY_CHOICES = [
        ('', '-- Choisir une ville --'),
        ('Tunis',    'Tunis'),
        ('Ariana',   'Ariana'),
        ('La Marsa', 'La Marsa'),
        ('Sousse',   'Sousse'),
        ('Sfax',     'Sfax'),
        ('Nabeul',   'Nabeul'),
        ('Hammamet', 'Hammamet'),
        ('Monastir', 'Monastir'),
        ('Bizerte',  'Bizerte'),
        ('Gabes',    'Gabes'),
        ('Autre',    'Autre'),
    ]

    property_type = forms.ChoiceField(
        choices=Property.TYPE_CHOICES, widget=forms.Select(attrs=W), label='Type de bien')
    city = forms.ChoiceField(
        choices=CITY_CHOICES, widget=forms.Select(attrs=W), label='Ville')
    surface = forms.FloatField(
        min_value=10, widget=forms.NumberInput(attrs={**W, 'step': '0.1'}), label='Surface (m²)')
    rooms = forms.IntegerField(
        min_value=1, widget=forms.NumberInput(attrs={**W, 'min': '1'}), label='Nombre de pièces')
    bedrooms = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={**W, 'min': '0'}), label='Chambres')
    construction_year = forms.IntegerField(
        min_value=1900, max_value=2024,
        widget=forms.NumberInput(attrs={**W, 'min': '1900', 'max': '2024'}),
        label="Année de construction", required=False)
    has_garden   = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=WC), label='Jardin')
    has_pool     = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=WC), label='Piscine')
    has_garage   = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=WC), label='Garage')
    has_balcony  = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=WC), label='Balcon')
    has_elevator = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=WC), label='Ascenseur')


# ─── Messagerie & évaluations ───────────────────────────────────────────────

class MessageForm(forms.ModelForm):
    class Meta:
        model   = Message
        fields  = ['subject', 'content']
        widgets = {
            'subject': forms.TextInput(attrs=W),
            'content': forms.Textarea(attrs={**W, 'rows': 5}),
        }


class PropertyRatingForm(forms.ModelForm):
    class Meta:
        model   = PropertyRating
        fields  = ['rating', 'comment']
        widgets = {
            'rating':  forms.Select(attrs=W),
            'comment': forms.Textarea(attrs={**W, 'rows': 3}),
        }


# ─── Recherche avancée ──────────────────────────────────────────────────────

class SearchForm(forms.Form):
    keyword      = forms.CharField(required=False, widget=forms.TextInput(attrs={**W, 'placeholder': 'Titre, ville…'}), label='Mot-clé')
    property_type = forms.ChoiceField(
        choices=[('', 'Tous les types')] + Property.TYPE_CHOICES,
        required=False, widget=forms.Select(attrs=W), label='Type')
    city         = forms.CharField(required=False, widget=forms.TextInput(attrs=W), label='Ville')
    min_price    = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={**W, 'placeholder': '0'}), label='Prix min (DT)')
    max_price    = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={**W, 'placeholder': '9 999 999'}), label='Prix max (DT)')
    min_surface  = forms.FloatField(required=False, min_value=0, widget=forms.NumberInput(attrs={**W, 'placeholder': '0'}), label='Surface min (m²)')
    max_surface  = forms.FloatField(required=False, widget=forms.NumberInput(attrs=W), label='Surface max (m²)')
    min_rooms    = forms.IntegerField(required=False, min_value=0, widget=forms.NumberInput(attrs=W), label='Pièces min')
    has_garden   = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=WC), label='Jardin')
    has_pool     = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=WC), label='Piscine')
    has_garage   = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=WC), label='Garage')
