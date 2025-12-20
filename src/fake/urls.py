from django.urls import path
from . import views, download

urlpatterns = [
    path('', views.home, name='home'),
    path('api/generate/', views.generate_identity, name='api_generate'),
    path('api/reset/', views.reset_session, name='api_reset'),
    path('api/download/', download.download_pdf, name='download_pdf'),
]

