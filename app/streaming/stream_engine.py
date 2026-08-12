"""
Enhanced Stream Engine with Kafka Integration
Orchestrates the streaming pipeline using Kafka for production-grade message passing
"""
import time
import threading
import logging
from typing import Optional, Dict, Any

from app.streaming.kafka_producer import KafkaStreamProducer
from app.streaming.kafka_consumer import KafkaStreamConsumer
from app.streaming.metrics import StreamingMetrics
from app.streaming.kafka_config import get_kafka_topic

logger = logging.getLogger(__name__)

class StreamEngine:
    """
    Enhanced stream processing engine using Kafka for reliable message passing
    """

    def __init__(self):
        self.producer: Optional[KafkaStreamProducer] = None
        self.consumer: Optional[KafkaStreamConsumer] = None
        self.metrics = StreamingMetrics()
        self.running = False
        self.producer_thread: Optional[threading.Thread] = None
        self.consumer_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

        # Performance tracking
        self.messages_produced = 0
        self.messages_consumed = 0
        self.last_metrics_time = time.time()

        logger.info("StreamEngine initialized with Kafka support")

    def start(self, production_rate: float = 10.0):
        """
        Start the stream processing pipeline

        Args:
            production_rate: Target number of transactions per second to generate
        """
        if self.running:
            logger.warning("StreamEngine is already running")
            return

        try:
            logger.info(f"Starting StreamEngine with production rate: {production_rate}/sec")

            # Initialize Kafka components
            self.producer = KafkaStreamProducer()
            self.consumer = KafkaStreamConsumer()

            # Reset state
            self.running = True
            self._stop_event.clear()

            # Start producer thread
            self.producer_thread = threading.Thread(
                target=self._producer_loop,
                args=(production_rate,),
                name="StreamProducer",
                daemon=True
            )
            self.producer_thread.start()

            # Start consumer thread
            self.consumer_thread = threading.Thread(
                target=self._consumer_loop,
                name="StreamConsumer",
                daemon=True
            )
            self.consumer_thread.start()

            logger.info("StreamEngine started successfully")

        except Exception as e:
            logger.error(f"Failed to start StreamEngine: {e}")
            self.stop()
            raise

    def stop(self):
        """Stop the stream processing pipeline gracefully"""
        if not self.running:
            logger.warning("StreamEngine is not running")
            return

        logger.info("Stopping StreamEngine...")
        self.running = False
        self._stop_event.set()

        # Wait for threads to finish (with timeout)
        if self.producer_thread and self.producer_thread.is_alive():
            self.producer_thread.join(timeout=5.0)

        if self.consumer_thread and self.consumer_thread.is_alive():
            self.consumer_thread.join(timeout=5.0)

        # Close resources
        if self.producer:
            self.producer.close()
            self.producer = None

        if self.consumer:
            # Consumer close is handled internally
            self.consumer = None

        logger.info("StreamEngine stopped")

    def _producer_loop(self, target_rate: float):
        """
        Main loop for generating and sending transactions

        Args:
            target_rate: Target transactions per second
        """
        interval = 1.0 / max(target_rate, 0.1)  # Avoid division by zero
        logger.info(f"Producer loop started with {target_rate}/sec rate")

        while self.running and not self._stop_event.is_set():
            start_time = time.time()

            try:
                if self.producer:
                    transaction = self.producer.produce_transaction()
                    if transaction:
                        self.messages_produced += 1
                        self.metrics.transactions += 1

                # Sleep to maintain rate
                elapsed = time.time() - start_time
                sleep_time = max(0, interval - elapsed)
                time.sleep(sleep_time)

            except Exception as e:
                logger.error(f"Error in producer loop: {e}")
                time.sleep(1)  # Back off on error

        logger.info("Producer loop ended")

    def _consumer_loop(self):
        """Main loop for consuming and processing transactions"""
        logger.info("Consumer loop started")

        while self.running and not self._stop_event.is_set():
            try:
                if self.consumer:
                    result = self.consumer.consume_transaction()
                    if result:
                        self.messages_consumed += 1

                # Small sleep to prevent busy waiting
                time.sleep(0.01)

            except Exception as e:
                logger.error(f"Error in consumer loop: {e}")
                time.sleep(1)  # Back off on error

        logger.info("Consumer loop ended")

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current processing metrics

        Returns:
            Dictionary containing performance metrics
        """
        uptime = time.time() - getattr(self, '_start_time', time.time())

        return {
            "running": self.running,
            "uptime_seconds": round(uptime, 2),
            "messages_produced": self.messages_produced,
            "messages_consumed": self.messages_consumed,
            "production_rate": round(self.messages_produced / max(uptime, 1), 2),
            "consumption_rate": round(self.messages_consumed / max(uptime, 1), 2),
            "lag": self.messages_produced - self.messages_consumed,
            "kafka_metrics": self.metrics.throughput() if hasattr(self.metrics, 'throughput') else {},
            "buffer_health": "healthy" if abs(self.messages_produced - self.messages_consumed) < 1000 else "backed_up"
        }

    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on streaming components

        Returns:
            Dictionary containing health status
        """
        health = {
            "status": "healthy" if self.running else "stopped",
            "components": {
                "producer": "healthy" if self.producer else "not_initialized",
                "consumer": "healthy" if self.consumer else "not_initialized",
                "producer_thread": "alive" if self.producer_thread and self.producer_thread.is_alive() else "dead",
                "consumer_thread": "alive" if self.consumer_thread and self.consumer_thread.is_alive() else "dead"
            },
            "lag_messages": self.messages_produced - self.messages_consumed
        }

        # Determine overall health
        if not self.running:
            health["status"] = "stopped"
        elif self.producer is None or self.consumer is None:
            health["status"] = "unhealthy"
            health["reason"] = "Components not initialized"
        elif abs(self.messages_produced - self.messages_consumed) > 10000:
            health["status"] = "degraded"
            health["reason"] = "High lag detected"
        else:
            health["status"] = "healthy"

        return health

    def __del__(self):
        """Cleanup on destruction"""
        if self.running:
            self.stop()