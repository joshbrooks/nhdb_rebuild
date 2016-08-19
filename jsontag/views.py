from django.shortcuts import render

from . import serializers
from .models import Translation
from project_tracker.views import JsonListView
# Create your views here.
class TranslationList(JsonListView):
    queryset = Translation.objects.all()
    serializer = serializers.TranslationSerializer
