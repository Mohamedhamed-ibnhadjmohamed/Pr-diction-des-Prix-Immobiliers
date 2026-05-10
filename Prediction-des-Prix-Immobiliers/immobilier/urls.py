from django.urls import path
from . import views
from . import views_auth
from . import views_features
from . import views_complete
# from . import views_advanced  # Temporairement désactivé

app_name = 'immobilier'

urlpatterns = [
    # Main application URLs
    path('', views.home, name='home'),
    path('properties/', views.property_list, name='property_list'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('predict/', views.predict_price, name='predict_price'),
    path('predict/result/<int:pk>/', views.prediction_result, name='prediction_result'),
    path('add/', views.add_property, name='add_property'),
    
    # Authentication URLs
    path('login/', views_auth.login_view, name='login'),
    path('register/', views_auth.register_view, name='register'),
    path('logout/', views_auth.logout_view, name='logout'),
    path('profile/', views_auth.profile_view, name='profile'),
    path('profile/edit/', views_auth.edit_profile_view, name='edit_profile'),
    path('change-password/', views_auth.CustomPasswordChangeView.as_view(), name='change_password'),
    
    # Dashboard URLs
    path('dashboard/', views_complete.dashboard_view, name='dashboard'),
    path('dashboard/agent/', views_complete.agent_dashboard, name='agent_dashboard'),
    path('dashboard/vendeur/', views_complete.vendeur_dashboard, name='vendeur_dashboard'),
    path('dashboard/acheteur/', views_complete.acheteur_dashboard, name='acheteur_dashboard'),
    
    # User management URLs
    path('users/', views_auth.user_list_view, name='user_list'),
    
    # Feature URLs
    path('favorites/', views_features.favorites_list, name='favorites_list'),
    path('add-favorites/<int:property_id>/', views_features.add_to_favorites, name='add_to_favorites'),
    path('remove-favorites/<int:property_id>/', views_features.remove_from_favorites, name='remove_from_favorites'),
    path('send-message/', views_complete.send_message, name='send_message'),
    path('send-message/<int:property_id>/', views_complete.send_message, name='send_message_property'),
    path('inbox/', views_complete.inbox, name='inbox'),
    path('mark-message-read/<int:message_id>/', views_complete.mark_message_read, name='mark_message_read'),
    path('rate-property/<int:property_id>/', views_complete.rate_property, name='rate_property'),
    path('advanced-search/', views_complete.advanced_search, name='advanced_search'),
    path('search-history/', views_complete.search_history, name='search_history'),
    path('statistics/', views_complete.statistics_view, name='statistics'),
    path('export/', views_complete.export_properties, name='export_properties'),
    
    # Advanced Features URLs - Temporairement désactivés
    # path('notifications/', views_advanced.notifications_list, name='notifications_list'),
    # path('mark-notification-read/<int:notification_id>/', views_advanced.mark_notification_read, name='mark_notification_read'),
    # path('mark-all-notifications-read/', views_advanced.mark_all_notifications_read, name='mark_all_notifications_read'),
    # path('review-user/<int:user_id>/', views_advanced.review_user, name='review_user'),
    # path('user-profile/<int:user_id>/', views_advanced.user_profile, name='user_profile'),
    # path('report/', views_advanced.report_content, name='report_content'),
    # path('create-comparison/', views_advanced.create_comparison, name='create_comparison'),
    # path('comparison/<int:pk>/', views_advanced.comparison_detail, name='comparison_detail'),
    # path('comparisons/', views_advanced.comparisons_list, name='comparisons_list'),
    # path('upload-document/', views_advanced.upload_document, name='upload_document'),
    # path('documents/', views_advanced.documents_list, name='documents_list'),
    # path('recommendations/', views_advanced.recommendations_list, name='recommendations_list'),
    # path('admin/notifications/', views_advanced.admin_notifications, name='admin_notifications'),
    # path('admin/reports/', views_advanced.admin_reports, name='admin_reports'),
    # path('export-data/', views_advanced.export_data, name='export_data'),
]
