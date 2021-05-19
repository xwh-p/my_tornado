import sys

host = '127.0.0.1'
config = {
    'db_params':{
        'host':host,
        'port':3306,
        'user':'root',
        'password':'12345678',
        'db':'tornado',
        'autocommit':False,
    },

    'redis_params':{
        'host':host,
        'db':1,
        'port':6379
    },

    'secret':'123213'
}


config['db_url'] = 'mysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4'.format(**config['db_params'])
config['redis_url'] = 'redis://{host}:{port}'.format(**config['redis_params'])