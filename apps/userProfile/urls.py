from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import JobsViewSet
from apps.userProfile.views import UserDataViewSet


app_name = 'profile' 
router = DefaultRouter()
router.register(r'jobs', JobsViewSet, basename='jobs')
router.register(r'userData', UserDataViewSet, basename='userData')
urlpatterns = router.urls


