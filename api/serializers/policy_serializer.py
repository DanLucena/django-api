from rest_framework import serializers
from api.models.policy import Policy

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['id', 'customer_name', 'policy_type', 'expiry_date']
