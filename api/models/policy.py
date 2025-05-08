from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Policy(models.Model):
    customer_name = models.CharField(max_length=255)
    policy_type = models.CharField(max_length=50)
    expiry_date = models.DateField()

    def clean(self):
        if self.expiry_date < timezone.now().date():
            raise ValidationError("Expiry date cannot be in the past.")

    def __str__(self):
        return f"{self.customer_name} - {self.policy_type}"
