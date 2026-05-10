from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms_auth import CustomUserCreationForm, CustomAuthenticationForm, UserUpdateForm, UserProfileForm
from .models import CustomUser, UserProfile, Property

def register_view(request):
    """Vue d'inscription des utilisateurs"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Compte créé avec succès pour {user.email}! Vous pouvez maintenant vous connecter.')
            return redirect('immobilier:login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'immobilier/auth/register.html', {'form': form})

def login_view(request):
    """Vue de connexion des utilisateurs"""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenue {user.first_name}!')
            
            # Redirection selon le rôle
            next_url = request.GET.get('next', 'immobilier:home')
            if user.role == 'agent':
                return redirect('immobilier:agent_dashboard')
            elif user.role == 'vendeur':
                return redirect('immobilier:vendeur_dashboard')
            else:
                return redirect(next_url)
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'immobilier/auth/login.html', {'form': form})

@login_required
def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté avec succès.')
    return redirect('immobilier:home')

@login_required
def profile_view(request):
    """Vue du profil utilisateur"""
    profile = get_object_or_404(UserProfile, user=request.user)
    user_properties = Property.objects.filter(created_by=request.user).order_by('-created_at')[:5]
    
    context = {
        'profile': profile,
        'user_properties': user_properties,
    }
    return render(request, 'immobilier/auth/profile.html', context)

@login_required
def edit_profile_view(request):
    """Vue d'édition du profil"""
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès!')
            return redirect('immobilier:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    return render(request, 'immobilier/auth/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def agent_dashboard(request):
    """Tableau de bord pour les agents immobiliers"""
    if not request.user.is_agent:
        messages.error(request, 'Accès réservé aux agents immobiliers.')
        return redirect('immobilier:home')
    
    # Statistiques pour l'agent
    total_properties = Property.objects.filter(created_by=request.user).count()
    recent_properties = Property.objects.filter(created_by=request.user).order_by('-created_at')[:5]
    
    context = {
        'total_properties': total_properties,
        'recent_properties': recent_properties,
    }
    return render(request, 'immobilier/auth/agent_dashboard.html', context)

@login_required
def vendeur_dashboard(request):
    """Tableau de bord pour les vendeurs"""
    if not request.user.is_vendeur:
        messages.error(request, 'Accès réservé aux vendeurs.')
        return redirect('immobilier:home')
    
    # Propriétés du vendeur
    user_properties = Property.objects.filter(created_by=request.user).order_by('-created_at')
    
    context = {
        'user_properties': user_properties,
    }
    return render(request, 'immobilier/auth/vendeur_dashboard.html', context)

@login_required
def acheteur_dashboard(request):
    """Tableau de bord pour les acheteurs"""
    if not request.user.is_acheteur:
        messages.error(request, 'Accès réservé aux acheteurs.')
        return redirect('immobilier:home')
    
    # Propriétés favorites (à implémenter)
    # recent_searches = SearchHistory.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        # 'recent_searches': recent_searches,
    }
    return render(request, 'immobilier/auth/acheteur_dashboard.html', context)

class CustomPasswordChangeView(PasswordChangeView):
    """Vue personnalisée pour le changement de mot de passe"""
    template_name = 'immobilier/auth/change_password.html'
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        messages.success(self.request, 'Votre mot de passe a été changé avec succès!')
        return super().form_valid(form)

@login_required
def user_list_view(request):
    """Vue pour lister les utilisateurs (admin/agent uniquement)"""
    if not (request.user.is_agent or request.user.is_staff):
        messages.error(request, 'Accès non autorisé.')
        return redirect('immobilier:home')
    
    users = CustomUser.objects.all().order_by('-date_joined')
    
    # Filtrer par rôle si spécifié
    role_filter = request.GET.get('role')
    if role_filter:
        users = users.filter(role=role_filter)
    
    context = {
        'users': users,
        'role_choices': CustomUser.ROLE_CHOICES,
        'current_role': role_filter,
    }
    return render(request, 'immobilier/auth/user_list.html', context)
