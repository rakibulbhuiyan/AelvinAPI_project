
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),           # our signup API
    path('accounts/', include('allauth.urls')),
    path('api/', include('post_app.urls')), 
    path('auth/', include('social_django.urls', namespace='social')),

    path('auth/google/', include('allauth.socialaccount.providers.google.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
