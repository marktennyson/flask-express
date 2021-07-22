from flaske import Flask, current_app
from flaske.typing import Request, Response
from flask import make_response
import mimetypes

app = Flask(__name__)

@app.route("/")
async def index(req:Request, res:Response):
    context = dict(name="Aniket sarkar", description="basic demo page.")
    return res.render("index.html", context=context)

@app.route("/set-status")
def set_statuser(req:Request, res:Response):
    # return res.Response(json.dumps({"status":200}), mimetype="application/json")
    return res.set_status(404).send("your requested page is not found.")

@app.route("/mrp")
def mrp(req:Request, res:Response):
    # resp = make_response("file resp")
    print (res.headers)
    print (current_app.config.get("ATTACHMENTS_FOLDER"))
    # res.attachment("hello.txt")
    return res.send("hello world")

if __name__ == "__main__":
    app.run(debug=True)