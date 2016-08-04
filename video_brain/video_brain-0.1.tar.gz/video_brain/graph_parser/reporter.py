
class Reporter():

    def __init__(self):

        self.nb_images = 0
        self.corpus_images = None
        self.imagenet_images = {}

    def add_imagenet_informations(self, X, y):

        self.imagenet_images['total'] = len(X)


    class Factory:
        reporter = None

        def create(self):
            if not Reporter.Factory.interpreter:
                Reporter.Factory.interpreter = Reporter()

            return self.reporter