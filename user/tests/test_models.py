from django.test import TestCase
from django.utils import timezone
from user.models import NewUser, OTP


class NewUserModelTest(TestCase):

    def setUp(self):
        self.user = NewUser.objects.create(
            username='testuser',
            first_name='Test',
            last_name='User',
            phone_number='1234567890',
        )

    def test_new_user_creation(self):
        """Test creating a new user"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.phone_number, '1234567890')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_new_user_str(self):
        """Test string representation of NewUser"""
        self.assertEqual(str(self.user), 'testuser')


class OTPModelTest(TestCase):

    def setUp(self):
        self.user = NewUser.objects.create(
            username='testuser',
            first_name='Test',
            last_name='User',
            phone_number='1234567890',
        )
        self.otp = OTP.objects.create(
            user=self.user,
            otp='1234',
            attempts=0,
            created_at=timezone.now(),
        )

    def test_otp_creation(self):
        """Test creating an OTP instance"""
        self.assertEqual(self.otp.user, self.user)
        self.assertEqual(self.otp.otp, '1234')
        self.assertEqual(self.otp.attempts, 0)

    def test_otp_str(self):
        """Test string representation of OTP"""
        self.assertEqual(str(self.otp), 'OTP for testuser')
