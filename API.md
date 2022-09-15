# High Score API

## Home

#### Request
`GET` -> `/`

### Responses

#### 200
`<h1>Welcome to the {app-name}!</h1><p>{description}</p><div><span>Version: {version}</span></br><span>Author: {author}</span></br><span>License: {license}</span></br><a href='{website}'>For more detail...</a></div>`

## Get Configuration
:tw-1f512:`Auth Required`

#### Request
`GET` -> `{route}/configs`

**Route** string
Url root of the api. It can be change from the conf.json file.

### Responses

#### 200
**BODY** `json`

	dictionary:"server"
		string:"host"
		int:"port"
		string:"route"
		dictionary:"auth"
			string:"username"
			string:"password"
	dictionary:"app"
		string"name"
		string:"version"
		string:"description"
		string:"author"
		string:"license"
		string:"website"

	dictionary:"SQLite3"
		string:"database"

	dictionary:"MySQL"
		string:"host"
		int:"port"
		string:"username"
		string:"password"
		string:"database"

	bool:"debug"

## Get High Scores
:tw-1f512:`Auth Required`

#### Request
`GET` -> `{route}/highscores`

**Route** string
Url root of the api. It can be change from the conf.json file.

### Responses

#### 200
**BODY** `json`
    
    array:
        string:"username"
        float:"score"
        int:"score_date"

## Wipe Database
:tw-1f512:`Auth Required`

#### Request
`DELETE` -> `{route}/wipe`

**Route** string
Url root of the api. It can be change from the conf.json file.

### Responses

#### 200
**BODY** `json`
    
    string:"succes"
	OR
	string:"error"

## Debug

#### Request
`GET` -> `{route}/debug`

**Route** string
Url root of the api. It can be change from the conf.json file.

### Responses

#### 200
**BODY** `json`
    
    bool:"debug"

## Feed
:tw-1f512:`Debug Mode Required`

#### Request
`POST` -> `{route}/feed`

**Route** string
Url root of the api. It can be change from the conf.json file.

#### Query

**count** int

### Responses

#### 200
**BODY** `json`
    
    string:"success"
	OR
	string:"error"

## Get Users
:tw-1f512:`Auth Required`

#### Request
`GET` -> `{route}/users`

**Route** string
Url root of the api. It can be change from the conf.json file.

### Responses

#### 200
**BODY** `json`
    
    array:
        int:"userID"
        string:"username"
        int:"created"
        int:"last_login"
        string:"last_ip"

## Post User
:tw-1f512:`Auth Required`

#### Request
`POST` -> `{route}/users`

**route** string

Url root of the api. It can be change from the conf.json file.

#### Query
**username** string

### Responses

#### 200
**BODY** `json`
    
    string:"success"
    OR
    string:"error"

## Get User
:tw-1f512:`Auth Required`

#### Request
`GET` -> `{route}/users/{username}`

**route** string

Url root of the api. It can be change from the conf.json file.

**username** string

### Responses **200**
**BODY** `json`
    
    int:"userID"
    string:"username"
    int:"created"
    int:"lastlogin"
    string:"last_ip"
    OR
    string:"error"

## Update User Last Login
:tw-1f512:`Auth Required`

#### Request
`PUT` -> `{route}/users/{username}`

**route** string

Url root of the api. It can be change from the conf.json file.

**username** string

### Responses **200**
**BODY** `json`
    
    string:"success"
    OR
    string:"error"

## Get User Scores
:tw-1f512:`Auth Required`

#### Request
`GET` -> `{route}/users/{username}/scores`

**route** string

Url root of the api. It can be change from the conf.json file.

**username** string

### Responses **200**
**BODY** `json`
    
    array:
        int:"scoreID"
        int:"userID"
        float:"score"
        int:"score_date"
    OR
    string:"error"

## Post User Score
:tw-1f512:`Auth Required`

#### Request
`POST` -> `{route}/users/{username}/scores`

**route** string

Url root of the api. It can be change from the conf.json file.

**username** string

#### Query

**score** int

### Responses **200**
**BODY** `json`
    
    string:"success"
    OR
    string:"error"