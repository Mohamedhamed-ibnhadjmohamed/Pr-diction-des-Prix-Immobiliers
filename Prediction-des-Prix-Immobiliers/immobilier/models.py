from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('agent', 'Agent Immobilier'),
        ('vendeur', 'Vendeur'),
        ('acheteur', 'Acheteur'),
        ('admin', 'Administrateur'),
    ]
    
    # Use email as username
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='acheteur')
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Set email as USERNAME_FIELD
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    # Use custom manager
    objects = CustomUserManager()
    
    # Fix reverse accessor conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="customuser",
    )
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_agent(self):
        return self.role == 'agent'
    
    @property
    def is_vendeur(self):
        return self.role == 'vendeur'
    
    @property
    def is_acheteur(self):
        return self.role == 'acheteur'

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company = models.CharField(max_length=100, blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    social_links = models.JSONField(default=dict, blank=True)
    preferences = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"
    
    def __str__(self):
        return f"Profil de {self.user.username}"

class Property(models.Model):
    TYPE_CHOICES = [
        ('appartement', 'Appartement'),
        ('maison', 'Maison'),
        ('studio', 'Studio'),
        ('villa', 'Villa'),
        ('terrain', 'Terrain'),
    ]
    
    title = models.CharField(max_length=200)
    property_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    surface = models.FloatField(help_text="Surface en m²")
    rooms = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField(default=1)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Propriété"
        verbose_name_plural = "Propriétés"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.city}"

class PropertyFeature(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='features')
    has_garden = models.BooleanField(default=False)
    has_pool = models.BooleanField(default=False)
    has_garage = models.BooleanField(default=False)
    has_balcony = models.BooleanField(default=False)
    has_elevator = models.BooleanField(default=False)
    floor = models.IntegerField(default=0, help_text="Étage")
    total_floors = models.IntegerField(default=0, help_text="Nombre total d'étages")
    construction_year = models.IntegerField()
    energy_efficiency = models.CharField(max_length=10, choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
    ], default='D')
    
    class Meta:
        verbose_name = "Caractéristique"
        verbose_name_plural = "Caractéristiques"
    
    def __str__(self):
        return f"Caractéristiques de {self.property.title}"

class Prediction(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='predictions')
    predicted_price = models.DecimalField(max_digits=12, decimal_places=2)
    confidence_score = models.FloatField(help_text="Score de confiance entre 0 et 1")
    model_version = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Prédiction"
        verbose_name_plural = "Prédiction"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Prédiction pour {self.property.title}: {self.predicted_price}€"

class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Favori"
        verbose_name_plural = "Favoris"
        unique_together = ['user', 'property']  # Un utilisateur ne peut mettre un bien en favori qu'une fois
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} favoris {self.property.title}"

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True, related_name='messages')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message de {self.sender.email} à {self.recipient.email}: {self.subject}"

class PropertyRating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ratings')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Évaluation"
        verbose_name_plural = "Évaluations"
        unique_together = ['user', 'property']  # Un utilisateur ne peut évaluer un bien qu'une fois
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Évaluation de {self.property.title} par {self.user.email}: {self.rating}/5"

class SearchHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='search_history')
    query_params = models.JSONField(default=dict)
    results_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Historique de recherche"
        verbose_name_plural = "Historiques de recherche"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Recherche de {self.user.email} - {self.created_at.strftime('%d/%m/%Y')}"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('message', 'Nouveau message'),
        ('favorite', 'Bien ajouté aux favoris'),
        ('rating', 'Nouvelle évaluation'),
        ('property_view', 'Consultation de bien'),
        ('property_update', 'Mise à jour de bien'),
        ('system', 'Notification système'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Optional related objects
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    sender = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"

class UserReview(models.Model):
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews_given')
    reviewed_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Avis utilisateur"
        verbose_name_plural = "Avis utilisateurs"
        unique_together = ['reviewer', 'reviewed_user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Avis de {self.reviewer.email} sur {self.reviewed_user.email}"

class Report(models.Model):
    REPORT_TYPES = [
        ('property', 'Bien immobilier'),
        ('user', 'Utilisateur'),
        ('message', 'Message'),
        ('comment', 'Commentaire'),
    ]
    
    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reports_made')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    reason = models.CharField(max_length=200)
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Related objects
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True, related_name='reports')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='reports')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True, related_name='reports')
    
    class Meta:
        verbose_name = "Signalement"
        verbose_name_plural = "Signalements"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Signalement {self.report_type} par {self.reporter.email}"

class PropertyComparison(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comparisons')
    properties = models.ManyToManyField(Property, related_name='comparisons')
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Comparaison de biens"
        verbose_name_plural = "Comparaisons de biens"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comparaison '{self.name}' par {self.user.email}"

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('property_pdf', 'PDF du bien'),
        ('contract', 'Contrat'),
        ('invoice', 'Facture'),
        ('id_card', 'Carte d\'identité'),
        ('other', 'Autre'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='documents')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.email}"

class Recommendation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recommendations')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='recommendations')
    score = models.FloatField(help_text="Score de recommandation entre 0 et 1")
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Recommandation"
        verbose_name_plural = "Recommandations"
        ordering = ['-score', '-created_at']
        unique_together = ['user', 'property']
    
    def __str__(self):
        return f"Recommandation pour {self.user.email} - {self.property.title}"
