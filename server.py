import asyncio,aioredis

import tornado.options
import tornado.web
import tornado.locks
from aiomysql.sa import create_engine

import config
from app.routes import routes

tornado.options.define("host",default="",help="server host")

tornado.options.define('port',default=8000)

class AttrDict(dict):
    def __init__(self,*args,**kwargs):
        super(AttrDict,self).__init__(*args,**kwargs)
        self.__dict__ = self


class Applicate(tornado.web.Application):
    async def initalize(self,loop):
        self.loop = loop
        self.config = AttrDict(config.config)

        self.engine = await create_engine(**self.config.db_params)
        # self.redis_client = await aioredis.create_redis(**self.config.redis_url)


if __name__ == '__main__':
    tornado.options.parse_command_line()

    settings = {'debug':True}
    app = Applicate(routes,cookie_secret=config.config['secret'],**settings)

    app.listen(tornado.options.options.port,tornado.options.options.host)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.initalize(loop))
    print("port:",tornado.options.options.port)
    loop.run_forever()







