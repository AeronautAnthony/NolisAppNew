from django.urls import path
from . import views

urlpatterns = [
    path('', views.Welcome, name='Welcome'),
    path('Flavor/', views.Flavor, name='Flavor'),

    path('Ingredients/', views.Ingredients, name='Ingredients'),
    path('Recommendation/', views.Recommendation, name='Recommendation'),

    path('process_ingredients/', views.process_ingredients, name='process_ingredients'),
]