# -*-coding:UTF-8-*-
import uuid
import os


class Handle(object):

    def __init__(self, cli, volume_path):
        self.cli = cli
        self.volume_path = volume_path

    def __call__(self, code):
        name = uuid.uuid4()
        path = '{}{}.py'.format(self.volume_path, name)
        with open(path, 'w') as f:
            f.write(code)
        image = self.cli.images(name='haruna')[0]
        self.container = self.cli.create_container(
            name=name,
            image=image.get('Id'),
            command='python {}.py'.format(name),
            volumes='/app',
            host_config=self.cli.create_host_config(binds={
                self.volume_path: {
                    'bind': '/app',
                    'mode': 'ro'
                }}, mem_limit='64m'
            )
        )
        self.cli.start(self.container.get('Id'))
        result = self.cli.logs(self.container, stdout=True)
        os.remove(path)
        return result


class Task(object):

    def __init__(self, mq, cli, volume_path):
        self.mq = mq
        self.cli = cli
        self.volume_path = volume_path

    def run(self):
        self.mq.register(Handle(self.cli, self.volume_path))
        self.mq.run()
