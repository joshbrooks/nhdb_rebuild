from rest_framework import serializers

from jsontag.models import Translation


class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = [field.name for field in model._meta.fields]