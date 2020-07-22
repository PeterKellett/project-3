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
    return render_template("index.html",
                           stats=mongo.db.match_stats.find())


@app.route("/get_data")
def get_data():
    stats = mongo.db.players.find()
    json_data = []
    for stat in stats:
        json_data.append(stat)
    return json_data


@app.route("/update_data")
def update_data():
    return render_template("update-data.html",
                           players=mongo.db.players.find())


@app.route('/manage_players')
def manage_players():
    return render_template('players.html',
                           players=list(mongo.db.players.find()))


@app.route("/add_player")
def add_player():
    return render_template('add-player.html')


@app.route("/insert_player", methods=['POST'])
def insert_player():
    players = mongo.db.players
    player_doc = {'player_name': request.form.get('player_name')}
    players.insert_one(player_doc)
    return redirect(url_for('update_data'))


@app.route("/edit_player/<player_id>")
def edit_player(player_id):
    return render_template('edit-player.html', player=mongo.db.players.find_one({'_id': ObjectId(player_id)}))


@app.route("/update_player/<player_id>", methods=["POST"])
def update_player(player_id):
    mongo.db.players.update(
        {'_id': ObjectId(player_id)},
        {'player_name': request.form.get('player_name')})
    return redirect(url_for('manage_players'))


@app.route("/delete_player/<player_id>")
def delete_player(player_id):
    mongo.db.players.delete_one({'_id': ObjectId(player_id)})
    return redirect(url_for('manage_players'))


@app.route("/insert_data", methods=['POST'])
def insert_data():
    mongo_doc = []
    print('mongo_doc')
    print(mongo_doc)   
    mongo_doc.append(request.form.to_dict())
    print(mongo_doc)
    stats = mongo.db.match_stats
    stats.insert_many(mongo_doc)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
