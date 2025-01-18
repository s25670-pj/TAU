from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User

class UserAPITests(APITestCase):
    def setUp(self):
        # Tworzymy przykładowego użytkownika do testów
        self.user = User.objects.create(
            name="Jan Kowalski",
            email="jan@kowalski.pl"
        )
        self.users_url = reverse('user-list')
        self.user_detail_url = reverse('user-detail', kwargs={'pk': self.user.id})

    def test_get_users_list(self):
        """Test pobierania listy użytkowników"""
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Jan Kowalski')

    def test_get_user_detail(self):
        """Test pobierania szczegółów użytkownika"""
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Jan Kowalski')
        self.assertEqual(response.data['email'], 'jan@kowalski.pl')

    def test_get_nonexistent_user(self):
        """Test pobierania nieistniejącego użytkownika"""
        url = reverse('user-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user(self):
        """Test tworzenia nowego użytkownika"""
        data = {
            'name': 'Anna Nowak',
            'email': 'anna@nowak.pl'
        }
        response = self.client.post(self.users_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Anna Nowak')

    def test_create_user_invalid_data(self):
        """Test tworzenia użytkownika z niepoprawnymi danymi"""
        data = {
            'name': 'Anna Nowak'
            # brak email
        }
        response = self.client.post(self.users_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user(self):
        """Test aktualizacji danych użytkownika"""
        data = {
            'name': 'Jan Kowalski Zaktualizowany',
            'email': 'jan.zaktualizowany@kowalski.pl'
        }
        response = self.client.put(self.user_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Jan Kowalski Zaktualizowany')
        
        # Sprawdzenie czy dane zostały rzeczywiście zaktualizowane
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.name, 'Jan Kowalski Zaktualizowany')

    def test_update_nonexistent_user(self):
        """Test aktualizacji nieistniejącego użytkownika"""
        url = reverse('user-detail', kwargs={'pk': 999})
        data = {
            'name': 'Test',
            'email': 'test@test.pl'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user(self):
        """Test usuwania użytkownika"""
        response = self.client.delete(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

    def test_delete_nonexistent_user(self):
        """Test usuwania nieistniejącego użytkownika"""
        url = reverse('user-detail', kwargs={'pk': 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)