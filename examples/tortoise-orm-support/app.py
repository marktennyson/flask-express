# from flask import jsonify, Flask
from flask_express import FlaskExpress
from models import *
from random import choice
from script import GenerateData

import typing as t

if t.TYPE_CHECKING:
    from flask_express.typing import Request, Response


STATUSES = ["New", "Old", "Gone"]

app:"FlaskExpress" = FlaskExpress(__name__)
app.config['TORTOISE_ORM_DATABASE_URI'] = 'sqlite://db.sqlite3'
app.config['TORTOISE_ORM_MODELS'] = "models"

models.init_app(app)

@app.get("/")
async def list_all(req:"Request", res:"Response"):
    users = await Users.all()
    workers = await Workers.all()
    co_workers = await CoWorker.all()
    return res.json(
        {"users": [str(user) for user in users], "workers": [str(worker) for worker in workers], "co-wrokers": [str(co_worker) for co_worker in co_workers]}
    )


@app.get("/user")
async def add_user(req:"Request", res:"Response", ):
    user = await Users.create(status=choice(STATUSES))  # nosec
    return str(user)


@app.get("/worker")
async def add_worker(req:"Request", res:"Response", ):
    worker = await Workers.create(status=choice(STATUSES))  # nosec
    return str(worker)

@app.get("/get-worker")
async def get_worker(req:"Request", res:"Response", ):
    worker:"Workers" = await Workers.get(id=1)
    return str(worker.status)

@app.get("/co-workers")
async def co_workers(req:"Request", res:"Response", ):
    user = await Users.get(id=1)
    co_worker:"CoWorker" = await CoWorker.create(name="Aniket Sarkar", rltn=user)
    return str(co_worker)

@app.get("/get-coworker/<int:id>")
async def aniket(req:"Request", res:"Response", id):
    pk=id
    co_worker =await CoWorker.get_or_404(pk=pk, description=f"user object not found at ID: {pk}")
    return res.json(name=str(co_worker.name))

@app.get("/delete-coworker/<int:id>")
async def delete_coworker(id):
    c = await CoWorker.get_or_404(id=id)
    await c.delete()
    return "object deleted"

@app.get("/sarkar")
async def sarkar(req:"Request", res:"Response", ):
    user = await Users.filter(pk=1).first_or_404()
    return res.json(name=str(user))

@app.get("/paginate")
async def paginator(req:"Request", res:"Response", ):
    user = await Users.paginate()
    print (user)
    return res.send("none")

@app.get("/create-data")
async def create_data(req:"Request", res:"Response"):
    r1 = await GenerateData.generate_user()
    r2 = await GenerateData.generate_worker()
    r3 = await GenerateData.generate_co_worker()
    return res.send("Done")

@app.get("/create-co-worker")
async def create_co_worker(req:"Request", res:"Response"):
    await GenerateData.generate_co_worker()
    return res.send("Done")

if __name__ == '__main__':
    app.run(debug=True, port=8080)