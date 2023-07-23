from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.sponsor.models import Sponsor


class TestSponsor(APITestCase):

    def setUp(self) -> None:
        jwt_response = self.client.post(path=reverse('obtain-token'), data={'username': '123', 'password': '123'})
        self.jwt_access_token = jwt_response.data['access']

    @classmethod
    def setUpTestData(cls):
        Sponsor.objects.create(
            full_name="Test Sponsor 1",
            phone_number="98996488450",
            sponsor_type="LEGAL_ENTITY",
            balance=20_000_000,
            company="Company Name 1"
        )
        get_user_model().objects.create_user(username='123', password='123', email='123@321.uz')

    def test_apply_for_sponsorship(self):
        url = reverse('appy-for-sponsorship')

        data = {
            "full_name": "Test Sponsor 2",
            "phone_number": "98996488450",
            "sponsor_type": "LEGAL_ENTITY",
            "balance": 10_000_000,
            "company": "Company Name 2"
        }

        response = self.client.post(url, data=data)
        sponsor = Sponsor.objects.get(pk=2)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(sponsor.full_name, data['full_name'])
        self.assertEqual(sponsor.phone_number, data['phone_number'])
        self.assertEqual(sponsor.balance, data['balance'])
        self.assertEqual(sponsor.sponsor_type, data['sponsor_type'])

    def test_list_sponsors_200(self):
        response = self.client.get(
            path=reverse('sponsors-list'),
            headers={
                'Authorization': f"Bearer {self.jwt_access_token}"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['full_name'], "Test Sponsor 1")
        self.assertEqual(response.data[0]['status'], "PENDING")
        self.assertEqual(response.data[0]['balance'], 20_000_000)

    def test_list_sponsors_401(self):
        response = self.client.get(
            path=reverse('sponsors-list'),
            headers={
                'Authorization': f"Bearer wrong_jwt_token"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_sponsor_200(self):
        response = self.client.get(
            reverse('sponsor-detail', kwargs={'pk': 1}),
            {'Authorization': f"Bearer {self.jwt_access_token}"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'Test Sponsor 1')
        self.assertEqual(response.data['phone_number'], '98996488450')

    def test_detail_sponsor_404(self):
        response = self.client.get(
            reverse('sponsor-detail', kwargs={'pk': 100}),
            {'Authorization': f"Bearer {self.jwt_access_token}"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_sponsor_200(self):
        response = self.client.put(
            path=reverse('sponsor-update', kwargs={'pk': 1}),
            data={
                "full_name": "Updated Test Sponsor 2",
                "phone_number": "98996488450",
                "sponsor_type": "LEGAL_ENTITY",
                "balance": 40_000_000,
                "company": "Company Name 2"
            },
            headers={'Authorization': f"Bearer {self.jwt_access_token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["full_name"], 'Updated Test Sponsor 2')
        self.assertEqual(response.data['balance'], 40_000_000)

    def test_update_sponsor_400(self):
        response = self.client.put(
            path=reverse('sponsor-update', kwargs={'pk': 1}),
            data={
                "full_name": "Updated Test Sponsor 2",
                "phone_number": "98996488450",
                "sponsor_type": "LEGAL_ENTITY",
                "company": "Company Name 2"
            },
            headers={'Authorization': f"Bearer {self.jwt_access_token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
