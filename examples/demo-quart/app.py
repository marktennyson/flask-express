from quart import Quart, render_template, websocket

app = Quart(__name__)

@app.route("/")
async def hello():
    b=1/0
    return await render_template("index.html")

@app.route("/api")
async def json():
    return jso({"hello": "world"})

@app.websocket("/ws")
async def ws():
    while True:
        await websocket.send("hello")
        await websocket.send_json({"hello": "world"})

if __name__ == "__main__":
    app.run(debug=True)