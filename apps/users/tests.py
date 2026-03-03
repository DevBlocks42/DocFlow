from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class AuthenticationTestCase(TestCase):

    def setUp(self):
        # Crée un utilisateur admin pour le test
        self.user = User.objects.create_user(
            email='admin@example.com',
            username='adminuser',
            password='MotDePasse123',
            role='admin'
        )
        self.user.save()

    def test_authentication_success(self):
        # Tenter d'authentifier l'utilisateur
        user = authenticate(email='admin@example.com', password='MotDePasse123')
        self.assertIsNotNone(user) 
        self.assertEqual(user.role, 'admin') 

    def test_authentication_fail_wrong_password(self):
        # Tenter d'authentifier avec un mauvais mot de passe
        user = authenticate(email='admin@example.com', password='WrongPassword')
        self.assertIsNone(user)  

    def test_authentication_fail_wrong_email(self):
        # Tenter d'authentifier avec un email inconnu
        user = authenticate(email='inconnu@example.com', password='MotDePasse123')
        self.assertIsNone(user) 