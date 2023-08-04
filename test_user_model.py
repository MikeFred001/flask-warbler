"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from flask import session
from models import db, User, Message, Follow, DEFAULT_IMAGE_URL, bcrypt

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        u1 = User.query.get(self.u1_id)
        u1_hash_check = bcrypt.check_password_hash(u1.password, "password")

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)
        self.assertEqual(len(u1.liked_messages), 0)

        self.assertEqual(u1.username, "u1")
        self.assertEqual(u1.email, "u1@email.com")
        self.assertEqual(u1.image_url, DEFAULT_IMAGE_URL)
        self.assertTrue(u1_hash_check) #different hashes?


class TestUserMethods(TestCase):

    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

    def tearDown(self):
        db.session.rollback()

    def test_is_following(self):
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        # detect that u2 is not following u1, then check if u2 is following u1
        self.assertNotIn(u2, u1.following)

        u1.following.append(u2)

        self.assertIn(u2, u1.following)

        # detect that u1 is not following u2, then check if u1 is following u2
        self.assertNotIn(u1, u2.following)

        u2.following.append(u1)

        self.assertIn(u1, u2.following)


    def test_is_followed_by(self):
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        # detect that u2 is not a follwer of u1, then check if u2 is a follower of u1
        self.assertNotIn(u2, u1.followers)

        u1.followers.append(u2)

        self.assertIn(u2, u1.followers)

        # detect that u1 is not a follower of u2, then check if u1 is a follower of u2
        self.assertNotIn(u1, u2.followers)

        u2.followers.append(u1)

        self.assertIn(u1, u2.followers)


    def test_user_signup(self):

        # call signup passing in username, email, password, image_url=DEFAULT_IMAGE_URL
        # test that user is in session and that user has same values

        u1 = User.query.get(self.u1_id)

        signed_up_user = User.signup(u1.username, u1.email, u1.password, u1.image_url)

        u1_hash_check = bcrypt.check_password_hash(u1.password, "password")

        self.assertEqual(signed_up_user.username, u1.username)
        self.assertEqual(signed_up_user.email, u1.email)
        self.assertEqual(signed_up_user.image_url, u1.image_url)
        self.assertIn(signed_up_user, db.session)
        self.assertTrue(u1_hash_check)


    def test_user_authenticate(self):
        """Tests user authentication method"""

        u1 = User.query.get(self.u1_id)

        auth_user = User.authenticate(u1.username, "password")

        self.assertTrue(auth_user)
        self.assertFalse(User.authenticate("hello", u1.password))
        self.assertFalse(User.authenticate(u1.username, "notpassword"))


