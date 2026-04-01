from django.db import models

class PropertyPrediction(models.Model):
    TYPE_CHOICES = [
        ('apartment', 'Appartement'),
        ('house', 'Maison'),
        ('studio', 'Studio'),
        ('duplex', 'Duplex'),
    ]
    
    CITY_CHOICES = [
        ('tunis', 'Tunis'),
        ('sfax', 'Sfax'),
        ('sousse', 'Sousse'),
        ('kairouan', 'Kairouan'),
        ('bizerte', 'Bizerte'),
        ('monastir', 'Monastir'),
    ]
    
    DISTRICT_CHOICES = [
        ('center', 'Centre-ville'),
        ('north', 'Nord'),
        ('south', 'Sud'),
        ('east', 'Est'),
        ('west', 'Ouest'),
        ('medina', 'Médina'),
        ('coastal', 'Zone côtière'),
        ('residential', 'Zone résidentielle'),
    ]
    
    DPE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
    ]
    
    city = models.CharField(max_length=20, choices=CITY_CHOICES)
    district = models.CharField(max_length=15, choices=DISTRICT_CHOICES)
    property_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    rooms = models.IntegerField()
    surface_area = models.FloatField()
    construction_year = models.IntegerField()
    floor = models.IntegerField()
    dpe_rating = models.CharField(max_length=1, choices=DPE_CHOICES)
    parking_spaces = models.IntegerField()
    
    # Champs calculés
    estimated_price = models.FloatField(null=True, blank=True)
    price_per_m2 = models.FloatField(null=True, blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_property_type_display()} - {self.get_city_display()} - {self.surface_area}m²"

class MarketData(models.Model):
    city = models.CharField(max_length=20)
    year = models.IntegerField()
    avg_price_per_m2 = models.FloatField()
    property_type = models.CharField(max_length=20)
    count = models.IntegerField()
    
    class Meta:
        unique_together = ['city', 'year', 'property_type']
