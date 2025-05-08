from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from api.models.policy import Policy

class PolicyAPITest(APITestCase):
    def setUp(self):
        self.policy = Policy.objects.create(
            customer_name="Fulano2",
            policy_type="Health",
            expiry_date=(timezone.now().date() + timedelta(days=30))
        )
        self.url = reverse('policy-list')
        self.policy_url = reverse('policy-detail', kwargs={'pk': self.policy.pk})
        
        self.valid_payload = {
            "customer_name": "Fulano",
            "policy_type": "Health",
            "expiry_date": (timezone.now().date() + timedelta(days=30)).isoformat()
        }
        
        self.invalid_payload = {
            "customer_name": "Beltrano",
            "policy_type": "Auto",
            "expiry_date": (timezone.now().date() - timedelta(days=5)).isoformat()
        }

        self.valid_update_payload = {
            "customer_name": "Novo Nome",
            "policy_type": "Auto",
            "expiry_date": (timezone.now().date() + timedelta(days=60)).isoformat()
        }

        self.invalid_update_payload = {
            "customer_name": "Nome Inválido",
            "policy_type": "Health",
            "expiry_date": (timezone.now().date() - timedelta(days=1)).isoformat()
        }

    def test_create_policy_success(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Policy.objects.count(), 2)

    def test_create_policy_with_expired_date_fails(self):
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_policy_success(self):
        response = self.client.put(self.policy_url, self.valid_update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.policy.refresh_from_db()
        self.assertEqual(self.policy.customer_name, "Novo Nome")
        self.assertEqual(self.policy.policy_type, "Auto")
        self.assertEqual(self.policy.expiry_date, timezone.now().date() + timedelta(days=60))

    def test_update_policy_with_expired_date_fails(self):
        response = self.client.put(self.policy_url, self.invalid_update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_policy_success(self):
        partial_payload = {"customer_name": "Nome Parcial"}
        response = self.client.patch(self.policy_url, partial_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.policy.refresh_from_db()
        self.assertEqual(self.policy.customer_name, "Nome Parcial")
        self.assertEqual(self.policy.policy_type, "Health")

    def test_delete_policy_success(self):
        response = self.client.delete(self.policy_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Policy.objects.count(), 0)

    def test_delete_policy_not_found(self):
        url_not_found = reverse('policy-detail', kwargs={'pk': 999})
        response = self.client.delete(url_not_found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
