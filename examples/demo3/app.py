from flask_express import FlaskExpress
from flask import session, current_app
from flask_express.typing import Request, Response

import uvicorn as uv 


app = FlaskExpress('flask-express-demo3')

app.config['SECRET_KEY'] = "this is the secret key."
app.config['MAKE_ASGI_APP'] = True
app.testing = True
# app.config['ATTACHMENTS_FOLDER'] = 'templates'

@app.route("/")
async def index(req:Request, res:Response):
    context = dict(name="Aniket sarkar", description="basic demo page.")
    return res.json(context)

@app.route("/aniket")
async def aniket(req:Request, res:Response):
    context = dict(name="Aniket sarkar", description="basic demo page.")
    return res.json(context)


if __name__ == "__main__":
    
    uv.run(app=app, debug=True)
    # app.run(debug=True)