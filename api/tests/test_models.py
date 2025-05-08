from django.test import TestCase
from django.utils import timezone
from api.models.policy import Policy
from django.core.exceptions import ValidationError
from datetime import timedelta

class PolicyModelTest(TestCase):
    def test_policy_creation_with_valid_data(self):
        future_date = timezone.now().date() + timedelta(days=10)
        policy = Policy.objects.create(
            customer_name="João da Silva",
            policy_type="Auto",
            expiry_date=future_date,
        )
        self.assertEqual(str(policy), "João da Silva - Auto")

    def test_policy_creation_with_past_date_should_fail(self):
        past_date = timezone.now().date() - timedelta(days=1)
        policy = Policy(
            customer_name="Maria",
            policy_type="Life",
            expiry_date=past_date
        )
        with self.assertRaises(ValidationError):
            policy.full_clean()
