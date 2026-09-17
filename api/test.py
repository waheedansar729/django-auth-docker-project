from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(APITestCase):
    def setUp(self):
        # Test user create karna authentication aur tests ke liye
        self.username = "testuser"
        self.password = "testpassword123"
        self.user = User.objects.create_user(
            username=self.username,
            email="test@example.com",
            password=self.password,
            phone_number="1234567890"
        )
        self.list_url = reverse('user-list')

    def test_create_user_unauthorized(self):
        """Test 1: Bagair login kiye user list access nahi honi chahiye (403 Forbidden)"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_and_get_users(self):
        """Test 2: Login karne ke baad user list successfully milni chahiye (200 OK)"""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_serializer_fields(self):
        """Test 3: Serializer sahi fields (id, username, email, phone_number) return kar raha hai"""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.list_url)
        data = response.data
        user_data = data[0] if isinstance(data, list) else data['results'][0]
        self.assertIn('username', user_data)
        self.assertIn('email', user_data)
        self.assertIn('phone_number', user_data)
        self.assertEqual(user_data['username'], self.username)

    def test_custom_user_creation(self):
        """Test 4: Custom User model database mein theek tarah save ho raha hai"""
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)
        self.assertEqual(self.user.phone_number, "1234567890")

    def test_user_detail_endpoint(self):
        """Test 5: Specific user ki detail API se fetch ho sakti hai"""
        self.client.login(username=self.username, password=self.password)
        detail_url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], "test@example.com")