from django.urls import path
from .views import anagraphic_list

urlpatterns = [
    path('api/anagraphic/', anagraphic_list.as_view(), name='anagraphic-list'),
]
