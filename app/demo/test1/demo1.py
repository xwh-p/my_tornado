import json
import time
import asyncio
import tornado
from sqlalchemy import text

from app.demo import base


class TTT(base.BaseORMHandler):
    _tableclass = None

    async def get(self):
        # id = self.get_argument('id')
        # val = tornado.escape.json(self.request.body)

        connect = await self.connect()
        async with connect.begin():
            sql_obj = await connect.execute(text("select * from student"))
            result = [dict(v) for v in await sql_obj.fetchall()]
        self.write_json(data=result)


class TTT1(base.BaseORMHandler):

    async def ss(self):
        asyncio.sleep(11)

    async def get(self):
        await self.ss()
        self.write_json(data='wwww')
