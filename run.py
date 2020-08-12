import os
from flask import Flask, render_template, redirect, request, url_for, session, flash

from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt

from flask_pymongo import PyMongo
if os.path.exists("env.py"):
    import env as config

from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = os.getenv("SECRET", "randomstring123")

app.config["MONGO_DBNAME"] = 'picture_puzzles'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
# app.config["secret_key"] = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html",
                           puzzles=list(mongo.db.puzzles.find()))


@app.route("/browse/<search_category>")
def search(search_category):
    print("search")
    print(search_category)
    alphabet_array = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                      'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                      'W', 'X', 'Y', 'Z', 'all']

    if search_category == 'all':
        print("if")
        return render_template('browse.html',
                               puzzles=mongo.db.puzzles.find(),
                               difficulty=mongo.db.
                               difficulty_categories.find(),
                               alphabet_array=alphabet_array)

    else:
        print("else")
        my_letter = "^" + search_category
        print(my_letter)
        return render_template('browse.html',
                               puzzles=mongo.db.
                               puzzles.find
                               ({"answer": {"$regex": my_letter.lower()}}),
                               difficulty=mongo.db.
                               difficulty_categories.find(),
                               alphabet_array=alphabet_array)


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


@app.route("/register", methods=["GET", "POST"])
def register():
    try:
        form = RegistrationForm(request.form)
        print("Try")
        if request.method == "POST":
            print("POST")
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.hash((str(form.password.data)))
            users = mongo.db.users
            existing_user = users.find_one({'email': email})
            if existing_user:
                flash("This name is already taken!!", "info")
                return render_template("register.html", form=form)
            else:
                users.insert_one({'username': username,
                                  'email': email,
                                  'password': password})
                flash('Registered Success!!')
                session['logged_in'] = True
                session["user"] = username
                return redirect(url_for('user'))
        else:
            return render_template("register.html", form=form)
    except Exception as e:
        return(str(e))


@app.route('/login', methods=["GET", "POST"])
def login():
    try:
        print("TRY")
        form = RegistrationForm(request.form)
        if request.method == "POST":
            users = mongo.db.users
            user_login = users.find_one({'email': request.form.get('email')})
            if user_login:
                if sha256_crypt.verify(request.form['password'],
                                       user_login['password']):
                    username = user_login['username']
                    session['logged_in'] = True
                    session['user'] = username
                    flash("You are now logged in")
                    return redirect(url_for("user"))
                else:
                    flash("Invalid credentials, try again.")
                    return render_template("login.html", form=form)
            else:
                flash("Sorry. We have no users by that email.")
                return render_template("login.html", form=form)
        else:
            return render_template("login.html", form=form)

    except Exception as e:
        error = "Invalid credentials, try again."
        return render_template("login.html", form=form, error=error)


@app.route("/forgot_password", methods=["POST", "GET"])
def forgot_password():
    if request.method == "POST":
        print("if POST")
        return render_template("password-request-landing.html")
    else:
        print("else")
        return render_template('forgot-password.html')


@app.route("/my_account", methods=["POST", "GET"])
def my_account():
    if request.method == "POST":
        print("if POST")
        users = mongo.db.users
        user_login = users.find_one({'email': request.form.get('email')})
        print(user_login)
        new_password = {"$set": {"password": request.form.get('password')}}
        print(new_password)
        users.update_one(user_login, new_password)
        return redirect(url_for('reset_password'))
    else:
        print("else")
        return render_template("my-account.html")


@app.route("/reset_password", methods=["POST", "GET"])
def reset_password():
    if request.method == "POST":
        print("if POST")
        users = mongo.db.users
        user_login = users.find_one({'email': request.form.get('email')})
        print(user_login)
        new_password = {"$set": {"password": request.form.get('password')}}
        print(new_password)
        users.update_one(user_login, new_password)
        return redirect(url_for('reset_password'))
    else:
        print("else")
        return render_template("reset-password.html")


@app.route("/user")
def user():
    print("user function")
    if "user" in session:
        return redirect(url_for("index", user=session["user"]))
    else:
        flash("You are not logged in.")
        return redirect(url_for("login"))


@app.route("/my_puzzles")
def my_puzzles():
    user = session["user"]
    print(user)
    return render_template("my-puzzles.html",
                           user=session["user"],
                           puzzles=list(mongo.db.puzzles.find({"added_by": user})))


@app.route("/upload_puzzle", methods=["POST", "GET"])
def upload_puzzle():
    if request.method == "POST":
        puzzles = mongo.db.puzzles
        puzzles.insert_one({'added_by': request.form.get('added_by'),
                            'difficulty': request.form.get('difficulty'),
                            'image': request.form.get('image'),
                            'answer': request.form.get('answer')})
        flash('Upload Success!!')
        return redirect(url_for('my_puzzles'))
    else:
        return render_template("upload-puzzle.html",
                               difficulty=list(mongo.db.difficulty_categories.find()))


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
