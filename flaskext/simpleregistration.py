import re

import flask


def provide_user(user):
    flask.g.user = None
    if "user_id" in flask.session:
        flask.g.user = user.query.get(flask.session["user_id"])


def login(form, redirect):
    if flask.request.method == "POST":
        form = form(flask.request.form)
        if form.validate():
            flask.g.user = form.user
            flask.session["user_id"] = flask.g.user.id
            flask.session.permanent = True
            if flask.request.args.get("next"):
                next = flask.request.args["next"]
                if '//' not in next and not re.match(r'[^\?]*//', next):
                    return flask.redirect(flask.request.args["next"])
            return flask.redirect(redirect)
        flask.flash("Sorry, there was an error!", category="error")
    return flask.render_template("login.html", form=form)


def logout(redirect):
    del flask.session["user_id"]
    return flask.redirect(redirect)


def signup(form, redirect):
    if flask.request.method == "POST":
        form = form(flask.request.form)
        if form.validate():
            user = form.save()
            flask.g.user = user
            flask.session["user_id"] = user.id
            flask.session.permanent = True
            return flask.redirect(redirect)
        flask.flash("Sorry, there was an error!", category="error")
    return flask.render_template("signup.html", form=form)
