## 0.1.0
- renamed the module name to flask-express from flaske to make it a extension of Flask.

## 0.1.1

- Some typo fixed at README.md.
- Some typo fixed at Munch module.
- Added the proper logo.

## 0.1.2
- Fixed `flask-admin` related issue.
- Added __MKDocs__ based documentation.

## 0.1.3
- Fixed attachment directory related issue
- Now the user have the power to add custom attachment folder.
- showing proper error message when attached file is absent at the attachment directory.
- added more CamelCase method to the `response.Response` class.
- Fixed `issubclass` checking error for different contents at `response.Response.send` method.
- Fixed `status_code` method for `response.Response` class not working.
- Fixed `response.Response.type` method.
- Renamed `response.Response.set_staus` and `response.Response.setStatus` methods to `response.Response.send_status` and `response.Response.sendStatus` responsively.
- Added more documentation.
- docstring typo fixed at `request.Request` class.
- Added more test cases.
- Changed the License from **GPL** to **MIT**.

## 0.1.4
- Added `download_name` features to the `Response.attachment` method to set the downloadable name of the attachment file.
- Added `set_session` and `get_session`, two methods to set and get data from the session object.
- Added `set_sessions` method to add multiple records at a single time to the session object.
- Version update of some dependencies.