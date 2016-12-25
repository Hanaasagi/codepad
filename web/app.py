# -*-coding:UTF-8-*-

import yaml
from bottle import route, run, error, template, request
from mqcli import Client


@error(404)
def not_found():
    return '404 Not Found'


@route('/', method='GET')
def index():
    return template('templates/index.html')


@route('/', method='POST')
def show_result():
    code = request.forms.get('code')
    result = cli.request(code).rstrip('LUVORC0=')
    length = len(code.split('\r\n'))
    line_no = reduce(lambda x, y: '{}<span>{}</span>\n'.format(x, y),
                     ([''] + range(1, length + 1)))
    return template('templates/result.html', line_no=line_no,
                    code=code, result=result)


if __name__ == '__main__':
    setting = {
        'setting_file': './setting.yaml'
    }

    with open(setting['setting_file'], 'r') as f:
        setting.update(yaml.load(f))

    cli = Client(setting['rabbitmq']['host'],
                 setting['rabbitmq']['username'],
                 setting['rabbitmq']['password'],
                 setting['rabbitmq']['queue_name'])

    run(host=setting['server']['host'], port=setting['server']['port'])
