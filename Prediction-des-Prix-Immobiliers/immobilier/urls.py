from django.urls import path
from . import views

app_name = 'immobilier'

urlpatterns = [
    # ── Pages publiques ──────────────────────────────────────────────────
    path('',                          views.home,            name='home'),
    path('properties/',               views.property_list,   name='property_list'),
    path('property/<int:pk>/',        views.property_detail, name='property_detail'),
    path('search/',                   views.advanced_search, name='advanced_search'),

    # ── Prédiction ───────────────────────────────────────────────────────
    path('predict/',                       views.predict_price,     name='predict_price'),
    path('predict/result/<int:pk>/',       views.prediction_result, name='prediction_result'),

    # ── Gestion des biens ────────────────────────────────────────────────
    path('property/add/',                  views.add_property,    name='add_property'),
    path('property/<int:pk>/edit/',        views.edit_property,   name='edit_property'),
    path('property/<int:pk>/delete/',      views.delete_property, name='delete_property'),

    # ── Authentification ─────────────────────────────────────────────────
    path('register/',                      views.register_view,   name='register'),
    path('login/',                         views.login_view,      name='login'),
    path('logout/',                        views.logout_view,     name='logout'),

    # ── Profil ───────────────────────────────────────────────────────────
    path('profile/',                       views.profile_view,      name='profile'),
    path('profile/edit/',                  views.edit_profile_view, name='edit_profile'),

    # ── Dashboard ────────────────────────────────────────────────────────
    path('dashboard/',                     views.dashboard,           name='dashboard'),

    # ── Favoris ──────────────────────────────────────────────────────────
    path('favorites/',                     views.favorites_list,          name='favorites_list'),
    path('favorites/add/<int:pk>/',        views.add_favorite,            name='add_favorite'),
    path('favorites/remove/<int:pk>/',     views.remove_favorite,         name='remove_favorite'),

    # ── Messagerie ───────────────────────────────────────────────────────
    path('inbox/',                         views.inbox,                   name='inbox'),
    path('message/send/',                  views.send_message,            name='send_message'),
    path('message/send/<int:property_pk>/', views.send_message,           name='send_message_property'),
    path('message/<int:pk>/read/',         views.mark_message_read,       name='mark_message_read'),

    # ── Évaluations ──────────────────────────────────────────────────────
    path('property/<int:pk>/rate/',        views.rate_property, name='rate_property'),

    # ── Statistiques & export ────────────────────────────────────────────
    path('statistics/',                    views.statistics,        name='statistics'),
    path('export/csv/',                    views.export_csv,        name='export_csv'),
]
