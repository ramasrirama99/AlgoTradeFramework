from timeit import default_timer as timer


class Benchmark:

    def __init__(self):
        self.start = -1
        self.end = -1

    def mark(self, message=''):
        if self.start is -1:
            self.start = timer()
        else:
            if self.end is -1:
                self.end = timer()
            print('{message:{fill}{align}{width}}-{time}'
                  .format(message=message, fill='-', align='<', width=30, time=(self.end - self.start)))
            self.start = -1
            self.end = -1
