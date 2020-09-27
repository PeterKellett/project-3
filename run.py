import os
from flask import Flask, render_template, \
    redirect, request, url_for, session, flash

from wtforms import Form, \
    TextField, PasswordField, validators

from passlib.hash import sha256_crypt

from flask_pymongo import PyMongo
if os.path.exists("env.py"):
    import env

from bson.objectid import ObjectId


app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'dingbat_dictionary'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/browse/")
def browse():
    alphabet_array = ['All', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                      'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                      'V', 'W', 'X', 'Y', 'Z']
    browse_letter = request.args.get('browse_letter', None)
    print("browse letter =", browse_letter)
    browse_difficulty = request.args.get('browse_difficulty', None)
    print("browse difficulty =", browse_difficulty)
    browse_contributer = request.args.get('browse_contributer', None)
    print("browse_contributer =", browse_contributer)
    if browse_letter is None and browse_difficulty is None and browse_contributer is None:
        print('All')
        return render_template('browse.html',
                               dingbats=list(mongo.db.dingbats.find().sort("answer")),
                               difficulty=mongo.db.
                               difficulty_categories.find(),
                               alphabet_array=alphabet_array,
                               letter_category="All",
                               difficulty_category="All",
                               contributer_category="All"
                               )
    elif browse_letter != 'All' and browse_difficulty == 'All' and browse_contributer == 'All':
        print('elif 1')
        return render_template('browse.html',
                               dingbats=list(mongo.db.dingbats.find({"answer": {"$regex": "^" + browse_letter.lower()}}).sort("answer")),
                               difficulty=mongo.db.
                               difficulty_categories.find(),
                               alphabet_array=alphabet_array,
                               letter_category=browse_letter,
                               difficulty_category=browse_difficulty,
                               contributer_category=browse_contributer)
    elif browse_letter != 'All' and browse_difficulty != 'All' and browse_contributer == 'All':
        print('elif 2')
        return render_template('browse.html',
                               dingbats=list(mongo.db.dingbats.find({'$and': [{"answer": {"$regex": "^" + browse_letter.lower()}}, {"difficulty": browse_difficulty}]}).sort("answer")),
                               difficulty=mongo.db.
                               difficulty_categories.find(),
                               alphabet_array=alphabet_array,
                               letter_category=browse_letter,
                               difficulty_category=browse_difficulty,
                               contributer_category=browse_contributer)
    elif browse_letter != 'All' and browse_difficulty == 'All' and browse_contributer != 'All':
        print('elif 3')
        return render_template('browse.html',
                               dingbats = list(mongo.db.dingbats.find({'$and': [{"answer": {"$regex": "^" + browse_letter.lower()}}, {"contributer_id": browse_contributer}]}).sort("answer")),
                               difficulty=mongo.db.
                               difficulty_categories.find(),
                               alphabet_array=alphabet_array,
                               letter_category=browse_letter,
                               difficulty_category=browse_difficulty,
                               contributer_category=browse_contributer)
    elif browse_letter == 'All' and browse_difficulty != 'All' and browse_contributer != 'All':
        print('elif 4')
        dingbats = list(mongo.db.dingbats.find({'$and': [{"difficulty": browse_difficulty}, {"contributer_id": browse_contributer}]}).sort("answer"))
        for dingbat in dingbats:
            print(dingbat["answer"])
            print(dingbat["difficulty"])
        return render_template('browse.html',
                               dingbats = list(mongo.db.dingbats.find({'$and': [{"difficulty": browse_difficulty}, {"contributer_id": browse_contributer}]}).sort("answer")),
                               difficulty=mongo.db.
                               difficulty_categories.find(),
                               alphabet_array=alphabet_array,
                               letter_category=browse_letter,
                               difficulty_category=browse_difficulty,
                               contributer_category=browse_contributer)
    elif browse_letter == 'All' and browse_difficulty != 'All' and browse_contributer == 'All':
        print('elif 5')
        dingbats = list(mongo.db.dingbats.find({"difficulty": browse_difficulty}).sort("answer"))
        for dingbat in dingbats:
            print(dingbat["answer"])
            print(dingbat["difficulty"])
        return render_template('browse.html',
                               dingbats = list(mongo.db.dingbats.find({"difficulty": browse_difficulty}).sort("answer")),
                               difficulty=mongo.db.
                               difficulty_categories.find(),
                               alphabet_array=alphabet_array,
                               letter_category=browse_letter,
                               difficulty_category=browse_difficulty,
                               contributer_category=browse_contributer)
    elif browse_letter == 'All' and browse_difficulty == 'All' and browse_contributer != 'All':
        print('elif 6')
        return render_template('browse.html',
                               dingbats = list(mongo.db.dingbats.find({"contributer_id": browse_contributer}).sort("answer")),
                               difficulty=mongo.db.
                               difficulty_categories.find(),
                               alphabet_array=alphabet_array,
                               letter_category=browse_letter,
                               difficulty_category=browse_difficulty,
                               contributer_category=browse_contributer)
    elif browse_letter != 'All' and browse_difficulty != 'All' and browse_contributer != 'All':
        print('elif 7')
        dingbats = list(mongo.db.dingbats.find({'$and': [{"answer": {"$regex": "^" + browse_letter.lower()}}, {"difficulty": browse_difficulty}, {"contributer_id": browse_contributer}]}).sort("answer"))
        for dingbat in dingbats:
            print(dingbat["answer"])
            print(dingbat["difficulty"])
        return render_template('browse.html',
                               dingbats = list(mongo.db.dingbats.find({'$and': [{"answer": {"$regex": "^" + browse_letter.lower()}}, {"difficulty": browse_difficulty}, {"contributer_id": browse_contributer}]}).sort("answer")),
                               difficulty=mongo.db.
                               difficulty_categories.find(),
                               alphabet_array=alphabet_array,
                               letter_category=browse_letter,
                               difficulty_category=browse_difficulty,
                               contributer_category=browse_contributer)
    else:
        print('NONE')
        return render_template('browse.html',
                               dingbats=list(mongo.db.dingbats.find().sort("answer")),
                               difficulty=mongo.db.
                               difficulty_categories.find(),
                               alphabet_array=alphabet_array,
                               letter_category="All",
                               difficulty_category="All",
                               contributer_category="All"
                               )

"""
    elif browse_category == 'All':
        return render_template('browse.html',
                               dingbats=list(mongo.db.dingbats.find().sort("answer")),
                               difficulty=mongo.db.
                               difficulty_categories.find(),
                               alphabet_array=alphabet_array,
                               browse_category='All',
                               letters=alphabet_array)
    elif browse_category == 'easy' \
        or browse_category == 'medium' \
            or browse_category == 'hard':
        return render_template('browse.html',
                               dingbats=list(mongo.db.
                               dingbats.find({"difficulty": browse_category}).sort("answer")),
                               difficulty=mongo.db.
                               difficulty_categories.find(),
                               alphabet_array=alphabet_array,
                               letters=alphabet_array
                               )
    elif len(browse_category) < 2:
        my_letter = "^" + browse_category
        return render_template('browse.html',
                               dingbats=list(mongo.db.
                               dingbats.find
                               ({"answer": {"$regex": my_letter.lower()}}).sort("answer")),
                               difficulty=mongo.db.
                               difficulty_categories.find(),
                               alphabet_array=alphabet_array,
                               browse_category=browse_category,
                               letters=browse_category)
"""

# Initiate flask registration form
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
                                         validators.Length(min=6,
                                                           message='Passwords must have \
                                                                    a minimum \
                                                                    of 6 \
                                                                    characters')
                                         ])
    confirm = PasswordField('Repeat Password',
                            validators=[validators.DataRequired(),
                                        validators.EqualTo('password',
                                                           message='Passwords must \
                                                                    match')])


# Route to registration page
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if "user" in session:
        flash('You are already registered', 'warning')
        return redirect(url_for('index'))
    else:
        if request.method == "POST" and form.validate():
            username = form.username.data.lower()
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
                session["user"] = username
                session["user_email"] = email
                return redirect(url_for('user'))
        else:
            return render_template("register.html", form=form)


# Initiate flask log in form
class LoginForm(Form):
    email = TextField('Email',
                      validators=[validators.DataRequired(),
                                  validators.Email(message='Email supplied \
                                                            is not of the \
                                                            correct format.')
                                  ])
    password = PasswordField('Password',
                             validators=[validators.DataRequired(),
                                         validators.Length(min=6,
                                                           message='Passwords must have \
                                                                    a minimum \
                                                                    of 6 \
                                                                    characters')
                                         ])


# Route to log in page
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if "user" in session:
        flash("You are already logged in", "success")
        return redirect(url_for('index'))
    else:
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
                    flash("You are now logged in", "success")
                    return redirect(url_for("user"))
                else:
                    flash("Invalid credentials, try again.", "error")
                    return render_template("login.html", form=form)
            else:
                flash("Sorry. We have no users by that email.", "warning")
                return render_template("login.html", form=form)
        else:
            return render_template("login.html", form=form)


# Route to forgot password page
@app.route("/forgot_password")
def forgot_password():
    return render_template('forgot-password.html')


@app.route("/password_link_requested")
def password_link_requested():
    return render_template('password-request-landing.html')


# Route to My Account page
@app.route("/my_account")
def my_account():
    if "user" in session:
        return render_template("my-account.html")
    else:
        flash("You are not logged in", "warning")
        return redirect(url_for('index'))


# Initiate the reset password form
class ResetPasswordForm(Form):
    password = PasswordField('Password',
                             validators=[validators.DataRequired(),
                                         validators.Length(min=6,
                                                           message='Passwords must have \
                                                                    a minimum \
                                                                    of 6 \
                                                                    characters')
                                         ])
    confirm = PasswordField('Repeat Password',
                            validators=[validators.DataRequired(),
                                        validators.EqualTo('password',
                                                           message='Passwords must \
                                                                    match')])


# Route to reset password page
@app.route("/reset_password", methods=["POST", "GET"])
def reset_password():
    if "user" in session:
        form = ResetPasswordForm(request.form)
        email = session['user_email']
        if request.method == "POST" and form.validate():
            email = session['user_email']
            users = mongo.db.users
            user_login = users.find_one({'email': email})
            password = sha256_crypt.hash((str(form.password.data)))
            new_password = {"$set": {"password": password}}
            users.update_one(user_login, new_password)
            flash("Changed password success!", "success")
            return redirect(url_for('my_account'))
        else:
            return render_template("reset-password.html", form=form)
    else:
        flash("You are not logged in", "warning")
        return redirect(url_for('index'))


# Process for adding dingbat likes
@app.route("/like/<dingbat_id>")
def like(dingbat_id):
    if "user" in session:
        dingbats = mongo.db.dingbats
        dingbat = mongo.db.dingbats.find_one({
            '_id': ObjectId(dingbat_id)
        })
        dingbats.update_one(dingbat, {"$push": {"likes": session['id']}})
        dingbat = mongo.db.dingbats.find_one({
            '_id': ObjectId(dingbat_id)
        })
        dingbats.update_one(dingbat, {"$pull": {"dislikes": session['id']}})
    else:
        flash("You must be logged in to add likes/dislikes", "warning")
    return redirect(url_for('browse', browse_category='All'))


# Process for removing dingbat likes
@app.route("/unlike/<dingbat_id>")
def unlike(dingbat_id):
    if "user" in session:
        dingbats = mongo.db.dingbats
        dingbat = mongo.db.dingbats.find_one({
            '_id': ObjectId(dingbat_id)
        })
        dingbats.update_one(dingbat, {"$pull": {"likes": session['id']}})
    else:
        flash("You must be logged in to add likes/dislikes", "warning")
    return redirect(url_for('browse', browse_category='All'))


# Process for adding dingbat dislikes
@app.route("/dislike/<dingbat_id>")
def dislike(dingbat_id):
    if "user" in session:
        dingbats = mongo.db.dingbats
        dingbat = mongo.db.dingbats.find_one({
            '_id': ObjectId(dingbat_id)
        })
        dingbats.update_one(dingbat, {"$push": {"dislikes": session['id']}})
        dingbat = mongo.db.dingbats.find_one({
            '_id': ObjectId(dingbat_id)
        })
        dingbats.update_one(dingbat, {"$pull": {"likes": session['id']}})
    else:
        flash("You must be logged in to add likes/dislikes", "warning")
    return redirect(url_for('browse', browse_category='All'))


# Process for removing dingbat dislikes
@app.route("/undislike/<dingbat_id>")
def undislike(dingbat_id):
    if "user" in session:
        dingbats = mongo.db.dingbats
        dingbat = mongo.db.dingbats.find_one({
            '_id': ObjectId(dingbat_id)
        })
        dingbats.update_one(dingbat, {"$pull": {"dislikes": session['id']}})
    else:
        flash("You must be logged in to add likes/dislikes", "warning")
    return redirect(url_for('browse', browse_category='All'))


# A Route redirect if user attempts to enter the url manually
@app.route("/user")
def user():
    if "user" in session:
        return redirect(url_for('index'))
    else:
        flash("You are not logged in.", "warning")
        return redirect(url_for('login'))


# Route to My Dingbats page
@app.route("/my_dingbats/<contributer_id>")
def my_dingbats(contributer_id):
    if contributer_id == session["id"]:
        contributer = mongo.db.users.find_one({"_id": ObjectId(contributer_id)})
        contributer["_id"] = str(contributer["_id"])
        return render_template("my-dingbats.html",
                               contributer=contributer,
                               dingbats=list(mongo.db.dingbats
                                            .find({"contributer_id": contributer_id}).sort("answer")))
    else:
        flash("You do not authorised to access that section", "error")
        return redirect(url_for('browse', browse_category='All'))


# Route to upload dingbat page
@app.route("/upload_dingbat", methods=["POST", "GET"])
def upload_dingbat():
    if "user" in session:
        if request.method == "POST":
            image = request.form.get('image')
            if image is None:
                flash('Please choose an image to upload', 'error')
                return render_template("upload-dingbat.html",
                                       difficulty=list(mongo.db
                                                       .difficulty_categories
                                                       .find()))
            else:
                dingbats = mongo.db.dingbats
                dingbats.insert_one({'contributer_id': session["id"],
                                     'contributer_name': session["user"],
                                     'difficulty': request.form.get('difficulty'),
                                     'image': 'https://res.cloudinary.com/dfboxofas/' + request.form.get('image'),
                                     'answer': request.form.get('answer').lower(),
                                     'likes': [],
                                     'dislikes': []})
                flash('Upload Success!!', 'success')
                return redirect(url_for('my_dingbats',  contributer_id=session['id']))
        else:
            return render_template("upload-dingbat.html",
                                   difficulty=list(mongo.db
                                                   .difficulty_categories
                                                   .find()))
    else:
        flash("You are not logged in", "warning")
        return redirect(url_for('index'))


# Route to Edit Dingbat page
@app.route("/edit_dingbat/<dingbat_id>")
def edit_dingbat(dingbat_id):
    the_dingbat = mongo.db.dingbats.find_one({"_id": ObjectId(dingbat_id)})
    difficulty_categories = mongo.db.difficulty_categories.find()
    return render_template('edit-dingbat.html',
                           dingbat=the_dingbat, difficulty=difficulty_categories)


# Function to Edit Dingbat
@app.route("/update_dingbat/<dingbat_id>", methods=["POST"])
def update_dingbat(dingbat_id):
    dingbats = mongo.db.dingbats
    the_dingbat = mongo.db.dingbats.find_one({"_id": ObjectId(dingbat_id)})
    image = request.form.get('image')
    if image is None:
        image = the_dingbat['image']
        dingbats.update({'_id': ObjectId(dingbat_id)},
                        {
                        'contributer_id': session["id"],
                        'contributer_name': session["user"],
                        'difficulty': request.form.get('difficulty'),
                        'image': image,
                        'answer': request.form.get('answer'),
                        'likes': the_dingbat['likes'],
                        'dislikes': the_dingbat["dislikes"]
                        })
    else:
        dingbats.update({'_id': ObjectId(dingbat_id)},
                        {
                        'contributer_id': session["id"],
                        'contributer_name': session["user"],
                        'difficulty': request.form.get('difficulty'),
                        'image': 'https://res.cloudinary.com/dfboxofas/' + request.form.get('image'),
                        'answer': request.form.get('answer'),
                        'likes': the_dingbat['likes'],
                        'dislikes': the_dingbat["dislikes"]
                        })
    return redirect(url_for('my_dingbats',  contributer_id=session['id']))


# Function to delete Dingbat
@app.route("/delete_dingbat/<dingbat_id>")
def delete_dingbat(dingbat_id):
    mongo.db.dingbats.remove({'_id': ObjectId(dingbat_id)})
    return redirect(url_for('my_dingbats',  contributer_id=session['id']))


# Route to Logout function - Clear session variables
@app.route("/logout")
def logout():
    session.pop("id", None)
    session.pop("user", None)
    session.pop("user_email", None)
    flash("You have been logged out", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
