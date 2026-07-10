import time

from app.streaming.stream_producer import StreamProducer

from app.streaming.stream_consumer import StreamConsumer
from app.streaming.metrics import StreamingMetrics

class StreamEngine:

    def __init__(self):

        self.producer = StreamProducer()

        self.consumer = StreamConsumer()
        self.metrics = StreamingMetrics()

    def start(self):

        print("Live Streaming Started")

        while True:

            transaction = self.producer.produce()
            start_time = time.perf_counter()
            prediction = self.consumer.consume(transaction)
            latency = (time.perf_counter() - start_time) * 1000
            self.metrics.update()

            print(
                  f"Transaction : {transaction['transaction_id']}\n"
                  f"Prediction  : {prediction['Prediction']}\n"
                  f"Risk Score  : {prediction['Risk_Score']}\n"
                  f"Latency     : {latency:.2f} ms\n"
                  )