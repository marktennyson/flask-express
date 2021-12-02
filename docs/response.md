# Response Class

Flask-Express has it's own `munch` based `Response` class to get all the response based params.

## API of Response Class

__class `flask_express.response.Response(*wargs, **kwargs)`__

**Bases**: `flask.wrappers.Response`    

The default response class for flask-express app.

### All the available methods are listed below: 

#### **attachment(file_name: str)**

send the attachments by using this method. The default attachment folder name is attachments. You can always change it by changing the config parameter. the config parameter is ATTACHMENTS_FOLDER.

**Parameters** `file_name` – the file you want to server as attachment.

```python
@app.route('/attachments') 
def attach(req, res):
    filename = req.query.filename 
    return res.attachment(file_name)
```

**from version 1.0.4 `flask-express` started supporting to set the downloadable name for the attachments.**

```python
from datetime import datetime

@app.route('/attachments')
def attach(req, res):
    filename = req.query.filename
    now = datetime.now()
    dl_filename = f'{filename.rsplit(".", 1)[0]}_{now.strftime("%Y%m%d-%I%M%S")}.{filename.rsplit(".", 1)[1]}'
    return res.attachment(file_name, download_name=dl_filename)
```

#### **clear_cookie(key: str, path: str = '/', domain: Optional[str] = None, secure: bool = False, httponly: bool = False, samesite: Optional[str] = None)→ Type[flask_express.response.Response]**

Clear a cookie. Fails silently if key doesn’t exist.

**Parameters**   

- __key__ – the key (name) of the cookie to be deleted.

- __path__ – if the cookie that should be deleted was limited to a path, the path has to be defined here.

- __domain__ – if the cookie that should be deleted was limited to a domain, that domain has to be defined here.

- __secure__ – If True, the cookie will only be available via HTTPS.

- __httponly__ – Disallow JavaScript access to the cookie.

- __samesite__ – Limit the scope of the cookie to only be attached to requests that are “same-site”.

#### **end(code: Optional[int] = None)**

end the current resonse process. :param code: provide the web error code, if you want to close this response with a http error. 

**for example:**

```python
@app.route("/end")
def ender(req, res):
    return res.end()
    #or
    return res.end(404) # to raise a 404 error.
```

#### **flash(message: str, category: str = 'info')→ Type[flask_express.response.Response]**

to flash a message.

**Parameters**

* **message** – the message to flash.

* **category** – the category of flash message. Default is “info”.

__for example:__

```python
@app.route('/flash')
def flasher(req, res):
    return res.flash("this is the flash message").end()
```

#### **get(key: str)→ str**

get the response headers.

**Parameters**

* **key** – the key to get the headers from response.

__For example:__
```python
@app.route(“/get”) 
def getter(req, res):
    print (res.get(“Content-Type”)) 
    return res.end()
```

#### **json(*wargs: Any, **kwargs: Any)→ Type[flask_express.response.Response]**

return the json seriliazed data.

**Parameters**

* __wargs__ – dict or list type value.

* __kwargs__ – kwargs type value. it will create a dictionary with the provided values of kwargs. 

**for example:**

```python
@app.route("/json")
def jsoner(req, res):
    return res.json(name="aniket sarkar")
    #or
    return res.json({'name': 'aniket sarkar'})
    #or
    return res.json([1,2,3,4])
```

#### **make_response(response: Optional[Union[Iterable[bytes], bytes, Iterable[str], str]] = None, status: Optional[Union[int, str, HTTPStatus]] = None, headers: Optional[Union[Mapping[str, Union[str, int, Iterable[Union[str, int]]]], Iterable[Tuple[str, Union[str, int]]]]] = None, mimetype: Optional[str] = None, content_type: Optional[str] = None, direct_passthrough: bool = False)→ Type[ResponseBase]**

the base function for this class to create the final response.


#### **redirect(route: str)**

redirect to specified route.

__Parameters__

* **route** – str based value, the default path where you want to redirect.

**for example:**

```python
@app.post('/login') 
def login(req, res):
    #if login success 
    return res.redirect('/dashboard')
```

#### **render(template_or_raw: str, *wargs: Any, **context: Any)→ Type[str]**

Renders a html and sends the rendered HTML string to the client.

**Parameters**

* __template_or_raw__ – provide the template name or the html string to be rendered.

* __wargs__ – The dictionary type context for the jinja2 template.

* __context__ – the kwargs type context for the jinja2 template.

**For example:**

```python
@app.route('/render') 
def renderer(req, res):
    context=dict(name="Aniket Sarkar", planet="Pluto") 
    return res.render("index.html", context) 
    #or 
    return res.render("index.html", name="Aniket Sarkar", planet="Pluto")
```

#### **send(content: Union[str, dict, List[Any]])→ Type[flask_express.response.Response]**

Sends the HTTP response.

**Parameters**

* **content** – the content to send.

**for example:**

```python
@app.route("/send")
def sender(req, res):
    return res.send("hello world")
    #or
    return res.send("<h1>hello world</h1>")
    #or
    return res.set_status(404).send("not found")
```

#### **send_file(path_or_file: Union[PathLike, str, BinaryIO], mimetype: Optional[str] = None, as_attachment: bool = False, download_name: Optional[str] = None, attachment_filename: Optional[str] = None, conditional: bool = True, etag: Union[bool, str] = True, add_etags: Optional[bool] = None, last_modified: Optional[Union[datetime, int, float]] = None, max_age: Optional[Union[int, Callable[[Optional[str]], Optional[int]]]] = None, cache_timeout: Optional[int] = None)→ Type[Response]**

Send the contents of a file to the client. Its internally using the send_file method from werkzeug.

__Parameters__

* **path_or_file** – The path to the file to send, relative to the current working directory if a relative path is given. Alternatively, a file-like object opened in binary mode. Make sure the file pointer is seeked to the start of the data. 

* **mimetype**: The MIME type to send for the file. If not provided, it will try to detect it from the file name.

* **as_attachment** – Indicate to a browser that it should offer to save the file instead of displaying it.

* **download_name** – The default name browsers will use when saving the file. Defaults to the passed file name.

* **conditional** – Enable conditional and range responses based on request headers. Requires passing a file path and environ.

* **etag** – Calculate an ETag for the file, which requires passing a file path. Can also be a string to use instead.

* **last_modified** – The last modified time to send for the file, in seconds. If not provided, it will try to detect it from the file path.

* **max_age** – How long the client should cache the file, in seconds. If set, Cache-Control will be public, otherwise it will be no-cache to prefer conditional caching.

#### **set(*wargs)**

set the default header.

__Parameters__

* **wargs** – dictionary or Headers type data.

__For example:__

```python
@app.route("/header-seter")
def header_setter(req, res):
    res.set('Content-Type', 'application/json')
    #or
    res.set({'Content-Type':'application/json'})
    return res.end()
```

#### **set_cookie(key: str, value: str = '', max_age: Optional[Union[timedelta, int]] = None, expires: Optional[Union[str, datetime.datetime, int, float]] = None, path: Optional[str] = '/', domain: Optional[str] = None, secure: bool = False, httponly: bool = False, samesite: Optional[str] = None)→ Type[Response]**

Sets a cookie.

A warning is raised if the size of the cookie header exceeds max_cookie_size, but the header will still be set.

__Parameters__

* __key__ – the key (name) of the cookie to be set.

* __value__ – the value of the cookie.

* __max_age__ – should be a number of seconds, or None (default) if the cookie should last only as long as the client’s browser session.

* __expires__ – should be a datetime object or UNIX timestamp.

* __path__ – limits the cookie to a given path, per default it will span the whole domain.

* __domain__ – if you want to set a cross-domain cookie. For example, domain=".example.com" will set a cookie that is readable by the domain www.example.com, foo.example.com etc. Otherwise, a cookie will only be readable by the domain that set it.

* __secure__ – If True, the cookie will only be available via HTTPS.

* __httponly__ – Disallow JavaScript access to the cookie.

* __samesite__ – Limit the scope of the cookie to only be attached to requests that are “same-site”.

#### **send_status(code: int)→ Type[flask_express.response.Response]**

set the web response status code. 

__Parameters__ 

* **code** - The web response status.

__For example:__

```python
@app.route("/send-status")
def send_statuser(req, res):
    return res.send_status(404).send("your requested page is not found.")
```

#### **type(type: str)**

Sets the Content-Type HTTP header to the MIME type as determined by the specified type.

**Parameters**

- **type** – The desired mine type to set.

```python
@app.route("/set-mime")
def mimer(req, res):
    res.type('application/json')
    #or
    res.type(".html")
    #or
    res.type("json")
```