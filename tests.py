from datetime import datetime, timedelta
import unittest

from app import (
    app,
    db,
)
from app.models import (
    Post,
    User,
)


class UserModelTestCase(unittest.TestCase):
    def setUp(self) -> None:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self) -> None:
        # Arrange
        user = User(username="susan")

        # Act
        user.set_password("cat")

        # Assert
        self.assertFalse(user.check_password("dog"))
        self.assertTrue(user.check_password("cat"))

    def test_avatar(self) -> None:
        # Arrange
        user = User(username="susan", email="susan@example.com")
        
        # Act
        pass

        # Assert
        self.assertEqual(
            user.avatar(128),
            "https://www.gravatar.com/avatar/f3fc30174d7fd74ab6ca3c36d198fcb9?d=identicon&s=128"
        )

    def test_follow(self) -> None:
        # Arrange
        u1 = User(username="susan", email="susan@example.com")
        u2 = User(username="john", email="john@example.com")

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        # Act 1: do nothing
        pass

        # Assert 1
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u1.followers.count(), 0)
        self.assertEqual(u2.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

        # Act 2: u1 follows u2
        u1.follow(u2)
        db.session.commit()

        # Assert 2
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, "john")
        self.assertEqual(u1.followers.count(), 0)
        self.assertEqual(u2.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, "susan")

        # Act 3: u1 unfollows u2
        u1.unfollow(u2)
        db.session.commit()

        # Assert 3: 
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u1.followers.count(), 0)
        self.assertEqual(u2.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # Arrange
        users = [
            User(username="john", email="john@example.com"),
            User(username="susan", email="susan@example.com"),
            User(username="mary", email="mary@example.com"),
            User(username="david", email="david@example.com"),
        ]

        posts = [Post(
            body=f"post from {user.username}",
            author=user,
            timestamp=datetime.utcnow() + timedelta(seconds=count+1),
        ) for count, user in enumerate(users)]

        db.session.add_all(users + posts)
        db.session.commit()

        # Act
        users[0].follow(users[1]) # john follows susan
        users[0].follow(users[3]) # john follows david
        users[1].follow(users[2]) # susan follows mary
        users[2].follow(users[3]) # mary follows david

        db.session.commit()

        # Assert
        followed = [user.followed_posts().all() for user in users]
        self.assertEqual(followed[0], [posts[3], posts[1], posts[0]])
        self.assertEqual(followed[1], [posts[2], posts[1]])
        self.assertEqual(followed[2], [posts[3], posts[2]])
        self.assertEqual(followed[3], [posts[3]])


if __name__ == "__main__":
    unittest.main(verbosity=2)
