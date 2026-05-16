from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# ─────────────────────────────────────────────
#  Gestionnaire utilisateur personnalisé
# ─────────────────────────────────────────────

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


# ─────────────────────────────────────────────
#  Utilisateur
# ─────────────────────────────────────────────

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin',        'Administrateur'),
        ('agent',        'Agent Immobilier'),
        ('vendeur',      'Vendeur'),
        ('proprietaire', 'Propriétaire'),
        ('acheteur',     'Acheteur'),
        ('investisseur', 'Investisseur'),
    ]

    username       = None
    email          = models.EmailField(unique=True, verbose_name='Email')
    role           = models.CharField(max_length=20, choices=ROLE_CHOICES, default='acheteur')
    phone          = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio            = models.TextField(max_length=500, blank=True)
    is_verified    = models.BooleanField(default=False)
    created_at     = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects         = CustomUserManager()

    groups = models.ManyToManyField(
        'auth.Group', blank=True,
        related_name='customuser_set', related_query_name='customuser',
        db_table='customuser_groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', blank=True,
        related_name='customuser_set', related_query_name='customuser',
        db_table='customuser_user_permissions',
    )

    class Meta:
        db_table = 'customuser'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    # Propriétés de rôle
    @property
    def is_admin_role(self):    return self.role == 'admin'
    @property
    def is_agent(self):         return self.role == 'agent'
    @property
    def is_vendeur(self):       return self.role in ('vendeur', 'proprietaire')
    @property
    def is_acheteur(self):      return self.role in ('acheteur', 'investisseur')
    @property
    def can_add_property(self): return self.role in ('agent', 'vendeur', 'proprietaire', 'admin')


class UserProfile(models.Model):
    user           = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    company        = models.CharField(max_length=100, blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    website        = models.URLField(blank=True)
    preferences    = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'userprofile'
        verbose_name = 'Profil utilisateur'
        verbose_name_plural = 'Profils utilisateurs'

    def __str__(self):
        return f"Profil de {self.user.email}"


# ─────────────────────────────────────────────
#  Bien immobilier
# ─────────────────────────────────────────────

class Property(models.Model):
    TYPE_CHOICES = [
        ('appartement', 'Appartement'),
        ('maison',      'Maison'),
        ('studio',      'Studio'),
        ('villa',       'Villa'),
        ('terrain',     'Terrain'),
    ]

    title         = models.CharField(max_length=200, verbose_name='Titre')
    property_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Type')
    address       = models.TextField(verbose_name='Adresse')
    city          = models.CharField(max_length=100, verbose_name='Ville')
    postal_code   = models.CharField(max_length=10, verbose_name='Code postal')
    surface       = models.FloatField(verbose_name='Surface (m²)')
    rooms         = models.IntegerField(verbose_name='Pièces')
    bedrooms      = models.IntegerField(verbose_name='Chambres')
    bathrooms     = models.IntegerField(default=1, verbose_name='Salles de bain')
    description   = models.TextField(blank=True, verbose_name='Description')
    price         = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Prix (DT)')
    created_by    = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties')
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'property'
        verbose_name = 'Propriété'
        verbose_name_plural = 'Propriétés'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.city}"

    def get_average_rating(self):
        from django.db.models import Avg
        result = self.ratings.aggregate(Avg('rating'))['rating__avg']
        return round(result, 1) if result else None


class PropertyFeature(models.Model):
    ENERGY_CHOICES = [(x, x) for x in ('A', 'B', 'C', 'D', 'E', 'F', 'G')]

    property          = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='features')
    has_garden        = models.BooleanField(default=False, verbose_name='Jardin')
    has_pool          = models.BooleanField(default=False, verbose_name='Piscine')
    has_garage        = models.BooleanField(default=False, verbose_name='Garage')
    has_balcony       = models.BooleanField(default=False, verbose_name='Balcon')
    has_elevator      = models.BooleanField(default=False, verbose_name='Ascenseur')
    floor             = models.IntegerField(default=0, verbose_name='Étage')
    total_floors      = models.IntegerField(default=0, verbose_name="Nombre d'étages")
    construction_year = models.IntegerField(verbose_name='Année de construction')
    energy_efficiency = models.CharField(max_length=2, choices=ENERGY_CHOICES, default='D', verbose_name='DPE')

    class Meta:
        db_table = 'propertyfeature'
        verbose_name = 'Caractéristiques'
        verbose_name_plural = 'Caractéristiques'

    def __str__(self):
        return f"Caractéristiques — {self.property.title}"


# ─────────────────────────────────────────────
#  Prédiction de prix
# ─────────────────────────────────────────────

class Prediction(models.Model):
    property         = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='predictions')
    predicted_price  = models.DecimalField(max_digits=12, decimal_places=2)
    confidence_score = models.FloatField()
    model_version    = models.CharField(max_length=50, default='v1.0')
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'prediction'
        verbose_name = 'Prédiction'
        verbose_name_plural = 'Prédictions'
        ordering = ['-created_at']

    def __str__(self):
        return f"Prédiction {self.property.title} : {self.predicted_price} DT"

    def confidence_percent(self):
        return round(self.confidence_score * 100)

    def confidence_label(self):
        if self.confidence_score > 0.8:
            return ('success', 'Très fiable')
        elif self.confidence_score > 0.6:
            return ('warning', 'Fiable')
        return ('danger', 'Moyennement fiable')


# ─────────────────────────────────────────────
#  Favoris
# ─────────────────────────────────────────────

class Favorite(models.Model):
    user       = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    property   = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favorite'
        verbose_name = 'Favori'
        verbose_name_plural = 'Favoris'
        unique_together = ['user', 'property']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} ♥ {self.property.title}"


# ─────────────────────────────────────────────
#  Messagerie
# ─────────────────────────────────────────────

class Message(models.Model):
    sender     = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient  = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    property   = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    subject    = models.CharField(max_length=200)
    content    = models.TextField()
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'message'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"De {self.sender.email} → {self.recipient.email} : {self.subject}"


# ─────────────────────────────────────────────
#  Évaluations
# ─────────────────────────────────────────────

class PropertyRating(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user       = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ratings')
    property   = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='ratings')
    rating     = models.IntegerField(choices=RATING_CHOICES)
    comment    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'propertyrating'
        verbose_name = 'Évaluation'
        verbose_name_plural = 'Évaluations'
        unique_together = ['user', 'property']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.property.title} — {self.rating}/5 par {self.user.email}"


# ─────────────────────────────────────────────
#  Historique de recherche
# ─────────────────────────────────────────────

class SearchHistory(models.Model):
    user          = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='search_history')
    query_params  = models.JSONField(default=dict)
    results_count = models.IntegerField(default=0)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'searchhistory'
        verbose_name = 'Historique de recherche'
        verbose_name_plural = 'Historiques de recherche'
        ordering = ['-created_at']

    def __str__(self):
        return f"Recherche de {self.user.email} — {self.created_at:%d/%m/%Y}"


# ─────────────────────────────────────────────
#  Notifications
# ─────────────────────────────────────────────

class Notification(models.Model):
    TYPE_CHOICES = [
        ('message',         'Nouveau message'),
        ('favorite',        'Bien ajouté aux favoris'),
        ('rating',          'Nouvelle évaluation'),
        ('property_update', 'Mise à jour de bien'),
        ('system',          'Notification système'),
    ]

    user              = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title             = models.CharField(max_length=200)
    message           = models.TextField()
    is_read           = models.BooleanField(default=False)
    created_at        = models.DateTimeField(auto_now_add=True)
    related_property  = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')

    class Meta:
        db_table = 'notification'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} — {self.title}"
