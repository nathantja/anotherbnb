"""SQLAlchemy models for Anotherbnb."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)


### Table Relationships
# users 1:M listings
# users 1:M reservations M:1 listings
# users 1:M messages M:1 users
# listings 1:M images
# reservations M:1 listings
# reservations M:1 users

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

    subject = db.Column(
        db.String(100),
        nullable=False,
    )

    message = db.Column(
        db.String(10000),
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow()
    )

    # RELATIONSHIP
    sender = db.relationship('User', primaryjoin=(User.id == sender_user_id))
    recipient = db.relationship('User', primaryjoin=(User.id == recipient_user_id))


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
        db.String(1000),
        nullable=False,
        default=""
    )

    sq_ft = db.Column(
        db.Integer,
        db.CheckConstraint('sq_ft > 0'),
        nullable=False
    )

    max_guests = db.Column(
        db.Integer,
        db.CheckConstraint('max_guests > 0'),
        nullable=False
    )

    hourly_rate = db.Column(
        db.Numeric(10,2),
        db.CheckConstraint('hourly_rate > 0'),
        nullable=False
    )

    # RELATIONSHIP
    images = db.relationship('Image', backref='listing')
    user = db.relationship('User')



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
        db.ForeignKey('listings.id', ondelete='CASCADE'),
        nullable=False
    )

    original_filename = db.Column(
        db.String(255),
        nullable=False
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    url = db.Column(
        db.String(1000),
        nullable=False
    )


### RESERVATIONS ###############################################################


class Reservation(db.Model):
    """Reservations to link users to specific listings."""

    __tablename__ = 'reservations'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey('listings.id', ondelete='CASCADE'),
        nullable=False
    )

    start_date = db.Column(
        db.Date,
        nullable=False
    )

    start_time = db.Column(
        db.Time,
        nullable=False
    )

    hours = db.Column(
        db.Integer,
        db.CheckConstraint('hours > 0'),
        nullable=False
    )

    guests = db.Column(
        db.Integer,
        db.CheckConstraint('guests > 0'),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="requested"
    )

    # RELATIONSHIPS
    listing = db.relationship('Listing', backref='reservations')
    user = db.relationship('User', backref='reserved_by')