import time


class Logger(object):

    def log(self, message, start_time=None):
        if start_time is not None:
            elapsed_time = time.time() - start_time
            self.message = message + " in %.1fs" % elapsed_time
        else:
            self.message = message


class NullLogger(Logger):

    def log(self, message):
        pass


class ConsoleLogger(Logger):

    def log(self, message, start_time=None):
        super(ConsoleLogger, self).log(message, start_time)
        print self.message


class FileLogger(Logger):

    def __init__(self, log_file='./axelrod.log'):
        self.log_file = log_file

    def log(self, message, start_time=None):
        super(FileLogger, self).log(message, start_time)
        with open(self.log_file, 'a') as file:
            file.write(self.message + '\n')
