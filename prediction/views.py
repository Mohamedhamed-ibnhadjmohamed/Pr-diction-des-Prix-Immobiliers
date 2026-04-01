from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import random
from datetime import datetime, timedelta

def home(request):
    return render(request, 'prediction/home.html')

@method_decorator(csrf_exempt, name='dispatch')
class PredictionAPI(View):
    def post(self, request):
        data = json.loads(request.body)
        
        # Simulation de prédiction (remplacer par vrai modèle ML)
        base_price = self.calculate_base_price(data)
        
        result = {
            'estimated_price': base_price,
            'price_per_m2': round(base_price / data['surface_area'], 2),
            'confidence_score': random.uniform(78, 95),
            'market_avg_price': self.get_market_avg(data['city']),
            'similar_properties': random.randint(15, 45),
            'market_trend': random.choice(['+4.2%', '-1.8%', '+2.1%', '-0.5%']),
            'factors': {
                'Localisation': 38,
                'Surface': 25,
                'Type de bien': 14,
                'DPE': 12,
                'Ancienneté': 7,
                'Étage': 4
            }
        }
        
        # Sauvegarder la prédiction
        from .models import PropertyPrediction
        prediction = PropertyPrediction.objects.create(
            city=data['city'],
            district=data['district'],
            property_type=data['property_type'],
            rooms=data['rooms'],
            surface_area=data['surface_area'],
            construction_year=data['construction_year'],
            floor=data['floor'],
            dpe_rating=data['dpe_rating'],
            parking_spaces=data['parking_spaces'],
            estimated_price=result['estimated_price'],
            price_per_m2=result['price_per_m2'],
            confidence_score=result['confidence_score']
        )
        
        return JsonResponse(result)
    
    def calculate_base_price(self, data):
        # Prix de base par ville (en TND/m² pour le marché tunisien)
        city_prices = {
            'tunis': 4500,  # Tunis: centre économique et administratif
            'sfax': 3200,   # Sfax: deuxième ville économique
            'sousse': 3800, # Sousse: ville touristique
            'kairouan': 2200, # Kairouan: ville historique
            'bizerte': 2800, # Bizerte: port et industrie
            'monastir': 3500 # Monastir: tourisme et aéroport
        }
        
        base_price = city_prices.get(data['city'], 3000) * data['surface_area']
        
        # Ajustements
        if data['property_type'] == 'house':
            base_price *= 1.1
        elif data['property_type'] == 'studio':
            base_price *= 0.9
        
        # DPE impact (adapté pour le climat tunisien)
        dpe_impact = {'A': 1.05, 'B': 1.03, 'C': 1.0, 'D': 0.97, 'E': 0.94, 'F': 0.90}
        base_price *= dpe_impact.get(data['dpe_rating'], 1.0)
        
        # Parking (plus rare et donc plus valorisé en Tunisie)
        base_price += data['parking_spaces'] * 25000
        
        return round(base_price, 2)
    
    def get_market_avg(self, city):
        prices = {
            'tunis': 4200,
            'sfax': 3000,
            'sousse': 3500,
            'kairouan': 2000,
            'bizerte': 2600,
            'monastir': 3200
        }
        return prices.get(city, 3000)

def analysis_data(request):
    city = request.GET.get('city', 'tunis')
    
    # Données simulées pour les graphiques
    evolution_data = {
        'years': ['2019', '2020', '2021', '2022', '2023', '2024'],
        'prices': generate_evolution_prices(city)
    }
    
    repartition_data = {
        'Appartement': 45,
        'Maison': 35,
        'Studio': 15,
        'Duplex': 5
    }
    
    city_comparison = {
        'Tunis': 4200,
        'Sfax': 3000,
        'Sousse': 3500,
        'Kairouan': 2000,
        'Bizerte': 2600,
        'Monastir': 3200
    }
    
    return JsonResponse({
        'evolution': evolution_data,
        'repartition': repartition_data,
        'comparison': city_comparison
    })

def generate_evolution_prices(city):
    base_prices = {
        'tunis': [3500, 3700, 3900, 4100, 4300, 4200],
        'sfax': [2500, 2600, 2800, 2900, 3100, 3000],
        'sousse': [3000, 3100, 3300, 3400, 3600, 3500],
        'kairouan': [1700, 1800, 1900, 2000, 2100, 2000],
        'bizerte': [2200, 2300, 2400, 2500, 2700, 2600],
        'monastir': [2800, 2900, 3100, 3200, 3400, 3200]
    }
    return base_prices.get(city, base_prices['tunis'])

def simulation_data(request):
    surface = float(request.GET.get('surface', 100))
    floor = int(request.GET.get('floor', 3))
    age = int(request.GET.get('age', 20))
    dpe = int(request.GET.get('dpe', 3))
    
    # Calcul des impacts (adaptés pour le marché tunisien en TND)
    surface_impact = (surface - 100) * 3500  # TND par m² supplémentaire
    floor_impact = (floor - 3) * 8000       # Impact de l'étage
    age_impact = -age * 2000                # Pénalité par année d'ancienneté
    dpe_impact = (3 - dpe) * 25000          # Impact du DPE
    
    base_price = 300000  # 300 000 TND de base pour bien moyen
    simulated_price = base_price + surface_impact + floor_impact + age_impact + dpe_impact
    
    return JsonResponse({
        'simulated_price': max(80000, simulated_price),  # Prix minimum 80 000 TND
        'impacts': {
            'surface': surface_impact,
            'floor': floor_impact,
            'age': age_impact,
            'dpe': dpe_impact
        }
    })

def history_data(request):
    from .models import PropertyPrediction
    
    predictions = PropertyPrediction.objects.all().order_by('-created_at')[:10]
    
    history = []
    for pred in predictions:
        history.append({
            'type': pred.get_property_type_display(),
            'city': pred.get_city_display(),
            'surface': pred.surface_area,
            'price': pred.estimated_price,
            'trend': random.choice(['+4.2%', '-1.8%', '+2.1%', '-0.5%']),
            'date': pred.created_at.strftime('%Y-%m-%d')
        })
    
    return JsonResponse({'history': history})
