from django.urls import path
from . import views

urlpatterns = [
    path('about-author/', views.about_author),
    path('about-lab/', views.about_lab),
    path('', views.main_page),
]
