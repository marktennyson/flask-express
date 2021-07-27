# flaske
<img src="https://raw.githubusercontent.com/marktennyson/flaske/main/logos/flaske-logo.png">

# Downloads
[![Downloads](https://pepy.tech/badge/flaske)](https://pepy.tech/project/flaske) [![Downloads](https://pepy.tech/badge/flaske/month)](https://pepy.tech/project/flaske/month) [![Downloads](https://pepy.tech/badge/flaske/week)](https://pepy.tech/project/flaske/week)
<br>

#### contributor wanted : feel free to contact me at aniketsarkar@yahoo.com    

provide the interactive service like expressJs for the flask app.


#### Important Links
[PYPI link](https://pypi.org/project/flaske)    
[Github link](https://github.com/marktennyson/flaske)    
[Documentation link](https://flaske.vercel.app) 

### Basic installation
Use the package manager [pip](https://pypi.org/project/flaske/) to install flaske.

```bash
python3 -m pip install flaske
```
Install from source code

```bash
git clone https://github.com/marktennyson/flaske.git && cd flaske/
python3 setup.py install
```

### Introduction to Flaske
Flaske is here to give you people the feel like ExpressJs while using the Flask app.
Basically you can use the default Request and Response as two parameters of the view functions.

Flaske comes with all the features of Flask with some extra features.

We are using the `munch` module to provide the attribute-style access very similar to the Javascript.
I think this is enough for the introdunction, let's play with the examples mentioned below.

### Examples and Usages

##### Basic example: 

```python
from flaske import Flask

app = Flask(__name__)

@app.get("/")
def index(req, res):
    return res.json(req.header)
```

##### Now the flask 2.0 support the asynchronus view function. You can implement this with flaske too.

```python
from flaske import Flask

app = Flask(__name__)

@app.get("/")
async def index(req, res):
    return res.json(req.header)
```

##### You can use the python typing for a better view of the codes and auto completion.

```python
from flaske import Flask
from flaske.typing import Request, Response

app = Flask(__name__)

@app.get("/")
def index(req:Request, res:Response):
    return res.json(req.header)
```

### Basic Documentation

The official and full documentation for this project is available at: https://flaske.vercel.app.
Here I have tried to provide some of the basic features of this project.

#### Request class:
N.B: all of the properties of the Request class will return an instance of Munch.
This will provide you the feel of the Javascript object.

##### property - json 
So if your app is receiving data as json format, you can use `json` property of the request class to access the data.
It's internally using the `get_json` method to provide the data.    

For example:

```python
@app.post("/send-json")
def send_json(req, res):
    name = req.json.name
    email = req.json.email
    return res.json(name=name, email=email)
```

##### property - query
This object provides you the url based parameter. 
It's internally using the `args` property to provide the data. 

For example:

```python
@app.get("/get-query")
def get_query(req, res):
    name=req.query.name
    email = req.query.email
    return res.send(dict(name=name, email=email))
```

##### property - body
This object provides you the all the parameters from the Form. 
It's internally using the `form` property to provide the data. 

For example:

```python
@app.get("/get-form-data")
def get_form_data(req, res):
    name=req.body.name
    email = req.body.email
    return res.send(dict(name=name, email=email))
```

##### property - header
This object provides you the all the parameters of the request header. 
It's internally using the `header` property to provide the data. 

For example:

```python
@app.get("/get-form-data")
def get_form_data(req, res):
    return res.send(req.header)
```

#### Response class

##### function - set_status
This is used to set the response header status.

for example:
```python
@app.route("/set-status")
def set_statuser(req, res):
    return res.set_status(404).send("your requested page is not found.")
```

##### function - flash
To flash a message at the UI.

for example:
```python
@app.route('/flash')
def flasher(req, res):
    return res.flash("this is the flash message").end()
```

##### function - send
 It sends the HTTP response.

for example:
```python
@app.route("/send")
def sender(req, res):
    return res.send("hello world")
    #or
    return res.send("<h1>hello world</h1>")
    #or
    return res.set_status(404).send("not found")
```

##### function - json
 To return the json seriliazed response.

for example:
```python
@app.route("/json")
def jsoner(req, res):
    return res.json(name="aniket sarkar")
    #or
    return res.json({'name': 'aniket sarkar'})
    #or
    return res.json([1,2,3,4])
```

##### function - end
 To end the current resonse process.

for example:
```python
@app.route("/end")
def ender(req, res):
    return res.end()
    #or
    return res.end(404) # to raise a 404 error.
```

##### function - render
 Renders a html and sends the rendered HTML string to the client.

for example:
```python
@app.route('/render')
def renderer(req, res):
    context=dict(name="Aniket Sarkar", planet="Pluto")
    return res.render("index.html", context)
    #or
    return res.render("index.html", name="Aniket Sarkar", planet="Pluto")
```

##### function - redirect
 redirect to specified route.

for example:
```python
@app.post("/login")
def login(req, res):
#if login success
return res.redirect("/dashboard")
```

##### function - get
Get the header information by the given key.

for example:
```python
@app.route("/get")
def getter(req, res):
    print (res.get("Content-Type"))
    return res.end()
```

##### function - set
Set the header information.

for example:
```python
@app.route("/header-seter")
def header_setter(req, res):
    res.set('Content-Type', 'application/json')
    #or
    res.set({'Content-Type':'application/json'})
    return res.end()
```

##### function - type
Sets the Content-Type HTTP header to the MIME type as determined by the specified type.

for example:
```python
@app.route("/set-mime")
def mimer(req, res):
    res.type('application/json')
    #or
    res.type(".html")
    #or
    res.type("json")
```

##### function - attachment
send the attachments by using this method.
The default attachment folder name is `attachments`.
You can always change it by changing the config parameter.
the config parameter is `ATTACHMENTS_FOLDER`.

for example:
```python
@app.route('/attachments')
def attach(req, res):
    filename = req.query.filename
    return res.attachment(file_name)
```

##### function - send_file
Send the contents of a file to the client.Its internally using the send_file method from werkzeug.

##### function - clear_cookie
Clear a cookie.  Fails silently if key doesn't exist.

##### function - set_cookie
Sets a cookie.

##### function - make_response
make a http response. It's same as `Flask.wrappers.Request`

### Development

#### Contribution procedure.
1. Form and clone this repository.
2. Make some changes as required.
3. Write unit test to showcase its functionality.
4. Submit a pull request under `development` branch.

#### Run this project on your local machine.
1. create a virtual environment on the project root directory.
2. install all the required dependencies from requirements.txt file.
3. make any changes on you local code.
4. then install the module on your virtual environment using `python setup.py install` command.
5. The above command will install the `flaske` module on your virtual environment.
6. Now create a separate project inside the example folder and start testing for your code changes.
7. If you face any difficulties to perform the above steps, then plese contact me at: `aniketsarkar@yahoo.com`.