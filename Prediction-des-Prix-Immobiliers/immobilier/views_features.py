from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import models
from django.db.models import Avg, Count
from .models import Property, Favorite, Message, PropertyRating, SearchHistory, CustomUser
import json

@login_required
def add_to_favorites(request, property_id):
    """Ajouter une propriété aux favoris"""
    property = get_object_or_404(Property, pk=property_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, property=property)
    
    if created:
        messages.success(request, f"{property.title} a été ajouté à vos favoris!")
    else:
        messages.info(request, f"{property.title} est déjà dans vos favoris!")
    
    return redirect('immobilier:property_detail', pk=property_id)

@login_required
def remove_from_favorites(request, property_id):
    """Retirer une propriété des favoris"""
    property = get_object_or_404(Property, pk=property_id)
    try:
        favorite = Favorite.objects.get(user=request.user, property=property_id)
        favorite.delete()
        messages.success(request, f"{property.title} a été retiré de vos favoris!")
    except Favorite.DoesNotExist:
        messages.error(request, "Ce bien n'est pas dans vos favoris!")
    
    return redirect('immobilier:property_detail', pk=property_id)

@login_required
def favorites_list(request):
    """Liste des propriétés favorites"""
    favorites = Favorite.objects.filter(user=request.user).select_related('property')
    return render(request, 'immobilier/features/favorites.html', {'favorites': favorites})

@login_required
def send_message(request, property_id=None):
    """Envoyer un message à un agent/vendeur"""
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        
        recipient = get_object_or_404(CustomUser, pk=recipient_id)
        property = Property.objects.get(pk=property_id) if property_id else None
        
        Message.objects.create(
            sender=request.user,
            recipient=recipient,
            property=property,
            subject=subject,
            content=content
        )
        
        messages.success(request, "Message envoyé avec succès!")
        return redirect('immobilier:property_detail', pk=property_id) if property_id else redirect('immobilier:home')
    
    # Pour GET, afficher le formulaire
    recipient_id = request.GET.get('recipient')
    recipient = get_object_or_404(CustomUser, pk=recipient_id) if recipient_id else None
    property = Property.objects.get(pk=property_id) if property_id else None
    
    return render(request, 'immobilier/features/send_message.html', {
        'recipient': recipient,
        'property': property
    })

@login_required
def inbox(request):
    """Boîte de réception des messages"""
    messages_received = Message.objects.filter(recipient=request.user).order_by('-created_at')
    unread_count = messages_received.filter(is_read=False).count()
    
    return render(request, 'immobilier/features/inbox.html', {
        'messages': messages_received,
        'unread_count': unread_count
    })

@login_required
def mark_message_read(request, message_id):
    """Marquer un message comme lu"""
    message = get_object_or_404(Message, pk=message_id, recipient=request.user)
    message.is_read = True
    message.save()
    return JsonResponse({'status': 'success'})

@login_required
def rate_property(request, property_id):
    """Évaluer une propriété"""
    property = get_object_or_404(Property, pk=property_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        
        rating_obj, created = PropertyRating.objects.update_or_create(
            user=request.user,
            property=property,
            defaults={'rating': rating, 'comment': comment}
        )
        
        if not created:
            rating_obj.rating = rating
            rating_obj.comment = comment
            rating_obj.save()
        
        messages.success(request, "Votre évaluation a été enregistrée!")
        return redirect('immobilier:property_detail', pk=property_id)
    
    return render(request, 'immobilier/features/rate_property.html', {'property': property})

def advanced_search(request):
    """Recherche avancée avec sauvegarde"""
    context = {}
    
    if request.method == 'GET':
        # Sauvegarder la recherche
        query_params = dict(request.GET.items())
        if query_params and request.user.is_authenticated:
            # Compter les résultats pour cette recherche
            properties = Property.objects.all()
            
            # Appliquer les filtres
            if 'property_type' in query_params:
                properties = properties.filter(property_type=query_params['property_type'])
            if 'min_price' in query_params:
                properties = properties.filter(price__gte=query_params['min_price'])
            if 'max_price' in query_params:
                properties = properties.filter(price__lte=query_params['max_price'])
            if 'min_surface' in query_params:
                properties = properties.filter(surface__gte=query_params['min_surface'])
            if 'max_surface' in query_params:
                properties = properties.filter(surface__lte=query_params['max_surface'])
            if 'city' in query_params:
                properties = properties.filter(city__icontains=query_params['city'])
            if 'rooms' in query_params:
                properties = properties.filter(rooms=query_params['rooms'])
            if 'bedrooms' in query_params:
                properties = properties.filter(bedrooms=query_params['bedrooms'])
            
            # Sauvegarder l'historique
            SearchHistory.objects.create(
                user=request.user,
                query_params=query_params,
                results_count=properties.count()
            )
            
            # Ajouter les statistiques au contexte
            context.update({
                'total_properties': properties.count(),
                'avg_price': properties.aggregate(avg=models.Avg('price'))['avg'] or 0,
                'avg_surface': properties.aggregate(avg=models.Avg('surface'))['avg'] or 0,
            })
        
        # Ajouter l'historique de recherche si l'utilisateur est connecté
        if request.user.is_authenticated:
            context['search_history'] = SearchHistory.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    return render(request, 'immobilier/features/advanced_search.html', context)

@login_required
def search_history(request):
    """Historique des recherches"""
    history = SearchHistory.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'immobilier/features/search_history.html', {'history': history})

@login_required
def statistics(request):
    """Statistiques pour l'utilisateur connecté"""
    if request.user.is_agent:
        # Statistiques pour les agents
        properties = Property.objects.filter(created_by=request.user)
        total_properties = properties.count()
        total_value = properties.aggregate(total=models.Sum('price'))['total'] or 0
        avg_price = properties.aggregate(avg=models.Avg('price'))['avg'] or 0
        
        # Évaluations reçues
        ratings = PropertyRating.objects.filter(property__in=properties)
        avg_rating = ratings.aggregate(avg=models.Avg('rating'))['avg'] or 0
        
        context = {
            'total_properties': total_properties,
            'total_value': total_value,
            'avg_price': avg_price,
            'avg_rating': avg_rating,
            'recent_properties': properties.order_by('-created_at')[:5],
            'type_stats': properties.values('property_type').annotate(count=Count('property_type'))
        }
    else:
        # Statistiques pour les acheteurs/vendeurs
        favorites = Favorite.objects.filter(user=request.user)
        ratings = PropertyRating.objects.filter(user=request.user)
        searches = SearchHistory.objects.filter(user=request.user)
        
        context = {
            'total_favorites': favorites.count(),
            'total_ratings': ratings.count(),
            'total_searches': searches.count(),
            'recent_favorites': favorites.select_related('property').order_by('-created_at')[:5],
            'recent_searches': searches.order_by('-created_at')[:5],
            'avg_rating_given': ratings.aggregate(avg=models.Avg('rating'))['avg'] or 0
        }
    
    return render(request, 'immobilier/features/statistics.html', context)

@login_required
def export_properties(request):
    """Exporter les propriétés en CSV"""
    import csv
    from django.http import HttpResponse
    
    if request.user.is_agent:
        properties = Property.objects.filter(created_by=request.user)
    else:
        properties = Property.objects.filter(created_by=request.user)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="properties.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Titre', 'Type', 'Ville', 'Surface', 'Pièces', 'Chambres', 'Prix', 'Date création'])
    
    for prop in properties:
        writer.writerow([
            prop.title,
            prop.get_property_type_display(),
            prop.city,
            prop.surface,
            prop.rooms,
            prop.bedrooms,
            prop.price,
            prop.created_at.strftime('%d/%m/%Y')
        ])
    
    return response
