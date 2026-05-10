from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Property, PropertyFeature, Prediction, CustomUser, UserProfile

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'city', 'surface', 'rooms', 'price', 'created_at')
    list_filter = ('property_type', 'city', 'created_at')
    search_fields = ('title', 'city', 'address')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'property_type', 'price', 'description')
        }),
        ('Localisation', {
            'fields': ('address', 'city', 'postal_code')
        }),
        ('Caractéristiques', {
            'fields': ('surface', 'rooms', 'bedrooms', 'bathrooms')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(PropertyFeature)
class PropertyFeatureAdmin(admin.ModelAdmin):
    list_display = ('property', 'has_garden', 'has_pool', 'has_garage', 'construction_year', 'energy_efficiency')
    list_filter = ('has_garden', 'has_pool', 'has_garage', 'energy_efficiency')
    search_fields = ('property__title', 'property__city')

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('property', 'predicted_price', 'confidence_score', 'model_version', 'created_at')
    list_filter = ('model_version', 'created_at')
    search_fields = ('property__title', 'property__city')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_verified', 'date_joined')
    list_filter = ('role', 'is_verified', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Rôle et permissions', {'fields': ('role', 'is_verified', 'is_staff', 'is_active', 'groups')}),
        ('Profil', {'fields': ('profile_picture', 'bio')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'license_number')
    search_fields = ('user__username', 'user__email', 'company')
    list_filter = ('company',)
