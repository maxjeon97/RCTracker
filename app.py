"""Flask App for Flask Cafe."""

import os
from dotenv import load_dotenv

from flask import Flask, render_template, flash, redirect, jsonify, session, g
from flask import request
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cafe, City, User

from forms import CSRFProtectForm, CafeInfoForm, UserSignupForm, LoginForm
from forms import ProfileEditForm, AddCityForm

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY")

if app.debug:
    app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

#######################################
# auth & auth routes

CURR_USER_KEY = "curr_user"
NOT_LOGGED_IN_MSG = "You are not logged in!"


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.before_request
def add_csrf_form_to_g():
    """Adds csrf protection form to Flask global"""

    g.csrf_form = CSRFProtectForm()


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handles user signup.

    If form is valid, create new user and add to DB. Redirect to cafe list.

    If form not valid, present form.

    If there already is a user with that username or email: flash message
    and re-present form.
    """

    do_logout()

    form = UserSignupForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                description=form.description.data,
                email=form.email.data,
                password=form.password.data,
                image_url=form.image_url.data or User.image_url.default.arg
            )

            db.session.add(user)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()

            flash("Username or email already taken!", 'danger')
            return render_template('auth/signup-form.html', form=form)

        do_login(user)

        flash('Signed up successfully! You are now logged in.', 'success')
        return redirect("/cafes")

    else:
        return render_template('auth/signup-form.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handles user login and redirects to cafe list on success."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            form.username.data,
            form.password.data
        )

        if user:
            do_login(user)

            flash(f"Hello, {user.username}!", "success")
            return redirect("/cafes")

        flash("Invalid credentials!", 'danger')

    return render_template('auth/login-form.html', form=form)


@app.post('/logout')
def logout():
    """Handle logout of user and redirect to login page."""

    if not g.user:
        flash(NOT_LOGGED_IN_MSG, "danger")
        return redirect("/login")

    if g.csrf_form.validate_on_submit():
        do_logout()

        flash("Successfully logged out!", 'success')
        return redirect('/login')

    else:
        raise Unauthorized()


#######################################
# homepage and error pages

@app.get("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.errorhandler(Unauthorized)
def page_unauthorized(e):
    """Shows Unauthorized page."""

    return render_template('unauthorized.html'), 401


@app.errorhandler(404)
def page_not_found(e):
    """Shows 404 NOT FOUND page."""

    return render_template('404.html'), 404


#######################################
# cafes


@app.get('/cafes')
def cafe_list():
    """Return list of all cafes."""

    if not g.user:
        flash(NOT_LOGGED_IN_MSG, "danger")
        return redirect("/login")

    cafes = Cafe.query.order_by('name').all()

    return render_template(
        'cafe/list.html',
        cafes=cafes,
    )


@app.get('/cafes/<int:cafe_id>')
def cafe_detail(cafe_id):
    """Show detail for cafe."""

    if not g.user:
        flash(NOT_LOGGED_IN_MSG, "danger")
        return redirect("/login")

    cafe = Cafe.query.get_or_404(cafe_id)

    return render_template(
        'cafe/detail.html',
        cafe=cafe,
    )


@app.route('/cafes/add', methods=['GET', 'POST'])
def add_cafe():
    """Renders form for adding a cafe or handles adding of a cafe"""

    if not g.user:
        flash(NOT_LOGGED_IN_MSG, "danger")
        return redirect("/login")

    if not g.user.admin:
        raise Unauthorized()

    form = CafeInfoForm()

    cities_in_db = [(city.code, city.name)
                    for city in City.query
                    .order_by('name')
                    .all()]

    form.city_code.choices = cities_in_db

    if form.validate_on_submit():
        cafe = Cafe(
            name=form.name.data,
            description=form.description.data,
            url=form.url.data,
            address=form.address.data,
            city_code=form.city_code.data,
            image_url=form.image_url.data or Cafe.image_url.default.arg
        )

        db.session.add(cafe)

        db.session.flush()
        cafe.save_cafe_map()

        db.session.commit()

        flash(f"{cafe.name} added!", "success")
        return redirect(f'/cafes/{cafe.id}')

    return render_template('cafe/add-form.html', form=form)


@app.route('/cafes/<int:cafe_id>/edit', methods=['GET', 'POST'])
def edit_cafe(cafe_id):
    """Renders form for editing a cafe or handles editing of a cafe"""

    if not g.user:
        flash(NOT_LOGGED_IN_MSG, "danger")
        return redirect("/login")

    if not g.user.admin:
        raise Unauthorized()

    cafe = Cafe.query.get_or_404(cafe_id)

    form = CafeInfoForm(obj=cafe)

    cities_in_db = [(city.code, city.name)
                    for city in City.query
                    .order_by('name')
                    .all()]

    form.city_code.choices = cities_in_db

    if form.validate_on_submit():
        form.populate_obj(cafe)

        # if empty string is given in image_url field, set it to the default
        if not form.image_url.data:
            cafe.image_url = Cafe.image_url.default.arg

        db.session.flush()
        cafe.save_cafe_map()

        db.session.commit()

        flash(f"{cafe.name} edited!", "success")
        return redirect(f'/cafes/{cafe.id}')

    # if we used the default picture, prepopulate with empty string
    if cafe.image_url == Cafe.image_url.default.arg:
        form.image_url.data = ""

    return render_template('cafe/edit-form.html', form=form, cafe=cafe)


@app.post('/cafes/<int:cafe_id>/delete')
def delete_cafe(cafe_id):
    """Deletes cafe. Only admins may perform this action"""

    if not g.user:
        flash(NOT_LOGGED_IN_MSG, "danger")
        return redirect("/login")

    if not g.user.admin:
        raise Unauthorized()

    cafe = Cafe.query.get_or_404(cafe_id)

    if g.csrf_form.validate_on_submit():
        cafe.delete_map()

        db.session.delete(cafe)
        db.session.commit()

        flash('Cafe deleted!', 'success')
        return redirect("/cafes")

    else:
        raise Unauthorized()


#######################################
# cities

@app.get('/cities')
def city_list():
    """Render list of all cities."""

    if not g.user:
        flash(NOT_LOGGED_IN_MSG, "danger")
        return redirect("/login")

    cities = City.query.order_by('name').all()

    return render_template(
        'city/list.html',
        cities=cities,
    )

@app.route('/cities/add', methods=['GET', 'POST'])
def add_city():
    """Renders form for adding a city or handles adding of a city"""

    if not g.user:
        flash(NOT_LOGGED_IN_MSG, "danger")
        return redirect("/login")

    if not g.user.admin:
        raise Unauthorized()

    form = AddCityForm()

    if form.validate_on_submit():
        city = City(code=form.code.data,
                    name=form.name.data,
                    state=form.state.data)

        db.session.add(city)
        db.session.commit()

        flash(f"{city.name} added!", "success")
        return redirect('/cities')

    return render_template('city/add-form.html', form=form)


#######################################
# profile


@app.get('/profile')
def user_profile():
    """Renders user profile page."""

    if not g.user:
        flash(NOT_LOGGED_IN_MSG, "danger")
        return redirect("/login")

    return render_template('profile/detail.html')


@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    """Renders form for editing user profile or handles edit POST request"""

    if not g.user:
        flash(NOT_LOGGED_IN_MSG, "danger")
        return redirect("/login")

    form = ProfileEditForm(obj=g.user)

    if form.validate_on_submit():
        form.populate_obj(g.user)

        if not form.image_url.data:
            g.user.image_url = User.image_url.default.arg

        db.session.commit()

        flash("Profile edited!", "success")
        return redirect('/profile')

    # if we used the default picture, prepopulate with empty string
    if g.user.image_url == User.image_url.default.arg:
        form.image_url.data = ""

    return render_template('profile/edit-form.html', form=form)


#######################################
# API likes


@app.get("/api/likes")
def check_like():
    """Given a cafe_id in the URL query string, check to see whether the
    current user likes that cafe. Returns JSON: {"likes": true|false}"""

    if not g.user:
        flash(NOT_LOGGED_IN_MSG, "danger")
        return redirect("/login")

    cafe_id = int(request.args.get("q"))

    cafe = Cafe.query.get_or_404(cafe_id)

    if g.user.has_liked(cafe):
        return jsonify({
            "likes": "true"
        })
    else:
        return jsonify({
            "likes": "false"
        })


@app.post('/api/likes-toggle')
def toggle_cafe_like():
    """Like and unlike a cafe"""

    if not g.user:
        flash(NOT_LOGGED_IN_MSG, "danger")
        return redirect("/")

    cafe_id = int(request.json.get("cafe_id"))

    cafe = Cafe.query.get_or_404(cafe_id)

    if g.user.has_liked(cafe):
        g.user.liked_cafes.remove(cafe)
        db.session.commit()

        return jsonify({"unliked": cafe_id})
    else:
        g.user.liked_cafes.append(cafe)
        db.session.commit()

        return jsonify({"liked": cafe_id})