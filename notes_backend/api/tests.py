from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Note

class HealthTests(APITestCase):
    def test_health(self):
        url = reverse('Health')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Server is up!"})

class AuthTests(APITestCase):
    def test_register_login_logout(self):
        register_url = reverse('auth-register')
        login_url = reverse('auth-login')
        logout_url = reverse('auth-logout')
        user_url = reverse('auth-user')

        # Register user
        response = self.client.post(register_url, {"username": "foo", "email": "foo@b.com", "password": "bar123xyz"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("user", response.data)
        # User is auto-logged in after registration
        response = self.client.get(user_url)
        self.assertEqual(response.status_code, 200)

        # Logout
        response = self.client.post(logout_url)
        self.assertEqual(response.status_code, 200)

        # Not authenticated after logout
        response = self.client.get(user_url)
        self.assertEqual(response.status_code, 401)

        # Login
        response = self.client.post(login_url, {"username": "foo", "password": "bar123xyz"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("user", response.data)

        # Fetch user details authenticated
        response = self.client.get(user_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], "foo")

class NoteTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass123')
        self.other = User.objects.create_user(username='bob', password='passbob')

    def test_note_crud(self):
        self.client.login(username='alice', password='pass123')
        url = reverse('note-list-create')

        # Create note
        response = self.client.post(url, {'title': 'Test Note', 'content': 'This is a note.'})
        self.assertEqual(response.status_code, 201)
        note_id = response.data['id']

        # List notes
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Note')

        # Update note
        note_url = reverse('note-detail', args=[note_id])
        response = self.client.put(note_url, {'title': 'Renamed', 'content': 'Updated'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Renamed')

        # Retrieve note
        response = self.client.get(note_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Renamed')

        # Delete note
        response = self.client.delete(note_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Note.objects.count(), 0)

    def test_notes_cannot_be_seen_by_others(self):
        self.client.login(username='alice', password='pass123')
        url = reverse('note-list-create')
        # Create a note as alice
        response = self.client.post(url, {'title': 'Alice Note', 'content': ''})
        note_id = response.data['id']

        # Bob logs in and can't see Alice's note
        self.client.logout()
        self.client.login(username='bob', password='passbob')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 0)
        note_url = reverse('note-detail', args=[note_id])
        response = self.client.get(note_url)
        self.assertEqual(response.status_code, 404)
