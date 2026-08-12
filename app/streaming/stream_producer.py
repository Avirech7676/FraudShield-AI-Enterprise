from queue import Queue

from app.streaming.transaction_generator import TransactionGenerator


class StreamProducer:

    def __init__(self):

        self.queue = Queue()

        self.generator = TransactionGenerator()

    def produce(self):

        transaction = self.generator.generate()

        self.queue.put(transaction)

        return transaction
