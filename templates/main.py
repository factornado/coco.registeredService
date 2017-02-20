import os
import time
from tornado import ioloop, web, httpserver
import logging

from utils import Config

config = Config('config.yml')

logging.basicConfig(
    level=20,  # Set to 10 for debug logs.
    filename=config.conf['log']['file'],
    format='%(asctime)s (%(filename)s:%(lineno)s)- %(levelname)s - %(message)s',
    )
logging.Formatter.converter = time.gmtime
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('tornado').setLevel(logging.WARNING)
logging.info('='*80)


class Info(web.RequestHandler):
    def get(self):
        self.write(config.conf)


class Heartbeat(web.RequestHandler):
    def get(self):
        config.register()
        self.write("ok")


class SomeHandler(web.RequestHandler):
    def get(self, param=''):
        self.write(
            "Hello from service {}. "
            "You've asked for uri {}\n".format(
                config.conf['name'], param))

app = web.Application([
    ("/(swagger.json)", web.StaticFileHandler, {'path': os.path.dirname(__file__)}),
    ("/swagger", web.RedirectHandler, {'url': '/swagger.json'}),
    ("/heartbeat", Heartbeat),
    ("/info", Info),
    ("/(.*)", SomeHandler),
    ])

if __name__ == '__main__':
    port = config.get_port()  # We need to have a fixed port in both forks.
    logging.info('Listening on port {}'.format(port))
    time.sleep(2)  # We sleep for a few seconds to let the registry start.
    if os.fork():
        config.register()
        server = httpserver.HTTPServer(app)
        server.bind(config.get_port(), address='0.0.0.0')
        server.start(config.conf['threads_nb'])
        ioloop.IOLoop.current().start()
    else:
        ioloop.PeriodicCallback(config.heartbeat,
                                config.conf['heartbeat']['period']*1000).start()
        ioloop.IOLoop.instance().start()
