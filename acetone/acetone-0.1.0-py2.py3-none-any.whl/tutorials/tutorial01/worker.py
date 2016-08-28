from tutorials.tutorial01.dependencies import dependencies
from tutorials.tutorial01.data_sender import DataSender


class Worker(object):
    """
    This ":type data_sender:" bellow is very useful for code completion. It's because the type
    is known during runtime and unfortunately many IDEs ignore the descriptor protocol, for example
    PyCharm: https://youtrack.jetbrains.com/issue/PY-8936

    :type data_sender: tutorials.tutorial01.data_sender.DataSender
    """
    # You specify a dependency here, configure the dependencies and then you are ready to create
    # the 'Worker' instances.
    data_sender = dependencies.Dependency(DataSender)

    def do_the_job(self):
        for i in range(10):
            self.data_sender.send_data('#{0} Hello world!'.format(i))
