from flask_express import FlaskExpress
from flask import session, current_app
from flask.logging import create_logger
from flask_express.typing import Request, Response

app = FlaskExpress('flask-express-demo3')

app.config['SECRET_KEY'] = "this is the secret key."
app.config['MAKE_ASGI_APP'] = True
# app.config['ATTACHMENTS_FOLDER'] = 'templates'

@app.route("/")
async def index(req:Request, res:Response):
    context = dict(name="Aniket sarkar", description="basic demo page.")
    return res.json(context)



if __name__ == "__main__":
    app.run(debug=True)