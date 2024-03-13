"""Data models for Flask Cafe"""


from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()

DEFAULT_CAFE_PIC = "/static/images/default-cafe.png"
DEFAULT_PROF_PIC = "/static/images/default-prof-pic.png"


class City(db.Model):
    """Cities for cafes."""

    __tablename__ = 'cities'

    code = db.Column(
        db.Text,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    state = db.Column(
        db.String(2),
        nullable=False,
    )


class Cafe(db.Model):
    """Cafe information."""

    __tablename__ = 'cafes'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(
        db.String(50),
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
        default=""
    )

    url = db.Column(
        db.Text,
        nullable=False,
        default=""
    )

    address = db.Column(
        db.Text,
        nullable=False,
    )

    city_code = db.Column(
        db.Text,
        db.ForeignKey('cities.code'),
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default=DEFAULT_CAFE_PIC,
    )

    city = db.relationship("City", backref='cafes')

    def __repr__(self):
        return f'<Cafe id={self.id} name="{self.name}">'

    def get_city_state(self):
        """Return 'city, state' for cafe."""

        city = self.city
        return f'{city.name}, {city.state}'


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    username = db.Column(
        db.String(30),
        nullable=False,
        unique=True,
    )

    admin = db.Column(
        db.Boolean,
        default=False
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False,
        default="",
    )

    image_url = db.Column(
        db.String(255),
        nullable=False,
        default=DEFAULT_PROF_PIC,
    )

    password = db.Column(
        db.String(100),
        nullable=False,
    )

    liked_cafes = db.relationship(
        'Cafe', secondary='likes', backref='liking_users')

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    def get_full_name(self):
        """Returns full name"""

        return f"{self.first_name} {self.last_name}"

    @classmethod
    def register(cls, username, email, first_name, last_name, password,
                 image_url=DEFAULT_PROF_PIC, admin=False, description=""):
        """Register user.

        Hashes password and returns the user instance.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=hashed_pwd,
            image_url=image_url or DEFAULT_PROF_PIC,
            admin=admin or False,
            description=description or ""
        )

        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        Searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        """

        user = cls.query.filter_by(username=username).one_or_none()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    # def has_liked(self, message):
    #     """Checks if this message is in likes. Returns True or False"""

    #     return message in self.likes


class Like(db.Model):
    """Through table that links users to cafes"""

    __tablename__ = 'likes'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True
    )

    cafe_id = db.Column(
        db.Integer,
        db.ForeignKey('cafes.id', ondelete="cascade"),
        primary_key=True
    )


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
