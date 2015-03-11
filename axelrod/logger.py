class NullLogger(object):

    def log(self, message):
        pass


class ConsoleLogger(object):

    def log(self, message):
        print message


class FileLogger(object):

    def __init__(self, log_file):
        self.log_file = log_file

    def log(self, message):
        with open(self.log_file, 'a') as file:
            file.write(message + '\n')
