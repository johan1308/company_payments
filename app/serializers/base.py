from rest_framework import serializers
from app.models.base import Status, Options



class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('__all__')


class OptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Options
        fields = ('__all__')


