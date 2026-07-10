import time


class StreamingMetrics:

    def __init__(self):

        self.transactions = 0

        self.start = time.time()

    def update(self):

        self.transactions += 1

    def throughput(self):

        elapsed = time.time() - self.start

        return round(

            self.transactions / elapsed,

            2

        )
