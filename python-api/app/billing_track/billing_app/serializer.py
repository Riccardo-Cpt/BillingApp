from rest_framework import serializers
from .models import ANAGRAPHIC_VIEW

class AnagraphigViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ANAGRAPHIC_VIEW
        fields = '__all__'
