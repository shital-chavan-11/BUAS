from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    dashboard_view,
    profile_view,
    update_profile
)
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve 

urlpatterns = [
    path('register/', register_view, name='register'),  # Registration page
    path('login/', login_view, name='login'),            # Login page
    path('logout/', logout_view, name='logout'),         # Logout action
    path('', dashboard_view, name='dashboard'), # User dashboard
    path('profile/', profile_view, name='profile'), 
    path('profile/update/', update_profile, name='update_profile'),  # Check the URL and name
    path('media/<path:path>/', serve, {'document_root': settings.MEDIA_ROOT}),  # For media files
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  