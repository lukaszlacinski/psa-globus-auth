from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls', namespace='social')),
]
