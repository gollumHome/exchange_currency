from datetime import timedelta

# 指定broker
BROKER_URL = 'redis://127.0.0.1:6379'
# 指定backend
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

# 指定时区
CELERY_TIMEZONE = 'Asia/Shanghai'

# 指定导入的任务模块
CELERY_IMPORTS = (
    'celerys.tasks',
)

# 定时调度schedules
CELERYBEAT_SCHEDULE = {
    'settle_job': {
        'task': 'celerys.tasks.settle_job',
        'schedule': timedelta(seconds=12),  # 每12秒执行一次
        'args': (),  # 任务函数参数
        'options': {'queue': 'CELERY_SCHEDULE_QUEUE'}
    },
    'recove_order_job': {
        'task': 'celerys.tasks.recove_order_job',
        'schedule': timedelta(seconds=20),  # 每20秒执行一次
        'args': (),  # 任务函数参数
        'options': {'queue': 'CELERY_SCHEDULE_QUEUE'}
    },
    'query_wx_order_job': {
        'task': 'celerys.tasks.query_wx_order_job',
        'schedule': timedelta(seconds=10),  # 每10秒执行一次
        'args': (),  # 任务函数参数
        'options': {'queue': 'CELERY_SCHEDULE_QUEUE'}
    },
    'cycle_get_token_job': {
        'task': 'celerys.tasks.cycle_get_token_job',
        'schedule': timedelta(seconds=6000),  # 每6000秒执行一次
        'args': (),  # 任务函数参数
        'options': {'queue': 'CELERY_SCHEDULE_QUEUE'}
    },
    'reward_rank_job': {
        'task': 'celerys.tasks.reward_rank_job',
        'schedule': timedelta(seconds=45),  # 每45秒执行一次
        'args': (),  # 任务函数参数
        'options': {'queue': 'CELERY_SCHEDULE_QUEUE'}
    },
    'complete_enrolls_job': {
        'task': 'celerys.tasks.complete_enrolls_job',
        'schedule': timedelta(seconds=10),  # 每10秒执行一次
        'args': (),  # 任务函数参数
        'options': {'queue': 'CELERY_SCHEDULE_QUEUE'}
    },
    'recove_reward_job': {
        'task': 'celerys.tasks.recove_reward_job',
        'schedule': timedelta(seconds=10),  # 每10秒执行一次
        'args': (),  # 任务函数参数
        'options': {'queue': 'CELERY_SCHEDULE_QUEUE'}
    },
    'complete_groups': {
        'task': 'celerys.tasks.complete_groups',
        'schedule': timedelta(seconds=60),  # 每60秒执行一次
        'args': (),  # 任务函数参数
        'options': {'queue': 'CELERY_SCHEDULE_QUEUE'}
    },
    'close_timeout_activity': {
        'task': 'celerys.tasks.close_timeout_activity',
        'schedule': timedelta(seconds=60),  # 每60秒执行一次
        'args': (),  # 任务函数参数
        'options': {'queue': 'CELERY_SCHEDULE_QUEUE'}
    },
    'remove_timeout_member': {
        'task': 'celerys.tasks.remove_timeout_member',
        'schedule': timedelta(seconds=60),  # 每60秒执行一次
        'args': (),  # 任务函数参数
        'options': {'queue': 'CELERY_SCHEDULE_QUEUE'}
    },
    "enroll_statics": {
        'task': 'celerys.tasks.enroll_statics',
        'schedule': timedelta(seconds=60),  # 每60秒执行一次
        'args': (), # 任务函数参数
        'options': {'queue': 'CELERY_SCHEDULE_QUEUE'}
    },
    "assist_rank_job": {
        'task': 'celerys.tasks.assist_rank_job',
        'schedule': timedelta(seconds=120),  # 每120秒执行一次
        'args': (),  # 任务函数参数
        'options': {'queue': 'CELERY_SCHEDULE_QUEUE'}
    },
    "query_transfers_job": {
        'task': 'celerys.tasks.query_transfers_job',
        'schedule': timedelta(seconds=30),  # 每30秒执行一次
        'args': (),  # 任务函数参数
         'options': {'queue': 'CELERY_SCHEDULE_QUEUE'}

    }
}
