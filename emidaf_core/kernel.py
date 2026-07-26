class Kernel:

    def __init__(self):

        self.bootstrap = Bootstrap()

    def start(self):

        self.bootstrap.initialize()