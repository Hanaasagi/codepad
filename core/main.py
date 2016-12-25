#!/usr/bin/env python
# -*-coding:UTF-8-*-

import os
import yaml
import time
from task import Task
from docker import Client
from rabbitmq import RabbitMQ


setting = {
    'setting_file': './setting.yaml'
}


def load_setting():
    with open(setting['setting_file'], 'r') as f:
        setting.update(yaml.load(f))


if __name__ == '__main__':
    load_setting()
    cli = Client(base_url='unix://var/run/docker.sock')
    pid = os.fork()
    if pid == 0:
        # 子进程
        def run():
            mq = RabbitMQ(setting['rabbitmq']['host'],
                          setting['rabbitmq']['username'],
                          setting['rabbitmq']['password'],
                          setting['rabbitmq']['queue_name'])
            task = Task(mq, cli, setting['docker']['volume_path'])
            task.run()
        print('codepad is running')
        run()
    else:
        # 父进程
        while True:
            for container in cli.containers(all=True):
                if time.time() - container['Created'] > setting['timeout']:
                    cli.remove_container(
                        container=container.get('Id'), force=True)
            time.sleep(60)
