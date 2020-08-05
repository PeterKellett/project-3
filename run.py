import os
from flask import Flask, render_template, redirect, request, url_for, session, flash

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
    alphabet_array = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                      'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                      'W', 'X', 'Y', 'Z', 'all']
    print(search_category)
    if search_category == 'all':
        print("if")
        return render_template('browse.html',
                               puzzles=mongo.db.puzzles.find(),
                               difficulty=mongo.db.
                               difficulty_categories.find(),
                               alphabet_array=alphabet_array)

    if search_category == 'easy' or 'medium' or 'hard':
        print("elif")
        return render_template('browse.html',
                               puzzles=mongo.db.
                               puzzles.find
                               ({"difficulty": search_category.lower()}),
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


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form.get('username')})
        if existing_user:
            flash("This name is already taken!!", "info")
            return redirect(url_for('register'))
        else:
            users.insert_one(request.form.to_dict())
            flash('Registered Success!!')
            session["user"] = user
            return redirect(url_for('user'))
    else:
        return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        users = mongo.db.users
        user_login = users.find_one({'username': request.form.get('username')})
        print(user_login)
        if user_login:
            password = request.form["password"]
            if user_login['password'] == password:
                session["user"] = user_login['username']
                flash("Login successful!")
                return redirect(url_for("user"))
            else:
                flash("Login unsuccessful!")
                return redirect(url_for('login'))
        else:
            flash("Sorry, we have no users by that name")
            return redirect(url_for('login'))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user")
def user():
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
        puzzles.insert_one(request.form.to_dict())
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
