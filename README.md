# flaske
<img src="https://raw.githubusercontent.com/marktennyson/flaske/main/logos/flaske-logo.png">
<br>

# Downloads
[![Downloads](https://pepy.tech/badge/flaske)](https://pepy.tech/project/flaske) [![Downloads](https://pepy.tech/badge/flaske/month)](https://pepy.tech/project/flaske/month) [![Downloads](https://pepy.tech/badge/flaske/week)](https://pepy.tech/project/flaske/week)
<br>

#### contributor wanted : feel free to contact me at aniketsarkar@yahoo.com

provide the interactive service like expressJs for the flask app.

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

##### You can use the python typing for a better view of the codes and auto complition.

```python
from flaske import Flask
from flaske.typing import Request, Response

app = Flask(__name__)

@app.get("/")
def index(req:Request, res:Response):
    return res.json(req.header)
```

### Basic Documentation

The officiaal and full documentation for this project is available at: https://flaske.vercel.app.
Here I have tried to provide some of the basic features of this project.

#### Request class:

##### property - json 
So if your app is receiving data as json format, you can use `json` property of the request class to access the data.
Basically it's internally using the `get_json` method to collect the data.    

For example:

```python
@app.post("/send-json")
def send_json(req, res):
    name = req.json.name
    email = req.json.email
    return res.json(name=name, email=email)
```