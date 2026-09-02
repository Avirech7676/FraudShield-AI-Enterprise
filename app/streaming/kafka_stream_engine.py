"""
Kafka-based Stream Engine for FraudShield AI Enterprise
Orchestrates the flow of transactions through Kafka topics
"""
import time
import threading
import logging
from typing import Optional

from app.streaming.kafka_producer import KafkaStreamProducer
from app.streaming.kafka_consumer import KafkaStreamConsumer
from app.streaming.metrics import StreamingMetrics

logger = logging.getLogger(__name__)

class KafkaStreamEngine:
    """
    Kafka-based stream engine that replaces the simple queue-based implementation
    Provides high-throughput, fault-tolerant transaction processing
    """

    def __init__(self):
        self.producer = KafkaStreamProducer()
        self.consumer = KafkaStreamConsumer()
        self.metrics = StreamingMetrics()
        self.running = False
        self.producer_thread: Optional[threading.Thread] = None
        self.consumer_thread: Optional[threading.Thread] = None

        logger.info("KafkaStreamEngine initialized")

    def start_producer(self, rate_per_second: float = 10.0):
        """
        Start the transaction producer thread

        Args:
            rate_per_second: Target rate of transactions per second
        """
        def produce_loop():
            delay = 1.0 / rate_per_second if rate_per_second > 0 else 0.1
            while self.running:
                try:
                    start_time = time.time()
                    self.producer.produce_transaction()
                    self.metrics.update()

                    # Maintain rate
                    elapsed = time.time() - start_time
                    sleep_time = max(0, delay - elapsed)
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                except Exception as e:
                    logger.error(f"Error in producer loop: {e}")
                    time.sleep(1)  # Brief pause before retry

        self.producer_thread = threading.Thread(target=produce_loop, daemon=True)
        self.producer_thread.start()
        logger.info(f"Started producer thread at {rate_per_second} tx/sec")

    def start_consumer(self):
        """Start the transaction consumer thread"""
        def consume_loop():
            while self.running:
                try:
                    result = self.consumer.consume_transaction()
                    if result is None:
                        # No message available, brief pause
                        time.sleep(0.1)
                except Exception as e:
                    logger.error(f"Error in consumer loop: {e}")
                    time.sleep(1)  # Brief pause before retry

        self.consumer_thread = threading.Thread(target=consume_loop, daemon=True)
        self.consumer_thread.start()
        logger.info("Started consumer thread")

    def start(self, production_rate: float = 10.0):
        """
        Start the stream processing engine

        Args:
            production_rate: Target transactions per second to generate
        """
        if self.running:
            logger.warning("Stream engine is already running")
            return

        self.running = True
        self.start_producer(production_rate)
        self.start_consumer()
        logger.info("KafkaStreamEngine started")

    def stop(self):
        """Stop the stream processing engine"""
        if not self.running:
            logger.warning("Stream engine is not running")
            return

        self.running = False

        # Wait for threads to finish (with timeout)
        if self.producer_thread and self.producer_thread.is_alive():
            self.producer_thread.join(timeout=5.0)

        if self.consumer_thread and self.consumer_thread.is_alive():
            self.consumer_thread.join(timeout=5.0)

        # Clean up resources
        self.producer.close()
        self.consumer.close()

        logger.info("KafkaStreamEngine stopped")

    def get_metrics(self) -> dict:
        """Get current processing metrics"""
        return {
            "throughput_tps": self.metrics.throughput(),
            "total_processed": getattr(self.metrics, 'transactions', 0),
            "running": self.running,
            "producer_alive": self.producer_thread.is_alive() if self.producer_thread else False,
            "consumer_alive": self.consumer_thread.is_alive() if self.consumer_thread else False
        }

    def health_check(self) -> dict:
        """Perform health check on streaming components"""
        try:
            # Test producer
            test_transaction = self.producer.producer.send(
                self.producer.topic,
                key="health-check",
                value={"test": True, "timestamp": time.time()}
            ).get(timeout=5)

            return {
                "status": "healthy",
                "components": {
                    "producer": "connected",
                    "consumer": "connected",
                    "kafka": "accessible"
                }
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "components": {
                    "producer": "unknown",
                    "consumer": "unknown",
                    "kafka": "unreachable"
                }
            }