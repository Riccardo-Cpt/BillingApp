from django.urls import path
from .views import anagraphic_list

urlpatterns = [
    path('billing_app/anagraphic/', anagraphic_list, name='anagraphic-list'),
]
