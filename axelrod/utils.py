import time


def timed_message(message, start_time):
    elapsed_time = time.time() - start_time
    return message + " in %.1fs" % elapsed_time
