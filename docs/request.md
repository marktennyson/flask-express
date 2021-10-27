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