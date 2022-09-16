import datetime
from db import DB, Users, Scores, HighScores
import json
import flask
from flask_httpauth import HTTPBasicAuth
from flask import send_from_directory
import random
import utilities as util

config = {}
with open("conf.json", "r") as f:
    config = json.load(f)

db = DB(config)

app = flask.Flask(__name__,
                  static_url_path='',
                  static_folder='web/static',
                  template_folder='web/templates')
auth = HTTPBasicAuth()

index = open("web/static/index.html", "r").read()


@app.route('/', methods=['GET'])
def home():
    return util.params_to_html(index, config['app'])
    # return send_from_directory(app.static_folder, 'index.html')


@app.route('/docs', methods=['GET'])
def docs():
    return send_from_directory(app.static_folder, 'docs.html')


@auth.verify_password
def authenticate(username, password):
    authInfo = config["server"]["auth"]
    if username and password:
        if username == authInfo["username"] and password == authInfo["password"]:
            return True
        else:
            return False
    return False


@app.route(config["server"]["route"]+'/configs', methods=['GET'])
@auth.login_required
def get_conf():
    return flask.jsonify(config)


@app.route(config["server"]["route"]+'/highscores', methods=['GET'])
@auth.login_required
def get_highscores():
    cursor = db.conn.cursor()
    cursor.execute(db.MyQUERIES["GET_HIGHSCORES"])
    scores = cursor.fetchall()
    payload = []
    for score in scores:
        payload.append(
            HighScores(score[0], score[1], score[2]).__dict__)
    cursor.close()
    return flask.jsonify(payload)


@app.route(config["server"]["route"]+'/wipe', methods=['DELETE'])
@auth.login_required
def wipe_database():
    cursor = db.conn.cursor()
    for query in db.MyQUERIES["WIPE_DATABASE"]:
        cursor.execute(query)
    db.conn.commit()
    cursor.close()
    return flask.jsonify({"success": "Database wiped!"})


if(config["debug"]):
    @app.route(config["server"]["route"]+'/debug', methods=['GET'])
    def debug():
        return flask.jsonify({"debug": "true"})

    @app.route(config["server"]["route"]+'/feed', methods=['POST'])
    def feed():
        cursor = db.conn.cursor()
        count = flask.request.json["count"]
        for i in range(count):
            username = "user" + str(random.randint(0, 1000000))
            created = int(datetime.datetime.now().timestamp())
            lastLogin = created
            ip = flask.request.remote_addr
            cursor.execute(db.MyQUERIES["INSERT_USER"] %
                           (username, created, lastLogin, ip))
        db.conn.commit()
        cursor.close()

        cursor = db.conn.cursor()

        cursor.execute(db.MyQUERIES["GET_USERS"])
        users = cursor.fetchall()
        for user in users:
            for i in range(count):
                score = random.randint(0, 100)
                date = int(datetime.datetime.now().timestamp())
                cursor.execute(db.MyQUERIES["INSERT_SCORE"] %
                               (user[0], score, date))
        db.conn.commit()
        cursor.close()
        return flask.jsonify({"success": "Database fed!"})

else:
    @app.route(config["server"]["route"]+'/debug', methods=['GET'])
    def debug():
        return flask.jsonify({"debug": "false"})


@app.route(config["server"]["route"]+'/users', methods=['GET'])
@auth.login_required
def get_users():
    cursor = db.conn.cursor()
    cursor.execute(db.MyQUERIES["GET_USERS"])
    users = cursor.fetchall()
    payload = []
    for user in users:
        payload.append(
            Users(user[0], user[1], user[2], user[3], user[4]).__dict__)
    cursor.close()
    return flask.jsonify(payload)


@app.route(config["server"]["route"]+'/users', methods=['POST'])
@auth.login_required
def post_user():
    cursor = db.conn.cursor()
    username = flask.request.json["username"]
    created = int(datetime.datetime.now().timestamp())
    lastLogin = created
    ip = flask.request.remote_addr

    cursor.execute(db.MyQUERIES["GET_USER"] % (username))
    user = cursor.fetchone()
    if(user is None):
        cursor.execute(db.MyQUERIES["INSERT_USER"] %
                       (username, created, lastLogin, ip))
        db.conn.commit()
        cursor.close()
        return flask.jsonify({"success": "User added!"})
    else:
        cursor.close()
        return flask.jsonify({"error": "User already exists!"})


@app.route(config["server"]["route"]+'/users/<string:username>', methods=['GET'])
@auth.login_required
def get_user(username):
    cursor = db.conn.cursor()
    cursor.execute(db.MyQUERIES["GET_USER"] % (username))
    user = cursor.fetchone()
    if(user is not None):
        payload = Users(user[0], user[1], user[2], user[3], user[4]).__dict__
        cursor.close()
        return flask.jsonify(payload)
    else:
        cursor.close()
        return flask.jsonify({"error": "User not found!"})


@app.route(config["server"]["route"]+'/users/<string:username>', methods=['PUT'])
@auth.login_required
def put_user(username):
    cursor = db.conn.cursor()
    cursor.execute(db.MyQUERIES["GET_USER"] % (username))
    user = cursor.fetchone()
    if(user is None):
        cursor.close()
        return flask.jsonify({"error": "User not found!"})
    user = Users(user[0], user[1], user[2], user[3], user[4])
    if(user is not None):
        lastLogin = int(datetime.datetime.now().timestamp())
        ip = flask.request.remote_addr
        cursor.execute(db.MyQUERIES["UPDATE_USER"] %
                       (lastLogin, ip, user.userID))
        db.conn.commit()
        cursor.close()
        return flask.jsonify({"success": "User updated!"})
    else:
        cursor.close()
        return flask.jsonify({"error": "User not found!"})


@app.route(config["server"]["route"]+'/users/<string:username>/scores', methods=['GET'])
@auth.login_required
def get_user_scores(username):
    cursor = db.conn.cursor()
    cursor.execute(db.MyQUERIES["GET_USER"] % (username))
    user = cursor.fetchone()
    if(user is None):
        cursor.close()
        return flask.jsonify({"error": "User not found!"})
    user = Users(user[0], user[1], user[2], user[3], user[4])
    if(user is not None):
        cursor.execute(db.MyQUERIES["GET_USER_SCORES"] % (user.userID))
        scores = cursor.fetchall()
        payload = []
        for score in scores:
            payload.append(
                Scores(score[0], score[1], score[2], score[3]).__dict__)
        cursor.close()
        return flask.jsonify(payload)
    else:
        cursor.close()
        return flask.jsonify({"error": "User not found!"})


@app.route(config["server"]["route"]+'/users/<string:username>/scores', methods=['POST'])
@auth.login_required
def post_user_score(username):
    cursor = db.conn.cursor()
    cursor.execute(db.MyQUERIES["GET_USER"] % (username))
    user = cursor.fetchone()
    if(user is None):
        cursor.close()
        return flask.jsonify({"error": "User not found!"})
    user = Users(user[0], user[1], user[2], user[3], user[4])
    if(user is not None):
        score = flask.request.json["score"]
        date = int(datetime.datetime.now().timestamp())
        cursor.execute(db.MyQUERIES["INSERT_SCORE"] %
                       (user.userID, score, date))
        db.conn.commit()
        cursor.close()
        return flask.jsonify({"success": "Score added!"})
    else:
        cursor.close()
        return flask.jsonify({"error": "User not found!"})


app.run(host=config["server"]["host"],
        port=config["server"]["port"], debug=config["debug"])

db.conn.close()
