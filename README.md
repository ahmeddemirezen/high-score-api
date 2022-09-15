full structure of conf.json

***

```json
{
"server": {
    "host": "localhost",
    "port": 8080,
    "route": "/api/v1",
    "auth": {
        "username": "admin",
        "password": "admin"
    }
},
"app": {
    "name": "High Score API",
    "version": "1.0.0",
    "description": "This is high score api",
    "author": "ahmmeddemirezen",
    "license": "MIT",
    "website": "https://ahmeddemirezen.github.io"
},
"MySQL": {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "my_db"
},
"SQLite3": {
    "database": "my_db"
},
"debug": true
}

```
