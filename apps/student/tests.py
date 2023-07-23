from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.sponsor.models import Sponsor
from apps.student.models import Student, University, Transfer


class TestStudent(APITestCase):

    def setUp(self) -> None:
        jwt_response = self.client.post(path=reverse('obtain-token'), data={'username': '123', 'password': '123'})
        self.jwt_access_token = jwt_response.data['access']

    @classmethod
    def setUpTestData(cls):
        sponsor = Sponsor.objects.create(
            full_name="Test Sponsor 1",
            phone_number="98996488450",
            sponsor_type="LEGAL_ENTITY",
            balance=20_000_000,
            company="Company Name 1",
            status="APPROVED"
        )

        university = University.objects.create(
            name='TATU',
            address='Bodomzor metro'
        )

        student = Student.objects.create(
            university_id=university.id,
            full_name='Student 1',
            contract_sum=30_000_000,
            degree="MASTER",
            due_date=datetime.now(),
            phone_number='998999099009',
            balance=10_000_000,
        )

        Transfer.objects.create(
            student_id=student.id,
            sponsor_id=sponsor.id,
            amount=10_000_000
        )

        get_user_model().objects.create_user(username='123', password='123', email='123@321.uz')

    def test_list_students_200(self):
        response = self.client.get(
            path=reverse('students-list'),
            headers={
                'Authorization': f"Bearer {self.jwt_access_token}"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['full_name'], 'Student 1')
        self.assertEqual(response.data[0]['degree'], "MASTER")
        self.assertEqual(response.data[0]['balance'], 10_000_000)
        self.assertEqual(response.data[0]['contract_sum'], 30_000_000)

    def test_detail_students_200(self):
        response = self.client.get(
            reverse('student-detail', kwargs={'pk': 1}),
            {'Authorization': f"Bearer {self.jwt_access_token}"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'Student 1')
        self.assertEqual(response.data['degree'], "MASTER")
        self.assertEqual(response.data['balance'], 10_000_000)
        self.assertEqual(response.data['contract_sum'], 30_000_000)

        self.assertEqual(response.data['sponsors'][0]["sponsor_full_name"], 'Test Sponsor 1')
        self.assertEqual(response.data['sponsors'][0]["spend_sum"], 10_000_000)

    def test_student_401(self):
        response = self.client.get(
            path=reverse('student-detail', kwargs={'pk': 1}),
            headers={
                'Authorization': f"Bearer wrong_jwt_token"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_student_201(self):
        response = self.client.post(
            path=reverse('student-create'),
            headers={'Authorization': f"Bearer {self.jwt_access_token}"},
            data={
                "full_name": "Student 2",
                "phone_number": "998944943435",
                "degree": "BACHELOR",
                "university": 1,
                "due_date": str(datetime.now() + timedelta(weeks=1)),
                "contract_sum": 25_000_000
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_student_400(self):
        response = self.client.post(
            path=reverse('student-create'),
            data={
                "full_name": "Student 2",
                "phone_number": "998944943435",
                "degree": "BACHELOR",
                "university": 1,
                "contract_sum": 25_000_000
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_attach_sponsor_to_student(self):
        response = self.client.post(
            path=reverse('attach-sponsor-to-student'),
            headers={'Authorization': f"Bearer {self.jwt_access_token}"},
            data={
                "sponsor_id": 1,
                "student_id": 1,
                "amount": 1_000_000
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_detach_sponsor_to_student(self):
        response = self.client.delete(
            path=reverse('detach-sponsor-to-student'),
            headers={'Authorization': f"Bearer {self.jwt_access_token}"},
            data={
                'sponsor_id': 1,
                'student_id': 1
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_sponsorship_transfer(self):
        response = self.client.put(
            path=reverse('update-sponsorship', kwargs={'pk':1}),
            headers={'Authorization': f"Bearer {self.jwt_access_token}"},
            data={
                'sponsor_id': 1,
                'student_id': 1,
                'amount': 1_000_000
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
