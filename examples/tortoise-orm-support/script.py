from models import *


class GenerateData(object):
    @classmethod
    async def generate_user(cls, count=5000):
        for i in range(count):
            user = await Users.create(status=f"User__{i}")
            user.save()
        return True

    @classmethod
    async def generate_worker(cls, count=5000):
        for i in range(count):
            worker = await Workers.create(status=f"Worker__{i}")
            worker.save()
        return True

    @classmethod
    async def generate_co_worker(cls, count=5000):
        for i in range(count):
            user = await Users.get(id=i+1)
            print ("user:", user)
            co_worker = await CoWorker.create(name=f"Co-Worker_{str(i)}", rltn=user)
            co_worker.save()
        return True