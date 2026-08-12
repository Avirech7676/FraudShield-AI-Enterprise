"""
Kafka Producer for FraudShield AI Enterprise
Handles publishing transactions to Kafka topics
"""

import json
import logging
import uuid
from typing import Dict, Any
from datetime import datetime

try:
    from kafka import KafkaProducer
    from kafka.errors import KafkaError
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False
    logging.warning("Kafka not available. Install kafka-python for Kafka support.")

from app.streaming.kafka_config import (
    get_kafka_producer_config,
    get_kafka_topic,
)
from app.streaming.transaction_generator import TransactionGenerator

logger = logging.getLogger(__name__)


class KafkaStreamProducer:
    """Kafka producer for streaming financial transactions"""

    def __init__(self):
        if not KAFKA_AVAILABLE:
            raise ImportError(
                "kafka-python is required for KafkaStreamProducer"
            )

        self.producer = KafkaProducer(
            **get_kafka_producer_config(),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda k: k.encode("utf-8") if k else None,
        )

        self.transaction_generator = TransactionGenerator()
        self.topic = get_kafka_topic("TRANSACTIONS")

        logger.info(
            f"KafkaStreamProducer initialized for topic: {self.topic}"
        )

    def produce_transaction(self) -> Dict[str, Any]:
        """
        Generate and send a transaction to Kafka.

        Returns:
            Dict containing the transaction that was sent.
        """
        try:
            # Generate transaction
            transaction = self.transaction_generator.generate()

            # Add timestamp if not present
            if "timestamp" not in transaction:
                transaction["timestamp"] = datetime.utcnow().isoformat()

            # Use transaction_id as key for partitioning
            key = transaction.get("transaction_id", str(uuid.uuid4()))

            # Send to Kafka
            future = self.producer.send(
                topic=self.topic,
                key=key,
                value=transaction,
            )

            # Wait for send to complete (optional, for demo)
            # In production, you may want to handle this asynchronously
            record_metadata = future.get(timeout=10)

            logger.debug(
                f"Sent transaction {transaction['transaction_id']} "
                f"to topic {record_metadata.topic} "
                f"partition {record_metadata.partition} "
                f"offset {record_metadata.offset}"
            )

            return transaction

        except Exception as e:
            logger.error(f"Failed to produce transaction: {e}")
            raise

    def produce(self) -> Dict[str, Any]:
        """
        Compatibility wrapper for tests.

        This method delegates to produce_transaction() so that
        existing tests expecting a `produce()` method continue to work.

        Returns:
            Dict containing the transaction that was sent.
        """
        return self.produce_transaction()

    def close(self):
        """Close the producer connection."""
        if hasattr(self, "producer"):
            self.producer.close()
            logger.info("Kafka producer closed")