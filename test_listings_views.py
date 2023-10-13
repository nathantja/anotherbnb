import os

os.environ['DATABASE_URL'] = "postgresql:///anotherbnb_test"

from app import app, CURR_USER_KEY
from unittest import TestCase

from models import db, Listing, User


# FIXME: BROKEN

class ListingBaseViewTestCase(TestCase):
    def setUp(self):
        """Create 2 users and 1 listing."""

        User.query.delete()
        Listing.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password")
        u2 = User.signup("u2", "u2@email.com", "password")

        self.u1_id = u1.id
        self.u2_id = u2.id

        listing1 = Listing(
            user_id=u1.id,
            title="Listing title",
            description="Listing description",
            sq_ft=10,
            max_guests=4,
            hourly_rate=25,
        )

        db.session.add(listing1)

        self.listing1_id = listing1.id

        db.session.commit()

        self.client = app.test_client()


class ListingViewTestCase(ListingBaseViewTestCase):
    def test_view_listing(self):
        """View a listing"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.get(f"/listings/{self.m1_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Listing title', html)