import os
from flask import Flask, render_template, \
    redirect, request, url_for, session, flash, jsonify

from wtforms import Form, BooleanField, \
    TextField, PasswordField, validators

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


@app.route("/interactive/")
def interactive():
    return render_template('interactive.html')


@app.route("/background_process2")
def background_process2():
    print("background_process2")
    return redirect(url_for('index'))


@app.route("/background_process")
def background_process():
    lang = request.args.get('proglang')
    if str(lang).lower() == 'python':
        return jsonify(result='Correct')
    else:
        return jsonify(result='Wrong!!')


@app.route("/browse/<search_category>")
def search(search_category):
    print("search")
    print(search_category)
    # print(likes)
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
    username = TextField('Username',
                         validators=[validators.DataRequired(),
                                     validators.Length(min=4,
                                                       max=20,
                                                       message='Username must be at \
                                                                least 4 \
                                                                characters \
                                                                long.'
                                                       )
                                     ]
                         )
    email = TextField('Email Address',
                      validators=[validators.DataRequired(),
                                  validators.Email(message='Email supplied \
                                                            is not of the \
                                                            correct format.')
                                  ])
    password = PasswordField('Password',
                             validators=[validators.DataRequired(),
                                         validators.EqualTo('confirm',
                                                            message='Passwords \
                                                                     must \
                                                                     match'
                                                            )
                                         ])
    confirm = PasswordField('Repeat Password',
                            validators=[validators.DataRequired(),
                                        validators.EqualTo('password',
                                        message='Passwords must match')])


@app.route("/register", methods=["GET", "POST"])
def register():
    try:
        form = RegistrationForm(request.form)
        print("Try")
        if "user" in session:
            flash("You are already registered")
            return redirect(url_for('index'))
        else:
            if request.method == "POST" and form.validate():
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
                    session["user_email"] = email
                    session['logged_in'] = True
                    session["user"] = username
                    return redirect(url_for('user'))
            else:
                # flash("Validation fail")
                return render_template("register.html", form=form)
    except Exception as e:
        return(str(e))


class LoginForm(Form):
    email = TextField('Email',
                      validators=[validators.DataRequired()
                                  ])
    password = PasswordField('Password',
                             validators=[validators
                                         .DataRequired()])


@app.route('/login', methods=["GET", "POST"])
def login():
    try:
        print(session)
        form = LoginForm(request.form)
        if "user" in session:
            flash("You are already registered")
            return redirect(url_for('index'))
        else:
            if request.method == "POST":
                users = mongo.db.users
                user_login = users.find_one({'email': request.form.
                                             get('email')})
                if user_login:
                    if sha256_crypt.verify(request.form['password'],
                                           user_login['password']):
                        username = user_login['username']
                        user_id = user_login['_id']
                        print(user_id)
                        session['user_email'] = user_login['email']
                        session['logged_in'] = True
                        session['user'] = username
                        print(session)
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


@app.route("/forgot_password")
def forgot_password():
    return render_template('forgot-password.html')


@app.route("/email_sent")
def email_sent():
    return render_template('password-request-landing.html')


@app.route("/my_account")
def my_account():
    if "user" in session:
        return render_template("my-account.html")
    else:
        flash("You are not logged in")
        return redirect(url_for('index'))


class ResetPasswordForm(Form):
    password = PasswordField('Password',
                             validators=[validators.DataRequired(),
                                         validators.EqualTo('confirm',
                                                            message='Passwords \
                                                                     must \
                                                                     match'
                                                            )
                                         ]
                             )
    confirm = PasswordField('Repeat Password')


@app.route("/reset_password", methods=["POST", "GET"])
def reset_password():
    if "user" in session:
        form = ResetPasswordForm(request.form)
        email = session['user_email']
        print(email)
        if request.method == "POST" and form.validate():
            print("if POST")
            email = session['user_email']
            print(email)
            users = mongo.db.users
            user_login = users.find_one({'email': email})
            print(user_login)
            password = sha256_crypt.hash((str(form.password.data)))
            new_password = {"$set": {"password": password}}
            print(new_password)
            users.update_one(user_login, new_password)
            flash("Changed password success!")
            return redirect(url_for('my_account'))
        else:
            print("else")
            return render_template("reset-password.html", form=form)
    else:
        flash("You are not logged in")
        return redirect(url_for('index'))


@app.route("/user")
def user():
    print("user function")
    if "user" in session:
        return redirect(url_for("index"))
    else:
        flash("You are not logged in.")
        return redirect(url_for("login"))


@app.route("/my_puzzles")
def my_puzzles():
    if "user" in session:
        user = session["user"]
        print(user)
        return render_template("my-puzzles.html",
                               user=session["user"],
                               puzzles=list(mongo.db.puzzles
                                            .find({"added_by": user})))
    else:
        flash("You are not logged in")
        return redirect(url_for('index'))


@app.route("/upload_puzzle", methods=["POST", "GET"])
def upload_puzzle():
    if "user" in session:
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
                                   difficulty=list(mongo.db
                                                   .difficulty_categories
                                                   .find()))
    else:
        flash("You are not logged in")
        return redirect(url_for('index'))


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("logged_in", None)
    session.pop("user_email", None)
    print(session)
    flash("You have been logged out", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
