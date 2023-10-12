import os
from dotenv import load_dotenv

from flask import Flask, session, g, flash, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
from werkzeug.utils import secure_filename
import uuid

from forms import UserAddForm, CSRFProtectForm, LoginForm, ListingAddForm
from models import db, connect_db, User, Listing, Image
# Reservation, Message
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

        flash("Successfully Logged out.", "success")
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

    listings = Listing.query.all()

    if g.user:
        return render_template("listings.html", listings=listings)

    else:
        return render_template("listings-guest.html", listings=listings)


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
                status=form.status.data
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
        return render_template("listings-new.html", form=form)


# @app.route('/listings/<int:id>/reserve', methods=['GET', 'POST'])
# def reserve_listing(id):



### Homepage (Redirect) ########################################################

@app.get('/')
def homepage():
    """Redirect to /listings"""

    return redirect("/listings")
