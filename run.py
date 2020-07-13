import os
from flask import Flask, render_template, redirect, request, url_for

from flask_pymongo import PyMongo
if os.path.exists("env.py"):
    import env as config

from bson.objectid import ObjectId

app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'esker-cel-u13'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html", stats=mongo.db.match_stats.find())


@app.route("/update_data")
def update_data():
    return render_template("update-data.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
