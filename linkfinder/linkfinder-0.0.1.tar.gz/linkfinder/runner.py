

class Runner(object):

    def __init__(self, driver, source):
        self.driver = driver
        self.source = source

    def run(self):
        endpoints = self.source.retrieve_endpoints()
        self.driver.process(endpoints)


class SimpleRunner(Runner):

    def run(self):
        super(SimpleRunner, self).run()

    def print_results(self):
        while not self.driver.queue.empty():
            status, url = self.driver.queue.get_nowait()
            print url + " returned: " + str(status)


def get_runner(driver, source):
    return SimpleRunner(driver=driver, source=source)
