from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Q, Count
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from .models import (
    Property, PropertyFeature, Favorite, Message, PropertyRating, 
    SearchHistory, Notification, UserReview, Report, PropertyComparison, 
    Document, Recommendation, CustomUser
)
from .forms import PropertyForm, PropertyFeatureForm, PredictionForm
from .forms_complete import (
    MessageForm, PropertyRatingForm, PropertySearchForm, UserReviewForm, 
    ReportForm, PropertyComparisonForm, DocumentForm, CustomUserUpdateForm
)
import random
import numpy as np
import csv

@login_required
def dashboard_view(request):
    """Tableau de bord principal selon le rôle de l'utilisateur"""
    user = request.user
    
    if user.is_agent:
        return agent_dashboard(request)
    elif user.is_vendeur:
        return vendeur_dashboard(request)
    else:
        return acheteur_dashboard(request)

def agent_dashboard(request):
    """Tableau de bord pour les agents immobiliers"""
    # Statistiques de l'agent
    my_properties = Property.objects.filter(created_by=request.user)
    total_properties = my_properties.count()
    avg_price = my_properties.aggregate(Avg('price'))['price__avg'] or 0
    
    # Messages non lus
    unread_messages = Message.objects.filter(recipient=request.user, is_read=False).count()
    
    # Propriétés récentes
    recent_properties = my_properties.order_by('-created_at')[:5]
    
    # Évaluations récentes
    recent_ratings = PropertyRating.objects.filter(property__created_by=request.user).order_by('-created_at')[:5]
    
    context = {
        'total_properties': total_properties,
        'avg_price': avg_price,
        'unread_messages': unread_messages,
        'recent_properties': recent_properties,
        'recent_ratings': recent_ratings,
    }
    return render(request, 'immobilier/dashboard/agent.html', context)

def vendeur_dashboard(request):
    """Tableau de bord pour les vendeurs"""
    # Propriétés du vendeur
    my_properties = Property.objects.filter(created_by=request.user)
    
    # Statistiques des vues
    total_views = sum(prop.views_count if hasattr(prop, 'views_count') else 0 for prop in my_properties)
    
    # Favoris reçus
    total_favorites = Favorite.objects.filter(property__created_by=request.user).count()
    
    # Messages reçus
    unread_messages = Message.objects.filter(recipient=request.user, is_read=False).count()
    
    context = {
        'my_properties': my_properties.order_by('-created_at')[:5],
        'total_properties': my_properties.count(),
        'total_views': total_views,
        'total_favorites': total_favorites,
        'unread_messages': unread_messages,
    }
    return render(request, 'immobilier/dashboard/vendeur.html', context)

def acheteur_dashboard(request):
    """Tableau de bord pour les acheteurs"""
    # Favoris de l'acheteur
    favorites = Favorite.objects.filter(user=request.user)
    
    # Recherches récentes
    recent_searches = SearchHistory.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Messages envoyés
    sent_messages = Message.objects.filter(sender=request.user).order_by('-created_at')[:5]
    
    # Recommandations
    recommendations = Recommendation.objects.filter(user=request.user).order_by('-score')[:5]
    
    context = {
        'favorites': favorites.order_by('-created_at')[:5],
        'recent_searches': recent_searches,
        'sent_messages': sent_messages,
        'recommendations': recommendations,
    }
    return render(request, 'immobilier/dashboard/acheteur.html', context)

@login_required
def send_message(request, property_id=None):
    """Envoyer un message à un propriétaire"""
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            
            # Si property_id est fourni, définir le destinataire comme le propriétaire
            if property_id:
                property = get_object_or_404(Property, pk=property_id)
                message.property = property
                if property.created_by:
                    message.recipient = property.created_by
                else:
                    messages.error(request, "Ce bien n'a pas de propriétaire défini.")
                    return redirect('immobilier:property_detail', pk=property_id)
            
            message.save()
            
            # Créer une notification pour le destinataire
            Notification.objects.create(
                user=message.recipient,
                notification_type='message',
                title=f"Nouveau message de {request.user.get_full_name() or request.user.email}",
                message=f"Vous avez reçu un nouveau message: {message.subject}",
                property=message.property,
                sender=request.user
            )
            
            messages.success(request, "Message envoyé avec succès!")
            return redirect('immobilier:inbox')
    else:
        initial_data = {}
        if property_id:
            property = get_object_or_404(Property, pk=property_id)
            initial_data['property'] = property
            if property.created_by:
                initial_data['recipient'] = property.created_by
        
        form = MessageForm(initial=initial_data)
    
    return render(request, 'immobilier/messages/send_message.html', {
        'form': form,
        'property_id': property_id
    })

@login_required
def inbox(request):
    """Boîte de réception des messages"""
    # Messages reçus
    received_messages = Message.objects.filter(recipient=request.user).order_by('-created_at')
    
    # Messages envoyés
    sent_messages = Message.objects.filter(sender=request.user).order_by('-created_at')
    
    # Pagination pour les messages reçus
    paginator = Paginator(received_messages, 20)
    page_number = request.GET.get('page')
    received_page_obj = paginator.get_page(page_number)
    
    context = {
        'received_messages': received_page_obj,
        'sent_messages': sent_messages[:10],  # Limiter les messages envoyés affichés
        'unread_count': received_messages.filter(is_read=False).count(),
    }
    return render(request, 'immobilier/messages/inbox.html', context)

@login_required
@require_POST
def mark_message_read(request, message_id):
    """Marquer un message comme lu"""
    message = get_object_or_404(Message, pk=message_id, recipient=request.user)
    message.is_read = True
    message.save()
    return JsonResponse({'status': 'success'})

@login_required
def favorites_list(request):
    """Liste des favoris de l'utilisateur"""
    favorites = Favorite.objects.filter(user=request.user).select_related('property')
    
    # Pagination
    paginator = Paginator(favorites, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'immobilier/favorites/list.html', context)

@login_required
@require_POST
def add_to_favorites(request, property_id):
    """Ajouter un bien aux favoris"""
    property = get_object_or_404(Property, pk=property_id)
    
    # Vérifier si déjà en favoris
    if Favorite.objects.filter(user=request.user, property=property).exists():
        messages.info(request, "Ce bien est déjà dans vos favoris.")
    else:
        Favorite.objects.create(user=request.user, property=property)
        
        # Notification pour le propriétaire
        if property.created_by and property.created_by != request.user:
            Notification.objects.create(
                user=property.created_by,
                notification_type='favorite',
                title="Nouveau favori",
                message=f"{request.user.get_full_name() or request.user.email} a ajouté votre bien '{property.title}' à ses favoris.",
                property=property,
                sender=request.user
            )
        
        messages.success(request, "Bien ajouté aux favoris!")
    
    return redirect('immobilier:property_detail', pk=property_id)

@login_required
@require_POST
def remove_from_favorites(request, property_id):
    """Retirer un bien des favoris"""
    property = get_object_or_404(Property, pk=property_id)
    
    try:
        favorite = Favorite.objects.get(user=request.user, property=property)
        favorite.delete()
        messages.success(request, "Bien retiré des favoris!")
    except Favorite.DoesNotExist:
        messages.error(request, "Ce bien n'est pas dans vos favoris.")
    
    return redirect('immobilier:favorites_list')

@login_required
def rate_property(request, property_id):
    """Évaluer une propriété"""
    property = get_object_or_404(Property, pk=property_id)
    
    if request.method == 'POST':
        form = PropertyRatingForm(request.POST)
        if form.is_valid():
            rating, created = PropertyRating.objects.update_or_create(
                user=request.user,
                property=property,
                defaults=form.cleaned_data
            )
            
            # Notification pour le propriétaire
            if property.created_by and property.created_by != request.user:
                Notification.objects.create(
                    user=property.created_by,
                    notification_type='rating',
                    title="Nouvelle évaluation",
                    message=f"Votre bien '{property.title}' a reçu une nouvelle évaluation de {rating.rating}/5 étoiles.",
                    property=property,
                    sender=request.user
                )
            
            action = "ajoutée" if created else "mise à jour"
            messages.success(request, f"Évaluation {action} avec succès!")
            return redirect('immobilier:property_detail', pk=property_id)
    else:
        # Vérifier si l'utilisateur a déjà évalué
        existing_rating = PropertyRating.objects.filter(user=request.user, property=property).first()
        form = PropertyRatingForm(instance=existing_rating)
    
    return render(request, 'immobilier/ratings/rate_property.html', {
        'form': form,
        'property': property,
    })

def advanced_search(request):
    """Recherche avancée de propriétés"""
    if request.method == 'GET':
        form = PropertySearchForm(request.GET)
        if form.is_valid():
            # Construire la requête
            properties = Property.objects.all()
            
            # Appliquer les filtres
            property_type = form.cleaned_data.get('property_type')
            city = form.cleaned_data.get('city')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            min_surface = form.cleaned_data.get('min_surface')
            rooms = form.cleaned_data.get('rooms')
            
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
            if rooms:
                properties = properties.filter(rooms__gte=rooms)
            
            # Sauvegarder la recherche
            if request.user.is_authenticated:
                SearchHistory.objects.create(
                    user=request.user,
                    query_params=form.cleaned_data,
                    results_count=properties.count()
                )
            
            # Pagination
            paginator = Paginator(properties, 12)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            context = {
                'form': form,
                'page_obj': page_obj,
                'search_performed': True,
                'results_count': properties.count(),
            }
        else:
            context = {'form': form}
    else:
        form = PropertySearchForm()
        context = {'form': form}
    
    return render(request, 'immobilier/search/advanced_search.html', context)

@login_required
def search_history(request):
    """Historique des recherches de l'utilisateur"""
    searches = SearchHistory.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'searches': searches,
    }
    return render(request, 'immobilier/search/history.html', context)

def statistics_view(request):
    """Statistiques globales de l'application"""
    # Statistiques générales
    total_properties = Property.objects.count()
    total_users = CustomUser.objects.count()
    total_favorites = Favorite.objects.count()
    total_ratings = PropertyRating.objects.count()
    
    # Prix moyen par type de bien
    avg_price_by_type = Property.objects.values('property_type').annotate(
        avg_price=Avg('price'),
        count=Count('id')
    ).order_by('-avg_price')
    
    # Top 10 des villes avec le plus de biens
    top_cities = Property.objects.values('city').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Distribution des types de biens
    property_types = Property.objects.values('property_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'total_properties': total_properties,
        'total_users': total_users,
        'total_favorites': total_favorites,
        'total_ratings': total_ratings,
        'avg_price_by_type': avg_price_by_type,
        'top_cities': top_cities,
        'property_types': property_types,
    }
    return render(request, 'immobilier/statistics/global.html', context)

@login_required
def export_properties(request):
    """Exporter les propriétés au format CSV"""
    if request.user.role not in ['agent', 'admin']:
        return HttpResponse("Accès non autorisé", status=403)
    
    # Propriétés à exporter (toutes ou seulement celles de l'utilisateur)
    if request.user.role == 'admin':
        properties = Property.objects.all()
    else:
        properties = Property.objects.filter(created_by=request.user)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="properties.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Titre', 'Type', 'Ville', 'Surface', 'Pièces', 'Chambres', 
        'Salle de bains', 'Prix', 'Description', 'Date création'
    ])
    
    for prop in properties:
        writer.writerow([
            prop.title,
            prop.get_property_type_display(),
            prop.city,
            prop.surface,
            prop.rooms,
            prop.bedrooms,
            prop.bathrooms,
            prop.price,
            prop.description,
            prop.created_at.strftime('%d/%m/%Y')
        ])
    
    return response
