import os
from dotenv import load_dotenv

from flask import Flask, session, g, flash, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
from werkzeug.utils import secure_filename

from forms import UserAddForm, CSRFProtectForm, LoginForm, ListingAddForm
from models import db, connect_db, User, Listing
# Reservation, Image, Message
from utils import uploadToS3

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
        return redirect("/login")

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


@app.route('/listings/new', methods=['GET', 'POST'])
def new_listing():
    """Display new listing form or process the form.

    Add new listing to database, then redirect to listings.
    If form not valid, present form.
    """

    form = ListingAddForm()

    if form.validate_on_submit():
        # TODO: check file extension before upload



        listing = Listing(
            user_id=g.user.id,
            title=form.title.data,
            description=form.description.data,
            status=form.status.data
        )
        db.session.add(listing)
        db.session.commit()

        print(listing.id)


        for image in form.images.data:


            original_filename = secure_filename(image.filename)
            unique_filename =

            uploadToS3(image, "pickle.png")





        flash("Successfully added listing", "success")
        return redirect("/listings")

    else:
        return render_template("listings-new.html", form=form)


### Homepage (Redirect) ########################################################

@app.get('/')
def homepage():
    """Redirect to /listings"""

    return redirect("/listings")
