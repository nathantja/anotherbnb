import os

os.environ['DATABASE_URL'] = "postgresql:///anotherbnb_test"

from app import app, IntegrityError
from unittest import TestCase

from models import db, User

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):

    def setUp(self):
        """Delete all users, then create 2."""

        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password")
        u2 = User.signup("u2", "u2@email.com", "password")

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_signup_valid(self):
        """Test User.signup class method when inputs are valid"""

        u3 = User.signup("u3", "u3@email.com", "password")
        db.session.add(u3)
        db.session.commit()

        self.assertIsInstance(u3, User)
        self.assertEqual(u3.username, "u3")
        self.assertEqual(u3.email, "u3@email.com")
        self.assertNotEqual(u3.password, "password")
        self.assertIn("$2b$12$", u3.password)


    def test_user_signup_invalid(self):
        """Test User.signup class method when inputs are invalid"""

        try:
            u3 = User.signup("u1", "u1@email.com", "password")
            db.session.add(u3)
            db.session.commit()

        except IntegrityError:
            failed_duplicate_username = True
            db.session.rollback()

        try:
            User.signup("u5")

        except TypeError:
            failed_missing_fields = True

        self.assertEqual(failed_duplicate_username, True)
        self.assertEqual(failed_missing_fields, True)

