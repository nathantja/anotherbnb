"""SQLAlchemy models for Anotherbnb. """

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from aws_utils import BUCKET_NAME, AWS_REGION

db = SQLAlchemy()
bcrypt = Bcrypt()


# TODO: need db relationships


### USERS ######################################################################

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(30),
        nullable=False,
        unique=True,
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.String(100),
        nullable=False,
    )

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user - hashes password, adds user to database, and returns
        user."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(
            username=username,
            email=email,
            password=hashed_pwd
            )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and check password via bcrypt hash.
        returns user object if authenticated OR False."""

        user = cls.query.filter_by(username=username).one_or_none()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


### MESSAGES ###################################################################

class Message(db.Model):
    """Messages stored in a join table to connect users to itself."""

    __tablename__ = 'messages'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    sender_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    recipient_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    message = db.Column(
        db.String(10000),
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )


### LISTINGS ###################################################################

class Listing(db.Model):
    """Listing information for a space to rent on anotherbnb."""

    __tablename__ = 'listings'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    title = db.Column(
        db.String(30),
        nullable=False,
    )

    description = db.Column(
        db.String(30),
        nullable=False,
        default=""
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="available"
    )


### IMAGES #####################################################################

class Image(db.Model):
    """Image information for a listing including AWS S3 bucket name and
    region."""

    __tablename__ = 'images'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey('listings.id', ondelete='CASCADE')
    )

    original_filename = db.Column(
        db.String(255),
        nullable=False
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    bucket = db.Column(
        db.String(63),
        nullable=False,
        default=BUCKET_NAME
    )

    region = db.Column(
        db.String(63),
        nullable=False,
        default=AWS_REGION
    )

### RESERVATIONS ###############################################################

class Reservation(db.Model):
    """Reservations to link users to specific listings."""

    __tablename__ = 'reservations'

