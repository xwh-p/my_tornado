import datetime
import json

import cachetools as cachetools
import tornado.web


class JSONDateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat(' ')
        elif isinstance(o, (datetime.date, datetime.time)):
            return o.isoformat()
        else:
            return json.JSONEncoder.default(self, o)


class BaseHandler(tornado.web.RequestHandler):
    user_cache = cachetools.TTLCache(128, ttl=3600)

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.set_header("Access-Control-Allow-Origin", "*")

    def check_origin(self, origin):
        return True

    def option(self):
        self.set_header("Access-Control-Allow-Headers",
                        "Origin,X-Requested-With,Content-Type,Accept")

        self.set_header("Access-Control-Allow-Methods",
                        "POST,GET,PUT,PATCH,DELETE,OPTIONS")
        self.write('')

    def load_queryargs(self):
        conditions = {
            key: self.get_arguments(key)
            for key in self.request.arguments
            if self.get_argument(key, None) is not None
        }
        return conditions

    async def fetchall(self, res):
        return list(map(dict, (await res.fetchall())))

    async def connect(self):
        if not hasattr(self, '_connet') or self._connect is None:
            self._connect = await self.application.engine.acquire()

        return self._connect

    def on_finish(self):

        super().on_finish()
        print("进入app之后。。。。")
        if hasattr(self, '_bodyjson'):
            delattr(self, '_bodyjson')
        if hasattr(self, '_connect'):
            self.application.engine.release(self._connect)
            delattr(self, '_connect')

    def write_json(self, data, status_code=200, msg='ok'):
        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps({
            'code': status_code,
            'msg': msg,
            'data': data
        },cls=JSONDateTimeEncoder))


class BaseORMHandler(BaseHandler):
    _tableclass = None

    async def prepare(self):
        res = super().prepare()
        if res is not None:
            await res

        self.conn = await self.connect()
        print("进入之前--------")


class BaseCRUDHandler(BaseORMHandler):
    pass
