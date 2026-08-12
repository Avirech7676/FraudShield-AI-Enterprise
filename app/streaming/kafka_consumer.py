"""
Kafka Consumer for FraudShield AI Enterprise
Handles consuming transactions from Kafka and processing them
"""
import json
import logging
from typing import Dict, Any
import pandas as pd

try:
    from kafka import KafkaConsumer
    from kafka.errors import KafkaError
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False
    logging.warning("Kafka not available. Install kafka-python for Kafka support.")

from app.inference.predictor import EnterpriseFraudPredictor
from app.database.connection import LazyCollection, MongoDBConnection
from app.database.repository import FraudRepository
from app.streaming.kafka_config import get_kafka_consumer_config, get_kafka_topic
from app.streaming.metrics import StreamingMetrics

logger = logging.getLogger(__name__)

class KafkaStreamConsumer:
    """Kafka consumer for processing financial transactions"""

    def __init__(self):
        if not KAFKA_AVAILABLE:
            raise ImportError("kafka-python is required for KafkaStreamConsumer")

        self.consumer = KafkaConsumer(
            get_kafka_topic('TRANSACTIONS'),
            get_kafka_topic('FEEDBACK'),  # For future feedback loop
            **get_kafka_consumer_config(),
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None
        )

        # Initialize services lazily — repository resolved on first use
        self.predictor = EnterpriseFraudPredictor()
        self._db = None
        self.metrics = StreamingMetrics()

        logger.info("KafkaStreamConsumer initialized")

    @property
    def repository(self) -> FraudRepository:
        """Lazily initialise FraudRepository on first access."""
        if self._db is None:
            self._db = MongoDBConnection().connect_sync()
        return FraudRepository(self._db)


    def consume_transaction(self) -> Dict[str, Any]:
        """
        Consume and process a single transaction from Kafka

        Returns:
            Dict containing the prediction result
        """
        try:
            # Poll for messages
            message_batch = self.consumer.poll(timeout_ms=1000, max_records=1)

            if not message_batch:
                return None

            # Process the first message
            for topic_partition, messages in message_batch.items():
                for message in messages:
                    transaction = message.value
                    transaction_id = transaction.get('transaction_id')

                    if not transaction_id:
                        logger.warning("Received transaction without transaction_id")
                        continue

                    logger.debug(f"Processing transaction {transaction_id}")

                    # Process the transaction
                    prediction_result = self._process_transaction(transaction)

                    # Commit offset
                    self.consumer.commit()

                    return prediction_result

            return None

        except Exception as e:
            logger.error(f"Error consuming transaction: {e}")
            raise

    def _process_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single transaction through the fraud detection pipeline

        Args:
            transaction: Transaction data dictionary

        Returns:
            Dictionary containing prediction results
        """
        try:
            # Convert transaction to DataFrame for prediction
            df = pd.DataFrame([transaction])

            # Get prediction from the model
            prediction = self.predictor.predict_single(df)

            # Prepare prediction record for storage
            prediction_record = {
                "transaction_id": transaction["transaction_id"],
                "prediction": prediction["Prediction"],
                "fraud_probability": prediction["Fraud_Probability"],
                "risk_score": prediction["Risk_Score"],
                "risk_tier": prediction["Risk_Tier"],
                "timestamp": transaction.get("timestamp")
            }

            # Save transaction and prediction to database
            self.repository.save_transaction(transaction)
            self.repository.save_prediction(prediction_record)

            # Create alert if risk score is high
            if prediction["Risk_Score"] >= 80:
                alert_record = {
                    "transaction_id": transaction["transaction_id"],
                    "priority": "P1" if prediction["Risk_Score"] >= 90 else "P2",
                    "status": "OPEN",
                    "timestamp": transaction.get("timestamp"),
                    "risk_score": prediction["Risk_Score"]
                }
                self.repository.save_alert(alert_record)
                self._send_alert_notification(alert_record)

            # Log audit trail
            self.repository.save_audit_log_sync({
                "transaction_id": transaction["transaction_id"],
                "action": "Streaming Prediction",
                "timestamp": transaction.get("timestamp"),
                "details": f"Processed via Kafka consumer with score {prediction['Risk_Score']}"
            })

            # Update metrics
            self.metrics.update()

            # Send prediction to Kafka topic for downstream processing (optional)
            # self._send_prediction_to_kafka(transaction["transaction_id"], prediction)

            logger.info(
                f"Processed transaction {transaction['transaction_id']}: "
                f"Prediction={prediction['Prediction']}, "
                f"Score={prediction['Risk_Score']}, "
                f"Tier={prediction['Risk_Tier']}"
            )

            return prediction

        except Exception as e:
            logger.error(f"Error processing transaction {transaction.get('transaction_id')}: {e}")
            raise

    def _send_alert_notification(self, alert: Dict[str, Any]):
        """Send alert notification (placeholder for email/SMS/webhook)"""
        # In production, this would integrate with notification services
        logger.warning(
            f"FRAUD ALERT: Transaction {alert['transaction_id']} "
            f"has high risk score {alert['risk_score']}"
        )

    def close(self):
        """Close the consumer connection"""
        if hasattr(self, 'consumer'):
            self.consumer.close()
            logger.info("Kafka consumer closed")

    def poll_messages(self, timeout_ms: int = 1000):
        """
        Generator that yields messages as they arrive
        Useful for streaming applications
        """
        try:
            for message in self.consumer:
                yield message.value
        except Exception as e:
            logger.error(f"Error in message polling: {e}")
            raise