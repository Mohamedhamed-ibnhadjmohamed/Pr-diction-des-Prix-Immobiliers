from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/predict/", views.PredictionAPI.as_view(), name="predict"),
    path("api/analysis/", views.analysis_data, name="analysis"),
    path("api/simulation/", views.simulation_data, name="simulation"),
    path("api/history/", views.history_data, name="history"),
]
