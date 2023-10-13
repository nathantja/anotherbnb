import os
from dotenv import load_dotenv

from flask import Flask, session, g, flash, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
from werkzeug.utils import secure_filename
import uuid

from forms import (
    UserAddForm,
    CSRFProtectForm,
    LoginForm,
    ListingAddForm,
    ReservationAddForm,
    MessageComposeForm,
)
from models import db, connect_db, User, Listing, Image, Reservation, Message
from utils import upload_to_S3, BUCKET_IMG_BASE_URL, validate_image_extensions

load_dotenv()

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']

toolbar = DebugToolbarExtension(app)

connect_db(app)


### Before/After Request #######################################################

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.before_request
def add_CSRF_to_g():
    """Adds a global property to access the CSRFProtectForm"""

    g.csrf_form = CSRFProtectForm()


@app.after_request
def add_header(response):
    """Add non-caching headers on every request."""

    response.cache_control.no_store = True
    return response


### User Signup/login/Logout ###################################################

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Log out user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Display the signup form or process the form.

    Add new user to database, then redirect to homepage.
    If form not valid, present form.
    If username not unique, flash message.
    """

    do_logout()

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", "danger")
            return render_template("users/signup.html", form=form)

        do_login(user)

        flash("Successfully logged in", "success")
        return redirect("/")

    else:
        return render_template("users/signup.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Display the signup form or process the form.

    Redirect to homepage on success.
    """

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            form.username.data,
            form.password.data,
        )

        if user:
            do_login(user)
            flash(f"Welcome back, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", "danger")

    return render_template("users/login.html", form=form)


@app.post('/logout')
def logout():
    """Handle logout of user and redirect to homepage."""

    if g.csrf_form.validate_on_submit():
        do_logout()

        flash("Successfully logged out", "success")
        return redirect("/")

    else:
        raise Unauthorized()


### Listings ###################################################################

@app.get('/listings')
def listings():
    """Show listings.

    Guest/Anon: only show listings
    Logged In: show UI to interact with listings
    """

    q = request.args.get('q', '')

    if q:
        listings = (Listing
                    .query
                    .filter(Listing.title.ilike(f'%{q}%') |
                            Listing.description.ilike(f'%{q}%'))
                    .all())

    else:
        listings = Listing.query.all()

    if g.user:
        return render_template("listings.html", listings=listings, q=q)

    else:
        return render_template("listings-guest.html", listings=listings, q=q)


@app.get('/listings/<int:id>')
def listing_id(id):
    """Show listing based on URL parameter. Requires sign-in."""

    if not g.user:
        flash("Signup or login to view listing", "warning")
        return redirect("/")

    listing = Listing.query.get_or_404(id)
    return render_template("listing.html", listing=listing)


@app.route('/listings/new', methods=['GET', 'POST'])
def new_listing():
    """Display new listing form or process the form.

    Add new listing to database, then redirect to listings.
    If form not valid, present form.
    """

    if not g.user:
        flash("Signup or login to add listing", "warning")
        return redirect("/")

    form = ListingAddForm()

    if form.validate_on_submit():

        if not validate_image_extensions(form.images.data):
            flash("Only png, jpg, & jpeg extensions supported.", "danger")
            return redirect("/listings/new")

        else:
            listing = Listing(
                user_id=g.user.id,
                title=form.title.data,
                description=form.description.data,
                sq_ft=form.sq_ft.data,
                max_guests=form.max_guests.data,
                hourly_rate=form.hourly_rate.data,
            )
            db.session.add(listing)
            db.session.commit()

            for image in form.images.data:
                original_filename = secure_filename(image.filename)
                extension = original_filename.rsplit(".", 1)[1].lower()
                uuid_filename = uuid.uuid4().hex + "." + extension
                upload_to_S3(image, uuid_filename)

                db_image = Image(
                    listing_id=listing.id,
                    original_filename=original_filename,
                    filename=uuid_filename,
                    url=f"{BUCKET_IMG_BASE_URL}/{uuid_filename}"
                )

                db.session.add(db_image)
                db.session.commit()

            flash("Successfully added listing", "success")
            return redirect(f"/listings/{listing.id}")

    else:
        return render_template("listing-new.html", form=form)


@app.route('/listings/<int:id>/reserve', methods=['GET', 'POST'])
def request_listing_reservation(id):
    """Display reservation form or process the request.

    Add new reservation to database, then redirect to user's reservations.
    If form not valid, present form.
    """

    if not g.user:
        flash("Signup or login to make reservation", "warning")
        return redirect("/")

    listing = Listing.query.get_or_404(id)

    if listing.user_id == g.user.id:
        flash("You cannot make a reservation for your own listing", "warning")
        return redirect(f"/listings/{id}")

    form = ReservationAddForm()

    if form.validate_on_submit():
        start_date = form.start_date.data
        start_time = form.start_time.data
        hours = form.hours.data
        guests = form.guests.data

        reservation = Reservation(
            user_id=g.user.id,
            listing_id=listing.id,
            start_date=start_date,
            start_time=start_time,
            hours=hours,
            guests=guests
        )

        db.session.add(reservation)
        db.session.commit()

        flash("Successfully requested", "success")
        return redirect(f"/reservations/me")

    else:
        return render_template("listing-reserve.html",
                               form=form,
                               listing=listing)


### Reservations ###############################################################

@app.get('/reservations/me')
def my_reservations():
    """Display user's reservations."""

    if not g.user:
        flash("Signup or login to see reservations", "warning")
        return redirect("/")

    reservations = (Reservation
                    .query
                    .filter(Reservation.user_id == g.user.id)
                    .all())

    return render_template("reservations-me.html", reservations=reservations)


@app.get('/reservations/manage')
def manage_reservations():
    """Portal to manage reservation requests from other users."""

    if not g.user:
        flash("Signup or login to access.", "warning")
        return redirect("/")

    user_listings = Listing.query.filter(Listing.user_id == g.user.id).all()
    user_listings_ids = [listing.id for listing in user_listings]

    reservations = (Reservation
                    .query
                    .filter(Reservation.listing_id.in_(user_listings_ids))
                    .all())

    return render_template("reservations-manage.html", reservations=reservations)


@app.post('/reservations/<int:id>/approve')
def approve_reservation(id):
    """Set status for reservation to 'approved'."""

    if not g.user or not g.csrf_form.validate_on_submit():
        raise Unauthorized()

    reservation = Reservation.query.get_or_404(id)

    if g.user.id != reservation.listing.user_id:
        raise Unauthorized()

    reservation.status = 'approved'
    db.session.commit()

    return redirect("/reservations/manage")


@app.post('/reservations/<int:id>/deny')
def deny_reservation(id):
    """Set status for reservation to 'denied'."""

    if not g.user or not g.csrf_form.validate_on_submit():
        raise Unauthorized()

    reservation = Reservation.query.get_or_404(id)

    if g.user.id != reservation.listing.user_id:
        raise Unauthorized()

    reservation.status = 'denied'
    db.session.commit()

    return redirect("/reservations/manage")


### Messages ###################################################################

@app.route('/messages/compose', methods=['GET', 'POST'])
def compose_message():
    """Show form to compose message or process the message.

    Can take 'recipient_username' param in query string to prefill username.
    Can take 'subject' param in query string to prefill subject.
    """

    if not g.user:
        flash("Signup or login to send message", "warning")
        return redirect("/")

    recipient_username = request.args.get('recipient_username')
    subject = request.args.get('subject')

    form = MessageComposeForm(recipient_username=recipient_username,
                              subject=subject)

    if form.validate_on_submit():
        recipient = User.query.filter(
            User.username == form.recipient_username.data).first()

        if not recipient:
            flash("Username does not exist", "danger")
            return redirect("/messages/compose")

        message = Message(
            sender_user_id=g.user.id,
            recipient_user_id=recipient.id,
            subject=form.subject.data,
            message=form.message.data
        )

        db.session.add(message)
        db.session.commit()

        flash("Message sent successfully", "success")
        return redirect("/messages/compose")

    else:
        return render_template("messages-compose.html", form=form)


@app.get('/messages/inbox')
def messages_inbox():
    """View all messages received."""

    if not g.user:
        flash("Signup or login to view messages", "warning")
        return redirect("/")

    messages = Message.query.filter(Message.recipient_user_id==g.user.id).all()

    return render_template("messages-inbox.html", messages=messages)


@app.get('/messages/sent')
def messages_sent():
    """View all messages sent."""

    if not g.user:
        flash("Signup or login to view messages", "warning")
        return redirect("/")

    messages = Message.query.filter(Message.sender_user_id==g.user.id).all()

    return render_template("messages-sent.html", messages=messages)




### Homepage (Redirect) ########################################################

@app.get('/')
def homepage():
    """Redirect to /listings"""

    return redirect("/listings")
