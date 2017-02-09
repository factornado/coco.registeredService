import socket
import yaml
import pymongo
import logging
import json
from tornado import httpclient

class Kwargs(object):
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            self.__setattr__(key, val)


class Config(object):
    def __init__(self, filename):
        self.conf = yaml.load(open(filename))
        self.mongo = Kwargs()
        _mongo = self.conf.get('db', {}).get('mongo', {})
        self.mongo = Kwargs(**{
            hostname: Kwargs(**{
                dbname: Kwargs(**{
                    collname: pymongo.MongoClient(
                        host['address'],
                        connect=False)[db['name']][coll['name']]
                    for collname, coll in _mongo.get('collection', {}).items()
                    if coll['database'] == dbname
                    })
                for dbname, db in _mongo.get('database', {}).items()
                if db['host'] == hostname
                })
            for hostname, host in _mongo.get('host', {}).items()
            })

    def get_port(self):
        if 'port' not in self.conf:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("", 0))
            self.conf['port'] = s.getsockname()[1]
            s.close()
        return self.conf['port']

    def heartbeat(self):
        request = httpclient.HTTPRequest(
            'http://localhost:{}/heartbeat'.format(self.get_port()),
            method='GET',
            )
        client = httpclient.HTTPClient()
        r = client.fetch(request, raise_error=False)
        logging.info('{} HEARTBEAT ({}).'.format(
                r.code, r.reason[:30]))

    def register(self):
        request = httpclient.HTTPRequest(
            '{}/register/{}/{}'.format(
                self.conf['heartbeat']['url'].rstrip('/'),
                self.conf['name'],
                self.conf['version'],
                ),
            method='POST',
            body=json.dumps({
                'url': 'http://{}:{}'.format(socket.gethostname(),
                                             self.get_port()),
                'config': self.conf,
                }),
            )
        client = httpclient.HTTPClient()
        r = client.fetch(request, raise_error=False)
        logging.info('{} REGISTER ({}).'.format(
                r.code, r.reason[:30]))
