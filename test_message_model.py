
import os
from unittest import TestCase
from models import db, User, Message

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

db.drop_all()
db.create_all()


class MessageModelTestCase(TestCase):
    """Testing Message Model"""
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        m1 = Message(
            text="test message",
            timestamp=None
        )

        u1.messages.append(m1)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

    def tearDown(self):
        db.session.rollback()


    def test_message_model(self):
        """Testing message model"""

        u1 = User.query.get(self.u1_id)
        self.assertEqual(len(u1.messages), 1)

        m2 = Message(
                    text="test message 2",
                    timestamp=None
        )
        u1.messages.append(m2)
        db.session.commit()

        self.assertEqual(len(u1.messages), 2)
        self.assertIn(m2, u1.messages)
        self.assertEqual(m2.text, "test message 2")