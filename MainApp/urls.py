from django.urls import path
from .views import StatusView,PNRFormView,EmailUpdatesView


urlpatterns = [
    path('pnr/', PNRFormView.as_view(), name='pnr_form'),
    path("status/",StatusView.as_view(), name='status'),
    path("update/",EmailUpdatesView.as_view(), name='update')
]