from rest_framework import serializers
from .models import Policy
from django.utils import timezone

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'

    def validate_expiry_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Expiry date cannot be in the past.")
        return value
