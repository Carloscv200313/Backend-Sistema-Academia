from django.test import TestCase
from rest_framework.test import APIClient
from myapp.models import Usuario, Docente
# Note: It is highly recommended to use Django's built-in user model
# and password hashing instead of storing plain text passwords.
# The current implementation has security vulnerabilities.

class LoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a user and a teacher for testing
        self.user = Usuario.objects.create(
            id_usuario='testuser',
            codigo_usuario='docente01',
            contrasena_usuario='testpassword',
            rol='docente'
        )
        self.docente = Docente.objects.create(
            id_docente='testdocente',
            id_usuario=self.user,
            nombre_docente='Test Docente'
        )

    def test_successful_login(self):
        """
        Ensure a user can log in with valid credentials.
        """
        data = {
            'username': 'docente01',
            'password': 'testpassword',
            'role': 'docente'
        }
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_failed_login_invalid_password(self):
        """
        Ensure a user cannot log in with an invalid password.
        """
        data = {
            'username': 'docente01',
            'password': 'wrongpassword',
            'role': 'docente'
        }
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_failed_login_invalid_username(self):
        """
        Ensure a user cannot log in with an invalid username.
        """
        data = {
            'username': 'wronguser',
            'password': 'testpassword',
            'role': 'docente'
        }
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_failed_login_invalid_role(self):
        """
        Ensure a user cannot log in with an invalid role.
        """
        data = {
            'username': 'docente01',
            'password': 'testpassword',
            'role': 'alumno' # Correct credentials, but wrong role
        }
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, 401)
