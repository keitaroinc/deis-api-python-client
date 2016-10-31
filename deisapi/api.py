import os
import requests
import json
import logging
import ConfigParser

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())

log_filename = os.path.join(os.getcwd(), 'error.log')
log.addHandler(logging.FileHandler(log_filename))

class DeisApi(object):

    def __init__(self):

        config = ConfigParser.RawConfigParser()
        config.read(os.path.join(os.path.expanduser('~'), '.keitaro', 'config.cfg')

        self.deis_domain = config.get('deis', 'deisDomain')
        self.deis_url = config.get('deis', 'deisUrl')
        self.deis_credentials = {
            'username': config.get('deis', 'deisUsername'),
            'password': config.get('deis', 'deisPassword')
        }

        response = requests.post(
            url='{}/v2/auth/login/'.format(self.deis_url),
            json=self.deis_credentials
        ).json()

        self.token = response['token']
        self.allowed_status_codes = [200, 404]

    def _generate_endpoint(self, path, query=''):
        return '{0}{1}'.format(self.deis_url, path)

    def call(self, method, **kwargs):

        response = None
        endpoint = self._generate_endpoint(kwargs.pop('path'))
        headers = {'Authorization': 'token {}'.format(self.token)}

        if method.lower() == 'get':
            response = requests.get(endpoint, headers=headers)
        elif method.lower() == 'post':
            data = {'id': '{}'.format(kwargs.pop('data', {})) }
            response = requests.post(endpoint, headers=headers, json=data)
        elif method.lower() == 'put':
            response = requests.put()
        elif method.lower() == 'delete':
            response = requests.delete()
        else:
            raise ValueError, 'Missing implementation for %s' % method

        if response.status_code not in self.allowed_status_codes:
            log.error('method:{0}\nurl: {1}\nstatus_code: {2}\ncontent: {3}\nrbody:{4}\nrheaders:{5}\nrurl:{6}'\
                      .format(method, response.url, response.status_code, response.content,
                              response.request.body, response.request.headers, response.request.url))

        return response.content

    def apps(self, path=None):
        if path is None:
            path = '/v2/apps/'
        return self.call(method='GET', path=path)

    def domains(self, domain, path=None):
        if path is None:
            path = '/v2/apps/{domain}/domains/'.format(domain=domain)
        return self.call(method='GET', path=path)

    def create_app(self, data, path=None):
        if path is None:
            path = '/v2/apps/'
        return self.call(method='POST', path=path, data=data)
