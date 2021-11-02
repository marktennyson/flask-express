# Flask-Express - ExpressJs apis for Flask

<img src="https://raw.githubusercontent.com/marktennyson/flask-express/main/logos/flask-express-logo.png">

[![MIT licensed](https://img.shields.io/github/license/marktennyson/Flask-Tortoise)](https://raw.githubusercontent.com/marktennyson/Flask-Tortoise/master/LICENSE) [![GitHub stars](https://img.shields.io/github/stars/marktennyson/Flask-Tortoise.svg)](https://github.com/marktennyson/Flask-Tortoise/stargazers) [![GitHub forks](https://img.shields.io/github/forks/marktennyson/Flask-Tortoise.svg)](https://github.com/marktennyson/Flask-Tortoise/network) [![GitHub issues](https://img.shields.io/github/issues-raw/marktennyson/Flask-Tortoise)](https://github.com/marktennyson/Flask-Tortoise/issues) [![Downloads](https://pepy.tech/badge/Flask-Tortoise)](https://pepy.tech/project/Flask-Tortoise)

## Introduction

**Flask-Express** is here to give you the feel like ExpressJs while using the Flask app. Basically you can use the default Request and Response as two parameters of the view functions.

**Flask-Express** comes with all the features of **Flask** with some extra features.

We are using the munch module to provide the attribute-style access very similar to the Javascript. I think this is enough for the introdunction, let's dig into the **key features and the installation process.**

## Key Features
- It's provides you the feel of ExpressJs while using a **Python based framework.**
- The **Resquest** and The **Response** objects are easily available.
- It's clean and __ExpressJs__ like apis provides a very readble syntex of your code.
- Support of __Munch__ module gives a very advnatage and understandable **attribute type parameters**.
- Rich test cases support using __pytest__ module.
- **MKDocs** based advanced documentation system.

## Installation

The installation process is very similar to the **other Python module** installation process.
You can install it directly from the PYPI using **pip** or from the __source code__.


#### Install or update from PYPI
```bash
python -m pip install -U Flask-Express
```

#### Install from source code
```bash
git clone https://github.com/marktennyson/flask-express && cd flask-express 
python -m pip install -U .
```

## A Basic Demo
```python
inbuilt flask_express.FlaskExpress class
```python
from flask_express import FlaskExpress

app = FlaskExpress(__name__)

@app.get("/")
def index(req, res):
    return res.json(req.header)

@app.get("/index-2")
async def index_2(req, res):
    return res.json(req.header)
```