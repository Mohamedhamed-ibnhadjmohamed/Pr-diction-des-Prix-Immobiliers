from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Property, PropertyFeature, Prediction
from .forms import PropertyForm, PropertyFeatureForm, PredictionForm
import random
import numpy as np

def home(request):
    """Page d'accueil avec statistiques et propriétés récentes"""
    total_properties = Property.objects.count()
    avg_price = Property.objects.aggregate(Avg('price'))['price__avg'] or 0
    recent_properties = Property.objects.order_by('-created_at')[:6]
    
    context = {
        'total_properties': total_properties,
        'avg_price': avg_price,
        'recent_properties': recent_properties,
    }
    return render(request, 'immobilier/home.html', context)

def property_list(request):
    """Liste de toutes les propriétés avec filtres"""
    properties = Property.objects.all()
    
    # Filtres
    property_type = request.GET.get('type')
    city = request.GET.get('city')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_surface = request.GET.get('min_surface')
    
    if property_type:
        properties = properties.filter(property_type=property_type)
    if city:
        properties = properties.filter(city__icontains=city)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    if min_surface:
        properties = properties.filter(surface__gte=min_surface)
    
    # Pagination
    paginator = Paginator(properties, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'property_types': Property.TYPE_CHOICES,
        'cities': Property.objects.values_list('city', flat=True).distinct(),
    }
    return render(request, 'immobilier/property_list.html', context)

def property_detail(request, pk):
    """Détail d'une propriété"""
    property = get_object_or_404(Property, pk=pk)
    features = getattr(property, 'features', None)
    predictions = property.predictions.all()
    
    # Propriétés similaires
    similar_properties = Property.objects.filter(
        property_type=property.property_type,
        city=property.city
    ).exclude(pk=pk)[:3]
    
    context = {
        'property': property,
        'features': features,
        'predictions': predictions,
        'similar_properties': similar_properties,
    }
    return render(request, 'immobilier/property_detail.html', context)

@login_required
def predict_price(request):
    """Interface de prédiction de prix"""
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            # Simulation de prédiction (remplacer par modèle ML réel)
            predicted_price = simulate_price_prediction(form.cleaned_data)
            confidence_score = random.uniform(0.7, 0.95)
            
            # Créer une propriété temporaire pour la prédiction
            temp_property = Property.objects.create(
                title=f"Prédiction - {form.cleaned_data['city']}",
                property_type=form.cleaned_data['property_type'],
                city=form.cleaned_data['city'],
                surface=form.cleaned_data['surface'],
                rooms=form.cleaned_data['rooms'],
                bedrooms=form.cleaned_data['bedrooms'],
                price=predicted_price
            )
            
            # Sauvegarder la prédiction
            prediction = Prediction.objects.create(
                property=temp_property,
                predicted_price=predicted_price,
                confidence_score=confidence_score,
                model_version="v1.0"
            )
            
            messages.success(request, f"Prédiction réussie! Prix estimé: {predicted_price:,.2f}€")
            return redirect('immobilier:prediction_result', pk=prediction.pk)
    else:
        form = PredictionForm()
    
    return render(request, 'immobilier/predict_price.html', {'form': form})

def prediction_result(request, pk):
    """Résultat de prédiction"""
    prediction = get_object_or_404(Prediction, pk=pk)
    return render(request, 'immobilier/prediction_result.html', {'prediction': prediction})

@login_required
def add_property(request):
    """Ajouter une nouvelle propriété"""
    if request.method == 'POST':
        property_form = PropertyForm(request.POST)
        feature_form = PropertyFeatureForm(request.POST)
        
        if property_form.is_valid() and feature_form.is_valid():
            property = property_form.save(commit=False)
            property.created_by = request.user
            property.save()
            features = feature_form.save(commit=False)
            features.property = property
            features.save()
            
            messages.success(request, "Propriété ajoutée avec succès!")
            return redirect('immobilier:property_detail', pk=property.pk)
    else:
        property_form = PropertyForm()
        feature_form = PropertyFeatureForm()
    
    return render(request, 'immobilier/add_property.html', {
        'property_form': property_form,
        'feature_form': feature_form,
    })

def simulate_price_prediction(data):
    """Simulation de prédiction de prix (remplacer par modèle ML réel)"""
    base_price = {
        'appartement': 3000,
        'maison': 4000,
        'studio': 2500,
        'villa': 6000,
        'terrain': 500,
    }.get(data['property_type'], 3000)
    
    price = base_price * data['surface']
    
    # Ajustements selon les caractéristiques
    if data.get('has_garden'):
        price *= 1.1
    if data.get('has_pool'):
        price *= 1.15
    if data.get('has_garage'):
        price *= 1.05
    if data.get('has_elevator'):
        price *= 1.03
    
    # Ajustement selon la ville (simulation)
    city_multiplier = {
        'paris': 1.5,
        'lyon': 1.2,
        'marseille': 1.1,
        'nice': 1.15,
    }.get(data['city'].lower(), 1.0)
    
    price *= city_multiplier
    
    # Ajouter un peu d'aléatoire
    price *= random.uniform(0.9, 1.1)
    
    return round(price, 2)
