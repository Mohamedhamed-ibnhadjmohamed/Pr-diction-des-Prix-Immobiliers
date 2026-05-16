from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, UserProfile, Property, PropertyFeature,
    Prediction, Favorite, Message, PropertyRating, Notification,
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model       = CustomUser
    list_display  = ('email', 'first_name', 'last_name', 'role', 'is_verified', 'is_active')
    list_filter   = ('role', 'is_verified', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering      = ('email',)
    fieldsets = (
        (None,          {'fields': ('email', 'password')}),
        ('Informations', {'fields': ('first_name', 'last_name', 'phone', 'bio', 'profile_picture')}),
        ('Rôle',        {'fields': ('role', 'is_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates',       {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': (
            'email', 'first_name', 'last_name', 'role', 'password1', 'password2')}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'license_number')


class PropertyFeatureInline(admin.StackedInline):
    model = PropertyFeature
    extra = 0


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display  = ('title', 'property_type', 'city', 'surface', 'price', 'created_by', 'created_at')
    list_filter   = ('property_type', 'city')
    search_fields = ('title', 'city', 'address')
    inlines       = [PropertyFeatureInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('property', 'predicted_price', 'confidence_score', 'model_version', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'created_at')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'is_read', 'created_at')
    list_filter  = ('is_read',)


@admin.register(PropertyRating)
class PropertyRatingAdmin(admin.ModelAdmin):
    list_display = ('property', 'user', 'rating', 'created_at')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter  = ('notification_type', 'is_read')
