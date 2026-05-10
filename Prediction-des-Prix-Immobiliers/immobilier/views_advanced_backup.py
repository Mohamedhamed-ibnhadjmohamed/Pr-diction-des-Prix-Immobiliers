from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import Avg, Count, Q
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from .models import (
    Property, Favorite, Message, PropertyRating, SearchHistory, 
    Notification, UserReview, Report, PropertyComparison, Document, 
    Recommendation, CustomUser
)
import json
import csv

@login_required
def notifications_list(request):
    """Liste des notifications de l'utilisateur"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    
    # Pagination
    paginator = Paginator(notifications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'immobilier/advanced/notifications.html', {
        'notifications': page_obj,
        'unread_count': unread_count
    })

@login_required
@require_POST
def mark_notification_read(request, notification_id):
    """Marquer une notification comme lue"""
    notification = get_object_or_404(Notification, pk=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})

@login_required
@require_POST
def mark_all_notifications_read(request):
    """Marquer toutes les notifications comme lues"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})

def create_notification(user, notification_type, title, message, property=None, sender=None):
    """Créer une notification (utilité interne)"""
    Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        property=property,
        sender=sender
    )

@login_required
def review_user(request, user_id):
    """Évaluer un utilisateur"""
    reviewed_user = get_object_or_404(CustomUser, pk=user_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        
        review, created = UserReview.objects.update_or_create(
            reviewer=request.user,
            reviewed_user=reviewed_user,
            defaults={'rating': rating, 'comment': comment}
        )
        
        if not created:
            review.rating = rating
            review.comment = comment
            review.save()
        
        # Créer une notification pour l'utilisateur évalué
        create_notification(
            reviewed_user,
            'rating',
            'Nouvel avis reçu',
            f'Vous avez reçu un nouvel avis de {request.user.get_full_name() or request.user.email}',
            sender=request.user
        )
        
        messages.success(request, "Votre avis a été enregistré!")
        return redirect('immobilier:user_profile', pk=user_id)
    
    # Vérifier si l'utilisateur a déjà évalué
    existing_review = UserReview.objects.filter(
        reviewer=request.user,
        reviewed_user=reviewed_user
    ).first()
    
    return render(request, 'immobilier/advanced/review_user.html', {
        'reviewed_user': reviewed_user,
        'existing_review': existing_review
    })

@login_required
def user_profile(request, user_id):
    """Profil public d'un utilisateur"""
    user = get_object_or_404(CustomUser, pk=user_id)
    
    # Statistiques de l'utilisateur
    properties_count = Property.objects.filter(created_by=user).count()
    reviews_given = UserReview.objects.filter(reviewer=user).count()
    reviews_received = UserReview.objects.filter(reviewed_user=user)
    avg_rating = reviews_received.aggregate(avg=Avg('rating'))['avg'] or 0
    
    # Propriétés de l'utilisateur
    properties = Property.objects.filter(created_by=user).order_by('-created_at')[:6]
    
    return render(request, 'immobilier/advanced/user_profile.html', {
        'profile_user': user,
        'properties_count': properties_count,
        'reviews_given': reviews_given,
        'reviews_received': reviews_received.count(),
        'avg_rating': avg_rating,
        'properties': properties,
        'can_review': request.user != user and not UserReview.objects.filter(
            reviewer=request.user, reviewed_user=user
        ).exists()
    })

@login_required
def report_content(request):
    """Signaler du contenu"""
    if request.method == 'POST':
        report_type = request.POST.get('report_type')
        reason = request.POST.get('reason')
        description = request.POST.get('description')
        
        report = Report.objects.create(
            reporter=request.user,
            report_type=report_type,
            reason=reason,
            description=description
        )
        
        # Ajouter les objets liés
        if report_type == 'property' and 'property_id' in request.POST:
            report.property = get_object_or_404(Property, pk=request.POST['property_id'])
        elif report_type == 'user' and 'user_id' in request.POST:
            report.user = get_object_or_404(CustomUser, pk=request.POST['user_id'])
        elif report_type == 'message' and 'message_id' in request.POST:
            report.message = get_object_or_404(Message, pk=request.POST['message_id'])
        
        report.save()
        
        messages.success(request, "Votre signalement a été enregistré. Nous allons l'examiner rapidement.")
        return redirect(request.META.get('HTTP_REFERER', 'immobilier:home'))
    
    return render(request, 'immobilier/advanced/report.html')

@login_required
def create_comparison(request):
    """Créer une comparaison de biens"""
    if request.method == 'POST':
        name = request.POST.get('name')
        property_ids = request.POST.getlist('properties')
        
        comparison = PropertyComparison.objects.create(
            user=request.user,
            name=name
        )
        comparison.properties.set(property_ids)
        
        messages.success(request, f"Comparaison '{name}' créée avec succès!")
        return redirect('immobilier:comparison_detail', pk=comparison.pk)
    
    return render(request, 'immobilier/advanced/create_comparison.html')

@login_required
def comparison_detail(request, pk):
    """Détail d'une comparaison"""
    comparison = get_object_or_404(PropertyComparison, pk=pk, user=request.user)
    properties = comparison.properties.all()
    
    return render(request, 'immobilier/advanced/comparison_detail.html', {
        'comparison': comparison,
        'properties': properties
    })

@login_required
def comparisons_list(request):
    """Liste des comparaisons de l'utilisateur"""
    comparisons = PropertyComparison.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'immobilier/advanced/comparisons.html', {
        'comparisons': comparisons
    })

@login_required
def upload_document(request):
    """Uploader un document"""
    if request.method == 'POST':
        title = request.POST.get('title')
        document_type = request.POST.get('document_type')
        description = request.POST.get('description', '')
        file = request.FILES.get('file')
        property_id = request.POST.get('property_id')
        
        document = Document.objects.create(
            user=request.user,
            title=title,
            document_type=document_type,
            file=file,
            description=description
        )
        
        if property_id:
            document.property = get_object_or_404(Property, pk=property_id)
            document.save()
        
        messages.success(request, f"Document '{title}' uploadé avec succès!")
        return redirect('immobilier:documents_list')
    
    return render(request, 'immobilier/advanced/upload_document.html')

@login_required
def documents_list(request):
    """Liste des documents de l'utilisateur"""
    documents = Document.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'immobilier/advanced/documents.html', {
        'documents': documents
    })

@login_required
def recommendations_list(request):
    """Liste des recommandations pour l'utilisateur"""
    recommendations = Recommendation.objects.filter(user=request.user).order_by('-score', '-created_at')
    
    return render(request, 'immobilier/advanced/recommendations.html', {
        'recommendations': recommendations
    })

def generate_recommendations(user):
    """Générer des recommandations pour un utilisateur (utilité interne)"""
    # Basé sur l'historique des favoris et des recherches
    favorite_properties = Favorite.objects.filter(user=user).values_list('property', flat=True)
    recent_searches = SearchHistory.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Logique simple de recommandation basée sur les favoris
    if favorite_properties:
        # Trouver des propriétés similaires
        favorite_property = Property.objects.filter(pk__in=favorite_properties).first()
        if favorite_property:
            similar_properties = Property.objects.filter(
                Q(city=favorite_property.city) |
                Q(property_type=favorite_property.property_type) |
                Q(price__range=(
                    favorite_property.price * 0.8,
                    favorite_property.price * 1.2
                )
            ).exclude(
                pk__in=favorite_properties,
                created_by=user
            )[:3]
            
            for property in similar_properties:
                score = 0.8  # Score de base
                if property.city == favorite_property.city:
                    score += 0.1
                if property.property_type == favorite_property.property_type:
                    score += 0.1
                
                Recommendation.objects.update_or_create(
                    user=user,
                    property=property,
                    defaults={
                        'score': score,
                        'reason': f'Similaire à vos favoris dans {property.city}'
                    }
                )

@login_required
def admin_notifications(request):
    """Tableau de bord des notifications (admin/agent uniquement)"""
    if not (request.user.is_agent or request.user.is_staff):
        messages.error(request, 'Accès réservé aux agents et administrateurs.')
        return redirect('immobilier:home')
    
    # Statistiques des notifications
    total_notifications = Notification.objects.count()
    unread_notifications = Notification.objects.filter(is_read=False).count()
    
    # Notifications par type
    notifications_by_type = Notification.objects.values('notification_type').annotate(
        count=Count('notification_type')
    ).order_by('-count')
    
    # Notifications récentes
    recent_notifications = Notification.objects.order_by('-created_at')[:10]
    
    return render(request, 'immobilier/advanced/admin_notifications.html', {
        'total_notifications': total_notifications,
        'unread_notifications': unread_notifications,
        'notifications_by_type': notifications_by_type,
        'recent_notifications': recent_notifications
    })

@login_required
def admin_reports(request):
    """Tableau de bord des signalements (admin/agent uniquement)"""
    if not (request.user.is_agent or request.user.is_staff):
        messages.error(request, 'Accès réservé aux agents et administrateurs.')
        return redirect('immobilier:home')
    
    # Statistiques des signalements
    total_reports = Report.objects.count()
    unresolved_reports = Report.objects.filter(is_resolved=False).count()
    
    # Signalements par type
    reports_by_type = Report.objects.values('report_type').annotate(
        count=Count('report_type')
    ).order_by('-count')
    
    # Signalements récents
    recent_reports = Report.objects.order_by('-created_at')[:10]
    
    return render(request, 'immobilier/advanced/admin_reports.html', {
        'total_reports': total_reports,
        'unresolved_reports': unresolved_reports,
        'reports_by_type': reports_by_type,
        'recent_reports': recent_reports
    })

@login_required
def export_data(request):
    """Exporter les données de l'utilisateur"""
    export_type = request.GET.get('type', 'properties')
    
    if export_type == 'properties':
        properties = Property.objects.filter(created_by=request.user)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="properties.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Titre', 'Type', 'Ville', 'Surface', 'Pièces', 'Prix', 'Date création'])
        
        for prop in properties:
            writer.writerow([
                prop.title,
                prop.get_property_type_display(),
                prop.city,
                prop.surface,
                prop.rooms,
                prop.price,
                prop.created_at.strftime('%d/%m/%Y')
            ])
        
        return response
    
    elif export_type == 'favorites':
        favorites = Favorite.objects.filter(user=request.user).select_related('property')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="favorites.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Titre', 'Type', 'Ville', 'Surface', 'Prix', 'Date ajout'])
        
        for fav in favorites:
            writer.writerow([
                fav.property.title,
                fav.property.get_property_type_display(),
                fav.property.city,
                fav.property.surface,
                fav.property.price,
                fav.created_at.strftime('%d/%m/%Y')
            ])
        
        return response
    
    messages.error(request, "Type d'export non valide")
    return redirect('immobilier:home')
