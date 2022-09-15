import os
import mysql.connector
import sqlite3
import queries


class DB:
    MyQUERIES = {}

    def __init__(self, config):
        if("MySQL" in config.keys()):
            self.conn = self.connect_mysql(config["MySQL"])
        elif("SQLite3" in config.keys()):
            self.conn = self.connect_sqlite(config["SQLite3"])
        else:
            raise Exception("No database configuration found.")

    def connect_mysql(self, _config):
        self.MyQUERIES = queries.MYSQL_QUREIES
        _conn = mysql.connector.connect(
            host=_config["host"],
            user=_config["user"],
            passwd=_config["password"],
            database=_config["database"]
        )
        _cursor = _conn.cursor()
        for query in self.MyQUERIES["INIT_DB"]:
            _cursor.execute(query)
        _conn.commit()
        _cursor.close()
        return _conn

    def connect_sqlite(self, _config):
        self.MyQUERIES = queries.SQLITE3_QUREIES
        _conn = sqlite3.connect(
            _config["database"] + '.db', check_same_thread=False)
        _cursor = _conn.cursor()
        for query in self.MyQUERIES["INIT_DB"]:
            _cursor.execute(query)
        _conn.commit()
        _cursor.close()
        return _conn

class Users:
    userID = 0
    username = ''
    created = 0
    lastLogin = 0
    lastIP = ''

    def __init__(self, _userID, _username, _created, _lastLogin, _lastIP):
        self.userID = _userID
        self.username = _username
        self.created = _created
        self.lastLogin = _lastLogin
        self.lastIP = _lastIP

class Scores:
    scoreID = 0
    userID = 0
    score = 0
    score_date = 0

    def __init__(self, _scoreID, _userID, _score, _score_date):
        self.scoreID = _scoreID
        self.userID = _userID
        self.score = _score
        self.score_date = _score_date
    
class HighScores:
    username = ''
    score = 0
    score_date = 0

    def __init__(self, _username, _score, _score_date):
        self.username = _username
        self.score = _score
        self.score_date = _score_date

