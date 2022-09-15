SQLITE3_QUREIES = {
    'INIT_DB': [
        "CREATE TABLE IF NOT EXISTS 'users' ('userID'	INTEGER NOT NULL,'username'	TEXT NOT NULL UNIQUE,'created'	INTEGER NOT NULL,'last_login' INTEGER,'last_ip' TEXT, PRIMARY KEY(`userID` AUTOINCREMENT));",
        "CREATE TABLE IF NOT EXISTS 'scores' ('scoreID' INTEGER NOT NULL,'userID' INTEGER NOT NULL, 'score' REAL NOT NULL,'score_date'	INTEGER NOT NULL, PRIMARY KEY(`scoreID` AUTOINCREMENT));",
        "CREATE VIEW IF NOT EXISTS high_scores AS SELECT t.username, MAX(p.score) AS score, p.score_date FROM users AS t, scores AS p WHERE t.userID = p.userID GROUP BY t.username ORDER BY score DESC;"
    ],
    #USER QUERIES
    'GET_USER': "SELECT * FROM users WHERE username = '%s'",
    'GET_USERS': "SELECT * FROM users",
    'UPDATE_USER': "UPDATE users SET last_login = %s, last_ip = '%s' WHERE userID = %s",
    'INSERT_USER': "INSERT INTO users (username, created, last_login, last_ip) VALUES ('%s', %s, %s, '%s')",
    
    #SCORE QUERIES
    'GET_HIGHSCORES': "SELECT * FROM high_scores",
    'GET_USER_SCORES': "SELECT * FROM scores WHERE userID = %s",
    'INSERT_SCORE': "INSERT INTO scores (userID, score, score_date) VALUES (%s, %s, %s)",

    #WIPE DATABASE
    'WIPE_DATABASE': [
        "DELETE FROM scores",
        "DELETE FROM users"
    ]
}
MYSQL_QUREIES = {
    'INIT_DB': [
        "CREATE TABLE IF NOT EXISTS users (userID INT NOT NULL AUTO_INCREMENT, username VARCHAR(255) NOT NULL UNIQUE, created INT NOT NULL, last_login INT, last_ip VARCHAR(255), PRIMARY KEY (userID));",
        "CREATE TABLE IF NOT EXISTS scores (scoreID INT NOT NULL AUTO_INCREMENT, userID INT NOT NULL, score FLOAT NOT NULL, score_date INT NOT NULL, PRIMARY KEY (scoreID), FOREIGN KEY (userID) REFERENCES users(userID));",
        "CREATE VIEW IF NOT EXISTS high_scores AS SELECT t.username, MAX(p.score) AS score, p.score_date FROM users AS t, scores AS p WHERE t.userID = p.userID GROUP BY t.username ORDER BY score DESC;"
    ],
    #USER QUERIES
    'GET_USER': "SELECT * FROM users WHERE username = '%s'",
    'GET_USERS': "SELECT * FROM users",
    'UPDATE_USER': "UPDATE users SET last_login = %s, last_ip = '%s' WHERE userID = %s",
    'INSERT_USER': "INSERT IGNORE INTO users (username, created, last_login, last_ip) VALUES ('%s', %s, %s, '%s')",

    #SCORE QUERIES
    'GET_HIGHSCORES': "SELECT * FROM high_scores",
    'GET_USER_SCORES': "SELECT * FROM scores WHERE userID = %s",
    'INSERT_SCORE': "INSERT INTO scores (userID, score, score_date) VALUES ((SELECT userID FROM users WHERE userID = %s), %s, %s)",

    #WIPE DATABASE
    'WIPE_DATABASE': [
        "DELETE FROM scores",
        "DELETE FROM users"
    ]
}