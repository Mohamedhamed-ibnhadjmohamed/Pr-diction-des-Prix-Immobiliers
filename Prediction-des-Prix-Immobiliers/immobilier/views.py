import random
import csv
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils import timezone

from .models import (
    CustomUser, UserProfile, Property, PropertyFeature,
    Prediction, Favorite, Message, PropertyRating,
    SearchHistory, Notification,
)
from .forms import (
    RegisterForm, LoginForm, UserUpdateForm, UserProfileForm,
    PropertyForm, PropertyFeatureForm, PredictionForm,
    MessageForm, PropertyRatingForm, SearchForm,
)


# ═══════════════════════════════════════════════════════════════════════════
#  PAGES PUBLIQUES
# ═══════════════════════════════════════════════════════════════════════════

def home(request):
    total   = Property.objects.count()
    avg     = Property.objects.aggregate(Avg('price'))['price__avg'] or 0
    recents = Property.objects.select_related('created_by').order_by('-created_at')[:6]
    return render(request, 'immobilier/home.html', {
        'total_properties': total,
        'avg_price':        avg,
        'recent_properties': recents,
    })


def property_list(request):
    qs = Property.objects.select_related('created_by').all()

    q         = request.GET.get('q', '').strip()
    ptype     = request.GET.get('type', '')
    city      = request.GET.get('city', '').strip()
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    min_surf  = request.GET.get('min_surface', '')

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(city__icontains=q) | Q(description__icontains=q))
    if ptype:
        qs = qs.filter(property_type=ptype)
    if city:
        qs = qs.filter(city__icontains=city)
    if min_price:
        qs = qs.filter(price__gte=min_price)
    if max_price:
        qs = qs.filter(price__lte=max_price)
    if min_surf:
        qs = qs.filter(surface__gte=min_surf)

    paginator = Paginator(qs, 12)
    page_obj  = paginator.get_page(request.GET.get('page'))

    cities = Property.objects.values_list('city', flat=True).distinct().order_by('city')
    return render(request, 'immobilier/property/list.html', {
        'page_obj':       page_obj,
        'property_types': Property.TYPE_CHOICES,
        'cities':         cities,
        'filters': {'q': q, 'type': ptype, 'city': city,
                    'min_price': min_price, 'max_price': max_price, 'min_surface': min_surf},
    })


def property_detail(request, pk):
    prop     = get_object_or_404(Property, pk=pk)
    features = getattr(prop, 'features', None)
    ratings  = prop.ratings.select_related('user').order_by('-created_at')
    similar  = Property.objects.filter(
        property_type=prop.property_type, city=prop.city
    ).exclude(pk=pk)[:3]

    user_rating = None
    is_favorite = False
    if request.user.is_authenticated:
        user_rating = ratings.filter(user=request.user).first()
        is_favorite = Favorite.objects.filter(user=request.user, property=prop).exists()

    return render(request, 'immobilier/property/detail.html', {
        'property':     prop,
        'features':     features,
        'ratings':      ratings,
        'similar':      similar,
        'user_rating':  user_rating,
        'is_favorite':  is_favorite,
    })


def advanced_search(request):
    form = SearchForm(request.GET or None)
    qs   = Property.objects.all()

    if form.is_valid():
        d = form.cleaned_data
        if d.get('keyword'):
            qs = qs.filter(Q(title__icontains=d['keyword']) | Q(city__icontains=d['keyword']))
        if d.get('property_type'):
            qs = qs.filter(property_type=d['property_type'])
        if d.get('city'):
            qs = qs.filter(city__icontains=d['city'])
        if d.get('min_price') is not None:
            qs = qs.filter(price__gte=d['min_price'])
        if d.get('max_price') is not None:
            qs = qs.filter(price__lte=d['max_price'])
        if d.get('min_surface') is not None:
            qs = qs.filter(surface__gte=d['min_surface'])
        if d.get('max_surface') is not None:
            qs = qs.filter(surface__lte=d['max_surface'])
        if d.get('min_rooms') is not None:
            qs = qs.filter(rooms__gte=d['min_rooms'])
        if d.get('has_garden'):
            qs = qs.filter(features__has_garden=True)
        if d.get('has_pool'):
            qs = qs.filter(features__has_pool=True)
        if d.get('has_garage'):
            qs = qs.filter(features__has_garage=True)

        # Sauvegarder l'historique si authentifié
        if request.user.is_authenticated and request.GET:
            SearchHistory.objects.create(
                user=request.user,
                query_params=dict(request.GET),
                results_count=qs.count(),
            )

    paginator = Paginator(qs, 12)
    page_obj  = paginator.get_page(request.GET.get('page'))
    return render(request, 'immobilier/features/advanced_search.html', {
        'form':     form,
        'page_obj': page_obj,
        'count':    qs.count(),
    })


# ═══════════════════════════════════════════════════════════════════════════
#  PRÉDICTION
# ═══════════════════════════════════════════════════════════════════════════

def _simulate_price(data):
    """Estimation statistique simple (sans ML)."""
    base = {
        'appartement': 2500,
        'maison':      3000,
        'studio':      2000,
        'villa':       4500,
        'terrain':     400,
    }.get(data['property_type'], 2500)

    price = base * data['surface']

    # Équipements
    if data.get('has_garden'):   price *= 1.08
    if data.get('has_pool'):     price *= 1.12
    if data.get('has_garage'):   price *= 1.05
    if data.get('has_balcony'):  price *= 1.03
    if data.get('has_elevator'): price *= 1.03

    # Ancienneté
    year = data.get('construction_year')
    if year:
        age = timezone.now().year - year
        if age < 5:   price *= 1.10
        elif age < 15: price *= 1.00
        elif age < 30: price *= 0.95
        else:          price *= 0.88

    # Ville
    city_factor = {
        'tunis':    1.40, 'la marsa': 1.35, 'ariana': 1.28,
        'sousse':   1.20, 'hammamet': 1.15, 'sfax':   1.10,
        'nabeul':   1.08, 'monastir': 1.08, 'bizerte': 1.00,
        'gabes':    0.95,
    }.get(data['city'].lower(), 1.00)

    price *= city_factor
    price *= random.uniform(0.92, 1.08)
    return round(price, 2)


@login_required
def predict_price(request):
    form = PredictionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data            = form.cleaned_data
        predicted_price = _simulate_price(data)
        confidence      = round(random.uniform(0.72, 0.94), 2)

        # Propriété temporaire liée à la prédiction
        prop = Property.objects.create(
            title=f"Estimation — {data['city']}",
            property_type=data['property_type'],
            city=data['city'],
            address='N/A',
            postal_code='00000',
            surface=data['surface'],
            rooms=data['rooms'],
            bedrooms=data['bedrooms'],
            price=predicted_price,
            created_by=request.user,
        )
        pred = Prediction.objects.create(
            property=prop,
            predicted_price=predicted_price,
            confidence_score=confidence,
            model_version='v1.0-statistique',
        )
        messages.success(request, f"Estimation réalisée : {predicted_price:,.0f} DT".replace(',', ' '))
        return redirect('immobilier:prediction_result', pk=pred.pk)

    return render(request, 'immobilier/prediction/predict.html', {'form': form})


def prediction_result(request, pk):
    prediction = get_object_or_404(Prediction, pk=pk)
    return render(request, 'immobilier/prediction/result.html', {'prediction': prediction})


# ═══════════════════════════════════════════════════════════════════════════
#  GESTION DES BIENS
# ═══════════════════════════════════════════════════════════════════════════

@login_required
def add_property(request):
    if not request.user.can_add_property:
        messages.error(request, "Vous n'êtes pas autorisé à ajouter un bien.")
        return redirect('immobilier:home')

    pform = PropertyForm(request.POST or None)
    fform = PropertyFeatureForm(request.POST or None)

    if request.method == 'POST' and pform.is_valid() and fform.is_valid():
        prop            = pform.save(commit=False)
        prop.created_by = request.user
        prop.save()
        feat          = fform.save(commit=False)
        feat.property = prop
        feat.save()
        messages.success(request, "Bien ajouté avec succès !")
        return redirect('immobilier:property_detail', pk=prop.pk)

    return render(request, 'immobilier/property/form.html', {
        'property_form': pform,
        'feature_form':  fform,
        'action':        'Ajouter',
    })


@login_required
def edit_property(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if prop.created_by != request.user and not request.user.is_staff:
        messages.error(request, "Vous ne pouvez pas modifier ce bien.")
        return redirect('immobilier:property_detail', pk=pk)

    features = getattr(prop, 'features', None)
    pform    = PropertyForm(request.POST or None, instance=prop)
    fform    = PropertyFeatureForm(request.POST or None, instance=features)

    if request.method == 'POST' and pform.is_valid() and fform.is_valid():
        pform.save()
        feat          = fform.save(commit=False)
        feat.property = prop
        feat.save()
        messages.success(request, "Bien modifié avec succès !")
        return redirect('immobilier:property_detail', pk=pk)

    return render(request, 'immobilier/property/form.html', {
        'property_form': pform,
        'feature_form':  fform,
        'property':      prop,
        'action':        'Modifier',
    })


@login_required
def delete_property(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if prop.created_by != request.user and not request.user.is_staff:
        messages.error(request, "Action non autorisée.")
        return redirect('immobilier:property_detail', pk=pk)
    if request.method == 'POST':
        prop.delete()
        messages.success(request, "Bien supprimé.")
        return redirect('immobilier:property_list')
    return render(request, 'immobilier/property/confirm_delete.html', {'property': prop})


# ═══════════════════════════════════════════════════════════════════════════
#  AUTHENTIFICATION
# ═══════════════════════════════════════════════════════════════════════════

def register_view(request):
    if request.user.is_authenticated:
        return redirect('immobilier:dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        UserProfile.objects.create(user=user)
        messages.success(request, "Compte créé ! Connectez-vous.")
        return redirect('immobilier:login')
    return render(request, 'immobilier/auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('immobilier:dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f"Bienvenue, {user.first_name or user.email} !")
        return redirect(request.GET.get('next', 'immobilier:dashboard'))
    return render(request, 'immobilier/auth/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('immobilier:home')


# ═══════════════════════════════════════════════════════════════════════════
#  PROFIL
# ═══════════════════════════════════════════════════════════════════════════

@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    props       = Property.objects.filter(created_by=request.user).order_by('-created_at')[:5]
    return render(request, 'immobilier/auth/profile.html', {
        'profile':          profile,
        'user_properties':  props,
    })


@login_required
def edit_profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    uform = UserUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
    pform = UserProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and uform.is_valid() and pform.is_valid():
        uform.save()
        pform.save()
        messages.success(request, "Profil mis à jour !")
        return redirect('immobilier:profile')
    return render(request, 'immobilier/auth/edit_profile.html', {
        'user_form':    uform,
        'profile_form': pform,
    })


# ═══════════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════

@login_required
def dashboard(request):
    user = request.user
    ctx  = {'user': user}

    if user.is_agent or user.can_add_property:
        my_props = Property.objects.filter(created_by=user)
        ctx.update({
            'my_properties':   my_props.order_by('-created_at')[:5],
            'total_properties': my_props.count(),
            'avg_price':        my_props.aggregate(Avg('price'))['price__avg'] or 0,
            'unread_messages':  Message.objects.filter(recipient=user, is_read=False).count(),
            'recent_ratings':   PropertyRating.objects.filter(
                                    property__created_by=user).order_by('-created_at')[:5],
        })
        template = 'immobilier/dashboard/agent.html' if user.is_agent else 'immobilier/dashboard/vendeur.html'

    else:  # acheteur / investisseur
        ctx.update({
            'favorites':       Favorite.objects.filter(user=user).select_related('property')[:5],
            'recent_searches': SearchHistory.objects.filter(user=user).order_by('-created_at')[:5],
            'sent_messages':   Message.objects.filter(sender=user).order_by('-created_at')[:5],
        })
        template = 'immobilier/dashboard/acheteur.html'

    return render(request, template, ctx)


# ═══════════════════════════════════════════════════════════════════════════
#  FAVORIS
# ═══════════════════════════════════════════════════════════════════════════

@login_required
def favorites_list(request):
    favs = Favorite.objects.filter(user=request.user).select_related('property').order_by('-created_at')
    return render(request, 'immobilier/features/favorites.html', {'favorites': favs})


@login_required
def add_favorite(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    _, created = Favorite.objects.get_or_create(user=request.user, property=prop)
    if created:
        messages.success(request, f"« {prop.title} » ajouté aux favoris.")
    else:
        messages.info(request, "Déjà dans vos favoris.")
    return redirect('immobilier:property_detail', pk=pk)


@login_required
def remove_favorite(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    Favorite.objects.filter(user=request.user, property=prop).delete()
    messages.success(request, f"« {prop.title} » retiré des favoris.")
    return redirect(request.META.get('HTTP_REFERER', 'immobilier:favorites_list'))


# ═══════════════════════════════════════════════════════════════════════════
#  MESSAGERIE
# ═══════════════════════════════════════════════════════════════════════════

@login_required
def inbox(request):
    received = Message.objects.filter(recipient=request.user).select_related('sender', 'property').order_by('-created_at')
    sent     = Message.objects.filter(sender=request.user).select_related('recipient', 'property').order_by('-created_at')
    return render(request, 'immobilier/messages/inbox.html', {
        'received':      received,
        'sent':          sent,
        'unread_count':  received.filter(is_read=False).count(),
    })


@login_required
def send_message(request, property_pk=None):
    prop      = get_object_or_404(Property, pk=property_pk) if property_pk else None
    recipient = prop.created_by if prop else None

    form = MessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        rid = request.POST.get('recipient_id')
        if rid:
            recipient = get_object_or_404(CustomUser, pk=rid)
        if not recipient:
            messages.error(request, "Destinataire introuvable.")
        else:
            msg            = form.save(commit=False)
            msg.sender     = request.user
            msg.recipient  = recipient
            msg.property   = prop
            msg.save()

            Notification.objects.create(
                user=recipient,
                notification_type='message',
                title=f"Nouveau message de {request.user.get_full_name() or request.user.email}",
                message=f"Sujet : {msg.subject}",
                related_property=prop,
            )
            messages.success(request, "Message envoyé !")
            return redirect('immobilier:inbox')

    return render(request, 'immobilier/messages/send_message.html', {
        'form':      form,
        'property':  prop,
        'recipient': recipient,
    })


@login_required
def mark_message_read(request, pk):
    msg = get_object_or_404(Message, pk=pk, recipient=request.user)
    msg.is_read = True
    msg.save()
    return redirect('immobilier:inbox')


# ═══════════════════════════════════════════════════════════════════════════
#  ÉVALUATIONS
# ═══════════════════════════════════════════════════════════════════════════

@login_required
def rate_property(request, pk):
    prop        = get_object_or_404(Property, pk=pk)
    existing    = PropertyRating.objects.filter(user=request.user, property=prop).first()
    form        = PropertyRatingForm(request.POST or None, instance=existing)

    if request.method == 'POST' and form.is_valid():
        rating          = form.save(commit=False)
        rating.user     = request.user
        rating.property = prop
        rating.save()
        messages.success(request, "Évaluation enregistrée !")
        return redirect('immobilier:property_detail', pk=pk)

    return render(request, 'immobilier/features/rate_property.html', {
        'form':     form,
        'property': prop,
        'existing': existing,
    })


# ═══════════════════════════════════════════════════════════════════════════
#  STATISTIQUES & EXPORT
# ═══════════════════════════════════════════════════════════════════════════

def statistics(request):
    props  = Property.objects.all()
    by_type = (props.values('property_type')
                    .annotate(count=Count('id'), avg_price=Avg('price'))
                    .order_by('-count'))
    by_city = (props.values('city')
                    .annotate(count=Count('id'), avg_price=Avg('price'))
                    .order_by('-count')[:10])
    return render(request, 'immobilier/features/statistics.html', {
        'total':      props.count(),
        'avg_price':  props.aggregate(Avg('price'))['price__avg'] or 0,
        'by_type':    by_type,
        'by_city':    by_city,
    })


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="biens_immobiliers.csv"'
    response.write('\ufeff')  # BOM UTF-8 pour Excel

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Titre', 'Type', 'Ville', 'Surface (m²)',
                     'Pièces', 'Chambres', 'Prix (DT)', 'Date ajout'])
    for p in Property.objects.order_by('-created_at'):
        writer.writerow([
            p.pk, p.title, p.get_property_type_display(),
            p.city, p.surface, p.rooms, p.bedrooms,
            p.price, p.created_at.strftime('%d/%m/%Y'),
        ])
    return response
