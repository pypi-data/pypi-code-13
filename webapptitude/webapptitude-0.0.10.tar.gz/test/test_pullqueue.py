
from webapptitude import pullqueue
from webapptitude import testkit
from webapptitude import WSGIApplication

class PullQueueTestCase(testkit.TestCase):

    @classmethod
    def preparePullQueueHandler(cls, queueName):

        class TestQueue(pullqueue.PullQueue):

            state = {}

            def run(self, value=0):
                self.state['value'] = self.state.pop('value', 1) * value

        return TestQueue(queueName)

    @classmethod
    def getHandlers(cls):
        cls.queue = cls.preparePullQueueHandler('testpullqueue')
        app = WSGIApplication(debug=True)
        app.route('/test', cls.queue.requesthandler)
        return app


    def testPullQueueHandler(self):
        self.queue.enqueue(
            self.queue.task(value=1),
            self.queue.task(value=2),
            self.queue.task(value=3)
        )

        response = self.testapp.get('/test')
        self.assertEqual(response.json_body['processed_tasks'], 3)
        self.assertEqual(self.queue.state['value'], 6)

