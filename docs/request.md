# Request Class

Flask-Express has it's own `munch` based `Request` class to get all the request based params.

## API of Request Class

**class `flask_express.request.Request(*wargs, **kwargs)`**

__Bases__: `flask.wrappers.Request`

__The default response class for the flask-express app.__

#### **property** `body`: `Type[flask_express.munch.Munch]`      
it provides you the form based data.

 
#### **property** `header`: `Type[flask_express.munch.Munch]`      
it provides you the headers based data.

 
#### **property** `json`: `Type[flask_express.munch.Munch]`   
it provides you the json based data.

 
#### **property** `query`: `Type[flask_express.munch.Munch]`      
it provides you the args based data.

 
#### **property** `session`: `Type[flask.session.SessionMixin]`      
it provides you the default session object of flask globals as a property of `request.Request` class.

**Added in version 1.0.4**

#### **set_session(key:Any, value:Any) -> Type[flask.session.SessionMixin]**
Set the session object by providing the kay value name.

**Parameters** `key` – the key name.    
**Parameters** `value` – the value for the provided key.

```python
@app.route('/set-session') 
def ss(req, res):
    req.set_session('name', 'aniket')
    return res.send("OK)
```

#### **set_sessions(key_value:Tuple[Any, Any]) -> Type[flask.session.SessionMixin]**
set multiple sessions at a same time by sending the key, value pair in a tuple.

**Parameters:** `key_value` - Tuple of the key-value pair

```python
@app.get("/set-sessions")
def sss(req, res):
    req.set_sessions(('name_1', 'aniket'), ('name_2', 'sarkar'))
    return res.send('OK')
```

#### **get_session(key:Any) -> Any**
Get the session value as per the provided key name.

**Parameters** `key` – the key name to fetch teh mapped value.    

```python
@app.route('/get-session') 
def gs(req, res):
    req.get_session('name')
    return res.send("OK)
```