from datetime import datetime, timedelta
import unittest

from app import create_app, db
from app.models import Post, User
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        susan = User(username='susan')
        susan.set_password('dog')
        self.assertFalse(susan.check_password('cat'))
        self.assertTrue(susan.check_password('dog'))

    def test_avatar(self):
        john = User(username='john', email='john@example.com')
        url = ('https://www.gravatar.com/avatar/d4c74594d'
               '841139328695756648b6bd6?d=identicon&s=128')
        self.assertEqual(john.avatar(128), url)

    def test_follow(self):
        john = User(username='john', email='john@example.com')
        susan = User(username='susan', email='susan@example.com')
        db.session.add(john)
        db.session.add(susan)
        db.session.commit()
        self.assertEqual(john.followed.all(), [])
        self.assertEqual(susan.followed.all(), [])

        john.follow(susan)
        db.session.commit()
        self.assertTrue(john.is_following(susan))
        self.assertEqual(john.followed.count(), 1)
        self.assertEqual(john.followed.first().username, 'susan')
        self.assertEqual(susan.followers.count(), 1)
        self.assertEqual(susan.followers.first().username, 'john')

        john.unfollow(susan)
        db.session.commit()
        self.assertFalse(john.is_following(susan))
        self.assertEqual(john.followed.count(), 0)
        self.assertEqual(susan.followers.count(), 0)

    def test_follow_posts(self):
        john = User(username='john', email='john@example.com')
        liam = User(username='liam', email='liam@example.com')
        gabe = User(username='gabe', email='gabe@example.com')
        rick = User(username='rick', email='rick@example.com')
        db.session.add_all([john, liam, gabe, rick])

        now = datetime.utcnow()
        post_1 = Post(body='john', author=john,
                      timestamp=now + timedelta(seconds=1))
        post_2 = Post(body='liam', author=liam,
                      timestamp=now + timedelta(seconds=4))
        post_3 = Post(body='gabe', author=gabe,
                      timestamp=now + timedelta(seconds=3))
        post_4 = Post(body='rick', author=rick,
                      timestamp=now + timedelta(seconds=2))
        db.session.add_all([post_1, post_2, post_3, post_4])
        db.session.commit()

        john.follow(liam)
        john.follow(rick)
        liam.follow(gabe)
        gabe.follow(rick)
        db.session.commit()

        followed_1 = john.followed_posts().all()
        followed_2 = liam.followed_posts().all()
        followed_3 = gabe.followed_posts().all()
        followed_4 = rick.followed_posts().all()

        self.assertEqual(followed_1, [post_2, post_4, post_1])
        self.assertEqual(followed_2, [post_2, post_3])
        self.assertEqual(followed_3, [post_3, post_4])
        self.assertEqual(followed_4, [post_4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
