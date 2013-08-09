import logging
import os
import web

log_level = logging.DEBUG
logger = logging.getLogger('main')
logger.setLevel(log_level)
ch = logging.StreamHandler()
ch.setLevel(log_level)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def is_test():
    if 'WEBPY_ENV' in os.environ:
        return os.environ['WEBPY_ENV'] == 'test'

if is_test():
    DB = web.database(dbn='mysql', host='localhost', db='systems_test', user='sot', pw='sot')
else:
    DB = web.database(dbn='mysql', host='localhost', db='systems', user='sot', pw='sot')

is_production = True
cache = is_production

#SendGrid
sd_username = 'user'
sd_password = 'pass'
