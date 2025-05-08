from api.models.policy import Policy
from django.utils import timezone
from rest_framework.exceptions import ValidationError

def create_policy_logic(data):
    if data['expiry_date'] < timezone.now().date():
        raise ValidationError({"expiry_date": "A expiry date deve ser no futuro!"})
    
    policy = Policy.objects.create(
        customer_name=data['customer_name'],
        policy_type=data['policy_type'],
        expiry_date=data['expiry_date']
    )
    return policy
