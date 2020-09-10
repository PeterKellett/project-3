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

from flask_mail import Mail, Message

app = Flask(__name__)
app.config.update(
    MAIL_USERNAME='peterprivate7@gmail.com',
    MAIL_PASSWORD='Blackhills1'
)
mail = Mail(app)

app.secret_key = os.getenv("SECRET", "randomstring123")

app.config["MONGO_DBNAME"] = 'picture_puzzles'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
# app.config["secret_key"] = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html",
                           puzzles=list(mongo.db.puzzles.find()))


@app.route("/flask_email")
def flask_email():
    msg = Message("Hello",
                  sender="peterprivate7@gmail.com",
                  recipients=["peterwkellett@gmail.com"])
    mail.send(msg)
    return render_template('interactive.html')


"""
@app.route("/background_process")
def background_process():
    lang = request.args.get('proglang')
    if str(lang).lower() == 'python':
        return jsonify(result='Correct')
    else:
        return jsonify(result='Wrong!!')
"""


@app.route("/browse/<search_category>")
def search(search_category):
    print("search")
    print(search_category)
    print(session)
    # print(likes)
    alphabet_array = ['All', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                      'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                      'V', 'W', 'X', 'Y', 'Z']

    if search_category == 'All':
        print("if")
        return render_template('browse.html',
                               puzzles=mongo.db.puzzles.find(),
                               difficulty=mongo.db.
                               difficulty_categories.find(),
                               alphabet_array=alphabet_array,
                               contributers=mongo.db.users.find(),
                               search_category='All')
    elif search_category == 'easy' \
        or search_category == 'medium' \
            or search_category == 'hard':
        print("elif")
        return render_template('browse.html',
                               puzzles=mongo.db.
                               puzzles.find({"difficulty": search_category}),
                               difficulty=mongo.db.
                               difficulty_categories.find(),
                               alphabet_array=alphabet_array,
                               contributers=mongo.db.users.find())
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
                               alphabet_array=alphabet_array,
                               contributers=mongo.db.users.find(),
                               search_category=search_category)


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
            flash('You are already registered', 'warning')
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
                    flash("This email is already taken!!", "warning")
                    return render_template("register.html", form=form)
                else:
                    id = users.insert_one({'username': username,
                                      'email': email,
                                      'password': password})
                    flash('Registered Success!!', 'success')
                    session["id"] = str(id.inserted_id)
                    session["user_email"] = email
                    session['logged_in'] = True
                    session["user"] = username
                    return redirect(url_for('user'))
            else:
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
        print("login function")
        form = LoginForm(request.form)
        if "user" in session:
            flash("You are already registered", "warning")
            return redirect(url_for('index'))
        else:
            print("login else")
            if request.method == "POST":
                users = mongo.db.users
                user_login = users.find_one({'email': request.form.
                                             get('email')})
                if user_login:
                    if sha256_crypt.verify(request.form['password'],
                                           user_login['password']):
                        session['id'] = str(user_login['_id'])
                        session['user'] = user_login['username']
                        session['user_email'] = user_login['email']
                        session['logged_in'] = True
                        print(session)
                        flash("You are now logged in", "success")
                        return redirect(url_for("user"))
                    else:
                        flash("Invalid credentials, try again.", "error")
                        return render_template("login.html", form=form)
                else:
                    flash("Sorry. We have no users by that email.", "warning")
                    return render_template("login.html", form=form)
            else:
                print("login else else")
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
        flash("You are not logged in", "warning")
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
        if request.method == "POST" and form.validate():
            email = session['user_email']
            print(email)
            users = mongo.db.users
            user_login = users.find_one({'email': email})
            password = sha256_crypt.hash((str(form.password.data)))
            new_password = {"$set": {"password": password}}
            users.update_one(user_login, new_password)
            flash("Changed password success!", "success")
            return redirect(url_for('my_account'))
        else:
            print("else")
            return render_template("reset-password.html", form=form)
    else:
        flash("You are not logged in", "warning")
        return redirect(url_for('index'))


@app.route("/like/<puzzle_id>")
def like(puzzle_id):
    if "user" in session:
        puzzles = mongo.db.puzzles
        puzzle = mongo.db.puzzles.find_one({
            '_id': ObjectId(puzzle_id)
        })
        puzzles.update_one(puzzle, {"$push": {"likes": session['id']}})
        puzzles.update_one(puzzle, {"$pull": {"dislikes": session['id']}})
    else:
        flash("Please register/login first", "warning")
        print("like else")
    return redirect(url_for('search', search_category='All'))


@app.route("/unlike/<puzzle_id>")
def unlike(puzzle_id):
    if "user" in session:
        puzzles = mongo.db.puzzles
        puzzle = mongo.db.puzzles.find_one({
            '_id': ObjectId(puzzle_id)
        })
        puzzles.update_one(puzzle, {"$pull": {"likes": session['id']}})
    return redirect(url_for('search', search_category='All'))


@app.route("/dislike/<puzzle_id>")
def dislike(puzzle_id):
    if "user" in session:
        puzzles = mongo.db.puzzles
        puzzle = mongo.db.puzzles.find_one({
            '_id': ObjectId(puzzle_id)
        })
        puzzles.update_one(puzzle, {"$push": {"dislikes": session['id']}})
        # puzzles.update_one(puzzle, {"$push": {"dislikes": session['id']}})
    return redirect(url_for('search', search_category='All'))


@app.route("/undislike/<puzzle_id>")
def undislike(puzzle_id):
    if "user" in session:
        puzzles = mongo.db.puzzles
        puzzle = mongo.db.puzzles.find_one({
            '_id': ObjectId(puzzle_id)
        })
        puzzles.update_one(puzzle, {"$pull": {"dislikes": session['id']}})
    return redirect(url_for('search', search_category='All'))


@app.route("/user")
def user():
    print("user function")
    if "user" in session:
        print("user if")
        return redirect(url_for('index'))
    else:
        print("user else")
        flash("You are not logged in.", "warning")
        return redirect(url_for('login'))


@app.route("/my_puzzles/<id>")
def my_puzzles(id):
    user = mongo.db.users.find_one({"_id": ObjectId(id)})
    print(user)
    print(type(user))
    print(type(user["_id"]))
    user["_id"] = str(user["_id"])
    print(user)
    print(type(user["_id"]))
    if "id" in session:
        if id == session["id"]:
            return render_template("my-puzzles.html",
                                   user=user,
                                   puzzles=list(mongo.db.puzzles
                                                .find({"contributer_id": id})))
        else:
            return render_template("my-puzzles.html",
                                   user=user,
                                   puzzles=list(mongo.db.puzzles
                                                .find({"contributer_id": id})))
    else:
        return render_template("my-puzzles.html",
                               user=user,
                               puzzles=list(mongo.db.puzzles
                                            .find({"contributer_id": id})))


@app.route("/upload_puzzle", methods=["POST", "GET"])
def upload_puzzle():
    if "user" in session:
        if request.method == "POST":
            puzzles = mongo.db.puzzles
            print(request.form.get('image'))
            puzzles.insert_one({'contributer_id': session["id"],
                                'contributer_name': session["user"],
                                'difficulty': request.form.get('difficulty'),
                                'image': 'https://res.cloudinary.com/dfboxofas/' + request.form.get('image'),
                                'answer': request.form.get('answer')})
            flash('Upload Success!!', 'success')
            return redirect(url_for('my_puzzles'))
        else:
            return render_template("upload-puzzle.html",
                                   difficulty=list(mongo.db
                                                   .difficulty_categories
                                                   .find()))
    else:
        flash("You are not logged in", "warning")
        return redirect(url_for('index'))


@app.route("/edit_puzzle/<puzzle_id>")
def edit_puzzle(puzzle_id):
    the_puzzle = mongo.db.puzzles.find_one({"_id": ObjectId(puzzle_id)})
    difficulty_categories = mongo.db.difficulty_categories.find()
    return render_template('edit-puzzle.html',
                           puzzle=the_puzzle, difficulty=difficulty_categories)


@app.route("/update_puzzle/<puzzle_id>", methods=["POST"])
def update_puzzle(puzzle_id):
    puzzles = mongo.db.puzzles
    puzzles.update({'_id': ObjectId(puzzle_id)},
                   {
                    'added_by': session["user"],
                    'difficulty': request.form.get('difficulty'),
                    'image': 'https://res.cloudinary.com/dfboxofas/' + request.form.get('image'),
                    'answer': request.form.get('answer')
    })
    return redirect(url_for('my_puzzles'))


@app.route("/delete_puzzle/<puzzle_id>")
def delete_puzzle(puzzle_id):
    mongo.db.puzzles.remove({'_id': ObjectId(puzzle_id)})
    return redirect(url_for('my_puzzles'))


@app.route("/logout")
def logout():
    session.pop("id", None)
    session.pop("user", None)
    session.pop("logged_in", None)
    session.pop("user_email", None)
    print(session)
    flash("You have been logged out", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
