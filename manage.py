# coding: utf-8

import os
import sys
import logging

from flask_docs import ApiDoc
from flask_cors import CORS
from flask_request_params import bind_request_params

from apps import create_app
from apps import db
from apps.get_middleware import StripContentTypeMiddleware
from SchedulerService import SchedulerApi
logger = logging.getLogger(__name__)
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
print(os.getenv('FLASK_CONFIG'))
app.before_request(bind_request_params)
ApiDoc(app)

CORS(app, resources={r"/*": {"origins": "*"}})
app.wsgi_app = StripContentTypeMiddleware(app.wsgi_app)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logger.info('系统准备启动了::: ')
    app.secret_key = 'x-ci-dm'
    app.run(host='127.0.0.1', port=8000)
