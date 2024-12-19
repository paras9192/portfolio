from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ThemeMetaDataViewSet
from .views import PortFolioViewSet


app_name = 'portfolio' 
router = DefaultRouter()
router.register(r'theme', ThemeMetaDataViewSet, basename='theme')
router.register(r'portfolio', PortFolioViewSet, basename='portfolio')
urlpatterns = router.urls


