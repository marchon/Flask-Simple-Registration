import functools
import re

import flask


class SimpleRegistration(object):

    def __init__(self, app, user_model, login_url, login_form, login_redirect,
            logout_url, logout_redirect, signup_url, signup_form,
            signup_redirect):

        self.login_url = login_url
        self.login_form = login_form
        self.login_redirect = login_redirect

        self.logout_url = logout_url
        self.logout_redirect = logout_redirect

        self.signup_url = signup_url
        self.signup_form = signup_form
        self.signup_redirect = signup_redirect

        app.before_request(self.before_request)

        app.add_url_rule(login_url, None, self.login, methods=["GET", "POST"])
        app.add_url_rule(signup_url, None, self.signup, methods=["GET", "POST"])
        app.add_url_rule(logout_url, None, self.logout)

    def before_request(self):
        flask.g.user = None
        if "user_id" in flask.session:
            flask.g.user = self.user_model.query.get(flask.session["user_id"])

    def login(self):
        if flask.request.method == "POST":
            form = self.login_form(flask.request.form)
            if form.validate():
                flask.g.user = form.user
                flask.session["user_id"] = flask.g.user.id
                flask.session.permanent = True
                if flask.request.args.get("next"):
                    next = flask.request.args["next"]
                    if '//' not in next and not re.match(r'[^\?]*//', next):
                        return flask.redirect(flask.request.args["next"])
                return flask.redirect(flask.url_for(self.login_redirect))
            flask.flash("Sorry, there was an error!", category="error")
        else:
            form = self.login_form()
        return flask.render_template("login.html", form=form)

    def logout(self):
        del flask.session["user_id"]
        return flask.redirect(flask.url_for(self.logout_redirect))

    def signup(self):
        if flask.request.method == "POST":
            form = self.signup_form(flask.request.form)
            if form.validate():
                user = form.save()
                flask.g.user = user
                flask.session["user_id"] = user.id
                flask.session.permanent = True
                return flask.redirect(flask.url_for(self.signup_redirect))
            flask.flash("Sorry, there was an error!", category="error")
        else:
            form = self.signup_form()
        return flask.render_template("signup.html", form=form)


def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if flask.g.user is None:
            return flask.redirect(flask.url_for('login',
                next=flask.request.path))
        return f(*args, **kwargs)
    return decorated_function
