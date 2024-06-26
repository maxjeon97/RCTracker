"""Tests for Flask Cafe."""


import os

os.environ["DATABASE_URL"] = "postgresql:///flaskcafe_test"
os.environ["FLASK_DEBUG"] = "0"

import re
from unittest import TestCase

from models import db, Cafe, City, User, CafeLike
from flask_bcrypt import Bcrypt

from app import app , CURR_USER_KEY, NOT_LOGGED_IN_MSG

bcrypt = Bcrypt()

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# Don't req CSRF for testing
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()

NOT_LOGGED_IN_MSG_AS_BYTES = NOT_LOGGED_IN_MSG.encode('utf-8')


#######################################
# helper functions for tests


def debug_html(response, label="DEBUGGING"):  # pragma: no cover
    """Prints HTML response; useful for debugging tests."""

    print("\n\n\n", "*********", label, "\n")
    print(response.data.decode('utf8'))
    print("\n\n")


def login_for_test(client, user_id):
    """Log in this user."""

    with client.session_transaction() as sess:
        sess[CURR_USER_KEY] = user_id


#######################################
# data to use for test objects / testing forms


CITY_DATA = dict(
    code="sf",
    name="San Francisco",
    state="CA"
)

CAFE_DATA = dict(
    name="Test Cafe",
    description="Test description",
    url="http://testcafe.com/",
    address="500 Sansome St",
    city_code="sf",
    image_url="http://testcafeimg.com/"
)

CAFE_DATA_EDIT = dict(
    name="new-name",
    description="new-description",
    url="http://new-image.com/",
    address="500 Sansome St",
    city_code="sf",
    image_url="http://new-image.com/"
)

TEST_USER_DATA = dict(
    username="test",
    first_name="Testy",
    last_name="MacTest",
    description="Test Description.",
    email="test@test.com",
    password="secret",
)

TEST_USER_DATA_EDIT = dict(
    first_name="new-fn",
    last_name="new-ln",
    description="new-description",
    email="new-email@test.com",
    image_url="http://new-image.com",
)

TEST_USER_DATA_NEW = dict(
    username="new-username",
    first_name="new-fn",
    last_name="new-ln",
    description="new-description",
    password="secret",
    email="new-email@test.com",
    image_url="http://new-image.com",
)

ADMIN_USER_DATA = dict(
    username="admin",
    first_name="Addie",
    last_name="MacAdmin",
    description="Admin Description.",
    email="admin@test.com",
    password="secret",
    admin=True,
)


#######################################
# homepage


class HomepageViewsTestCase(TestCase):
    """Tests about homepage."""

    def test_homepage(self):
        with app.test_client() as client:
            resp = client.get("/")
            self.assertIn(b'A Way to Keep Track of Your Favorite Restaurants and Cafes', resp.data)


#######################################
# cities


class CityModelTestCase(TestCase):
    """Tests for City Model."""

    def setUp(self):
        """Before all tests, add sample city & users"""

        Cafe.query.delete()
        City.query.delete()
        User.query.delete()

        sf = City(**CITY_DATA)
        db.session.add(sf)

        cafe = Cafe(**CAFE_DATA)
        db.session.add(cafe)

        user = User(**TEST_USER_DATA)
        db.session.add(user)

        db.session.commit()

        self.cafe = cafe
        self.user_id = user.id

    def tearDown(self):
        """After each test, remove all cafes."""

        Cafe.query.delete()
        City.query.delete()
        User.query.delete()
        db.session.commit()

    # depending on how you solve exercise, you may have things to test on
    # the City model, so here's a good place to put that stuff.


#######################################
# cafes


class CafeModelTestCase(TestCase):
    """Tests for Cafe Model."""

    def setUp(self):
        """Before all tests, add sample city & users"""

        Cafe.query.delete()
        City.query.delete()
        User.query.delete()

        sf = City(**CITY_DATA)
        db.session.add(sf)

        cafe = Cafe(**CAFE_DATA)
        db.session.add(cafe)

        user = User(**TEST_USER_DATA)
        db.session.add(user)

        db.session.commit()

        self.cafe = cafe
        self.user_id = user.id

    def tearDown(self):
        """After each test, remove all cafes."""

        Cafe.query.delete()
        City.query.delete()
        User.query.delete()

        db.session.commit()

    def test_get_city_state(self):
        self.assertEqual(self.cafe.get_city_state(), "San Francisco, CA")


class CafeViewsTestCase(TestCase):
    """Tests for views on cafes."""

    def setUp(self):
        """Before all tests, add sample city & users"""

        Cafe.query.delete()
        City.query.delete()
        User.query.delete()

        sf = City(**CITY_DATA)
        db.session.add(sf)

        cafe = Cafe(**CAFE_DATA)
        db.session.add(cafe)

        user = User(**TEST_USER_DATA)
        db.session.add(user)

        db.session.commit()

        self.cafe_id = cafe.id
        self.user_id = user.id

    def tearDown(self):
        """After each test, remove all cafes."""

        Cafe.query.delete()
        City.query.delete()
        User.query.delete()

        db.session.commit()

    def test_list(self):
        with app.test_client() as client:
            login_for_test(client, self.user_id)

            resp = client.get("/cafes")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Test Cafe", resp.data)

    def test_detail(self):
        with app.test_client() as client:
            login_for_test(client, self.user_id)

            resp = client.get(f"/cafes/{self.cafe_id}")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Test Cafe", resp.data)
            self.assertIn(b'testcafe.com', resp.data)


class CafeAdminViewsTestCase(TestCase):
    """Tests for add/edit views on cafes."""

    def setUp(self):
        """Before each test, add sample city, users, and cafes"""

        City.query.delete()
        Cafe.query.delete()
        User.query.delete()

        sf = City(**CITY_DATA)
        db.session.add(sf)

        cafe = Cafe(**CAFE_DATA)
        db.session.add(cafe)

        user = User(**TEST_USER_DATA)
        db.session.add(user)

        admin = User(**ADMIN_USER_DATA)
        db.session.add(admin)

        db.session.commit()

        self.cafe_id = cafe.id
        self.user_id = user.id
        self.admin_id = admin.id

    def tearDown(self):
        """After each test, delete the cities."""

        Cafe.query.delete()
        City.query.delete()
        User.query.delete()

        db.session.commit()

    def test_add(self):
        with app.test_client() as client:
            login_for_test(client, self.admin_id)

            resp = client.get("/cafes/add")
            self.assertIn(b'Add Cafe', resp.data)

            resp = client.post(
                f"/cafes/add",
                data=CAFE_DATA_EDIT,
                follow_redirects=True)
            self.assertIn(b'added', resp.data)

    def test_add_unauthorized(self):
        with app.test_client() as client:
            login_for_test(client, self.user_id)

            resp = client.get("/cafes/add", follow_redirects=True)
            self.assertEqual(resp.status_code, 401)
            self.assertIn(b'UNAUTHORIZED', resp.data)
            self.assertNotIn(b'Add Cafe', resp.data)

            resp = client.post(
                f"/cafes/add",
                data=CAFE_DATA_EDIT,
                follow_redirects=True)
            self.assertEqual(resp.status_code, 401)
            self.assertIn(b'UNAUTHORIZED', resp.data)
            self.assertNotIn(b'added', resp.data)

    def test_dynamic_cities_vocab(self):
        id = self.cafe_id

        # the following is a regular expression for the HTML for the drop-down
        # menu pattern we want to check for
        choices_pattern = re.compile(
           r'<select [^>]*name="city_code"[^>]*><option [^>]*value="sf">' +
           r'San Francisco</option></select>')

        with app.test_client() as client:
            login_for_test(client, self.admin_id)

            resp = client.get("/cafes/add")
            self.assertRegex(resp.data.decode('utf8'), choices_pattern)

            resp = client.get(f"/cafes/{id}/edit")
            self.assertRegex(resp.data.decode('utf8'), choices_pattern)

    def test_edit(self):
        id = self.cafe_id

        with app.test_client() as client:
            login_for_test(client, self.admin_id)

            resp = client.get(f"/cafes/{id}/edit", follow_redirects=True)
            self.assertIn(b'Edit Cafe', resp.data)

            resp = client.post(
                f"/cafes/{id}/edit",
                data=CAFE_DATA_EDIT,
                follow_redirects=True)
            self.assertIn(b'edited', resp.data)

    def test_edit_unauthorized(self):
        id = self.cafe_id

        with app.test_client() as client:
            login_for_test(client, self.user_id)

            resp = client.get(f"/cafes/{id}/edit", follow_redirects=True)
            self.assertEqual(resp.status_code, 401)
            self.assertIn(b'UNAUTHORIZED', resp.data)
            self.assertNotIn(b'Edit Cafe', resp.data)

            resp = client.post(
                f"/cafes/{id}/edit",
                data=CAFE_DATA_EDIT,
                follow_redirects=True)
            self.assertEqual(resp.status_code, 401)
            self.assertIn(b'UNAUTHORIZED', resp.data)
            self.assertNotIn(b'edited', resp.data)

    def test_edit_form_shows_curr_data(self):
        id = self.cafe_id

        with app.test_client() as client:
            login_for_test(client, self.admin_id)

            resp = client.get(f"/cafes/{id}/edit", follow_redirects=True)
            self.assertIn(b'Test description', resp.data)


#######################################
# users


class UserModelTestCase(TestCase):
    """Tests for the user model."""

    def setUp(self):
        """Before each test, add sample users."""

        User.query.delete()

        user = User.register(**TEST_USER_DATA)
        db.session.add(user)

        db.session.commit()

        self.user = user

    def tearDown(self):
        """After each test, remove all users."""

        User.query.delete()
        db.session.commit()

    def test_authenticate(self):
        rez = User.authenticate("test", "secret")
        self.assertEqual(rez, self.user)

    def test_authenticate_fail(self):
        rez = User.authenticate("no-such-user", "secret")
        self.assertFalse(rez)

        rez = User.authenticate("test", "password")
        self.assertFalse(rez)

    def test_full_name(self):
        self.assertEqual(self.user.get_full_name(), "Testy MacTest")

    def test_register(self):
        u = User.register(**TEST_USER_DATA)
        # test that password gets bcrypt-hashed (all start w/$2b$)
        self.assertEqual(u.password[:4], "$2b$")
        db.session.rollback()


class AuthViewsTestCase(TestCase):
    """Tests for views on logging in/logging out/registration."""

    def setUp(self):
        """Before each test, add sample users."""

        User.query.delete()

        user = User.register(**TEST_USER_DATA)
        db.session.add(user)

        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """After each test, remove all users."""

        User.query.delete()
        db.session.commit()

    def test_signup(self):
        with app.test_client() as client:
            resp = client.get("/signup")
            self.assertIn(b'Sign Up', resp.data)

            resp = client.post(
                "/signup",
                data=TEST_USER_DATA_NEW,
                follow_redirects=True,
            )

            self.assertIn(b"Signed up successfully!", resp.data)

            with client.session_transaction() as sess:
                self.assertTrue(sess.get(CURR_USER_KEY))

    def test_signup_username_taken(self):
        with app.test_client() as client:
            resp = client.get("/signup")
            self.assertIn(b'Sign Up', resp.data)

            # signup with same data as the already-added user
            resp = client.post(
                "/signup",
                data=TEST_USER_DATA,
                follow_redirects=True,
            )

            self.assertIn(b"Username or email already taken", resp.data)

    def test_login(self):
        with app.test_client() as client:
            resp = client.get("/login")
            self.assertIn(b'Welcome Back!', resp.data)

            resp = client.post(
                "/login",
                data={"username": "test", "password": "WRONG"},
                follow_redirects=True,
            )

            self.assertIn(b"Invalid credentials", resp.data)

            resp = client.post(
                "/login",
                data={"username": "test", "password": "secret"},
                follow_redirects=True,
            )

            self.assertIn(b"Hello, test", resp.data)

            with client.session_transaction() as sess:
                self.assertEqual(sess.get(CURR_USER_KEY), self.user_id)

    def test_logout(self):
        with app.test_client() as client:
            login_for_test(client, self.user_id)

            resp = client.post("/logout", follow_redirects=True)

            self.assertIn(b"Successfully logged out!", resp.data)

            with client.session_transaction() as sess:
                self.assertEqual(sess.get(CURR_USER_KEY), None)


class NavBarTestCase(TestCase):
    """Tests navigation bar."""

    def setUp(self):
        """Before tests, add sample user."""

        User.query.delete()

        user = User.register(**TEST_USER_DATA)

        db.session.add_all([user])
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """After tests, remove all users."""

        User.query.delete()
        db.session.commit()

    def test_anon_navbar(self):
        with app.test_client() as client:
            resp = client.get("/")
            self.assertEqual(resp.status_code, 200)

            self.assertIn(b"A Way to Keep Track of Your Favorite Restaurants and Cafes", resp.data)
            self.assertIn(b"Sign Up", resp.data)
            self.assertIn(b"Log In", resp.data)
            self.assertNotIn(b"Log Out", resp.data)

    def test_logged_in_navbar(self):
        with app.test_client() as client:
            login_for_test(client, self.user_id)

            resp = client.get("/")
            self.assertEqual(resp.status_code, 200)

            self.assertIn(b"A Way to Keep Track of Your Favorite Restaurants and Cafes", resp.data)
            self.assertNotIn(b"Sign Up", resp.data)
            self.assertNotIn(b"Log In", resp.data)
            self.assertIn(b"Log Out", resp.data)
            self.assertIn(b"Testy MacTest", resp.data)


class ProfileViewsTestCase(TestCase):
    """Tests for views on user profiles."""

    def setUp(self):
        """Before each test, add sample user."""

        User.query.delete()

        user = User.register(**TEST_USER_DATA)
        db.session.add(user)

        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """After each test, remove all users."""

        User.query.delete()
        db.session.commit()

    def test_anon_profile(self):
        with app.test_client() as client:
            resp = client.get("/profile", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            self.assertIn(NOT_LOGGED_IN_MSG_AS_BYTES, resp.data)
            self.assertIn(b"Welcome Back!", resp.data)
            self.assertNotIn(b"Edit Your Profile", resp.data)

    def test_logged_in_profile(self):
        with app.test_client() as client:
            login_for_test(client, self.user_id)

            resp = client.get("/profile")
            self.assertEqual(resp.status_code, 200)

            self.assertIn(b"Testy MacTest", resp.data)
            self.assertIn(b"Username:", resp.data)
            self.assertIn(b"Email:", resp.data)
            self.assertIn(b"Edit Your Profile", resp.data)

    def test_anon_profile_edit(self):
        with app.test_client() as client:
            resp = client.post(
                "/profile/edit",
                data = TEST_USER_DATA_EDIT,
                follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            self.assertIn(NOT_LOGGED_IN_MSG_AS_BYTES, resp.data)
            self.assertIn(b"Welcome Back!", resp.data)
            self.assertNotIn(b"Profile edited!", resp.data)

    def test_logged_in_profile_edit(self):
        with app.test_client() as client:
            login_for_test(client, self.user_id)

            resp = client.post(
                "/profile/edit",
                data = TEST_USER_DATA_EDIT,
                follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            self.assertNotIn(b"Testy MacTest", resp.data)
            self.assertIn(b"Profile edited!", resp.data)
            self.assertIn(b"new-fn new-ln", resp.data)
            self.assertIn(b"new-description", resp.data)
            self.assertIn(b"new-email@test.com", resp.data)


#######################################
# likes


class LikeViewsTestCase(TestCase):
    """Tests for likes on cafes."""

    def setUp(self):
        """Before all tests, add sample city, cafes, users, and likes"""
        CafeLike.query.delete()
        Cafe.query.delete()
        City.query.delete()
        User.query.delete()

        sf = City(**CITY_DATA)
        db.session.add(sf)

        cafe = Cafe(**CAFE_DATA)
        db.session.add(cafe)

        user = User(**TEST_USER_DATA)
        db.session.add(user)

        user.liked_cafes.append(cafe)

        db.session.commit()

        self.cafe = cafe
        self.user_id = user.id

    def tearDown(self):
        """After each test, remove everything."""

        CafeLike.query.delete()
        Cafe.query.delete()
        City.query.delete()
        User.query.delete()

        db.session.commit()

    def test_likes_display_on_profile_has_likes(self):
        """Tests that a user with likes sees liked cafes on profile page"""
        with app.test_client() as client:
            login_for_test(client, self.user_id)

            resp = client.get('/profile')
            self.assertEqual(resp.status_code, 200)

            self.assertIn(b"Testy MacTest", resp.data)
            self.assertIn(b"Your Liked Cafes", resp.data)
            self.assertIn(b"Test Cafe", resp.data)

    def test_likes_display_on_profile_no_likes(self):
        """Tests that a user with no likes sees the correct message"""
        user2 = User(**TEST_USER_DATA_NEW)
        db.session.add(user2)
        db.session.commit()

        with app.test_client() as client:
            login_for_test(client, user2.id)

            resp = client.get('/profile')
            self.assertEqual(resp.status_code, 200)

            self.assertIn(b"new-fn new-ln", resp.data)
            self.assertIn(b"Your Liked Cafes", resp.data)
            self.assertIn(b"You have no liked cafes", resp.data)