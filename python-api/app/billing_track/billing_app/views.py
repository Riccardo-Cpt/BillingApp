from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from billing_app.models import ANAGRAPHIC_VIEW
from billing_app.serializers import AnagraphigViewSerializer

@api_view(['GET'])
def anagraphic_list(request):
    """
    List all anagraphical information
    """
    if request.method == 'GET':
        anagraphic = ANAGRAPHIC_VIEW.objects.all()
        serializer = AnagraphigViewSerializer(anagraphic, many=True)
        return Response(serializer.data)
