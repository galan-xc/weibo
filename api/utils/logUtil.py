import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s(%(name)s)- %(pathname)s:%(module)s:%(funcName)s-> %(message)s'
)
logger = logging.getLogger('log')

