from rest_framework import serializers
from .models import ANAGRAPHIC_VIEW

class MyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ANAGRAPHIC_VIEW
        fields = '__all__'
