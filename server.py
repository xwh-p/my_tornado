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







# 获取JSON参数
# import tornado.escape
# print(tornado.scape.json decode(self.request,body))
# 建立连接
# engine = create_engine(config.config['db_ur1'])
# Session = sessionmaker(engine) session = Session()
# 原生sql
# res = session.execute("select * from users")
# print(pd.DataFrame([dict(zip(i.keys(), i)) for i in res]))
# ORM
# s = session.query(auth.User).all()
# print([i.email for i in s])

# 异步查询
# stmt = select([auth.User]).where(auth.User.id != 0)
# rp = await connect.execute(stmt)
# tablegroups = [dict(v) for v in await rp.fetchall]
# 异步原生查询
# a = await connect.execute(text("select * from datasets"))
# print([dict(v) for v in await a.fetchall()])
# join 查询
# connect = await self.connect()
# async with connect.begin():
# TDT = model.TestReportDatasetTable
# j = join(TDT,model.Dataset,model.Dataset.id==TDT.dataset_id)
# stmt = select([TDT,model.Dataset.status]).select_from(j)

# 三张表查询
# j = join(join(TDT,model.Dataset, model.Dataset.id == TDT.dataset_id), model.TestReport,TDT.test_report_id==model.TestReport.id)
# stmt = select([TDT, model.Dataset.status,model.TestReport. run_time]). select_from(j).where(TDT,id==18)
# rp = await connect.execute(stmt)
# res = [dict(v) for v in await rp.fetchal1()]


# 插入操作
# i = insert(model.Dataset).values(t"name":"2021-03-08 10:38:06""test_run_id": 120，"status": "completed"]) await connect.execute(i)

# 更新操作
# connect = await self.connect() async with connect.begin():
# await connect.execute(update(model.ReportTemplate).where(model.ReportTemplate.id == o.id).values(('params’: o.params]))



