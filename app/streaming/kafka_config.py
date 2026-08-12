"""
Kubernetes streaming configuration for FraudShield AI Enterprise
"""
import os
from typing import Dict, Any

# Kafka Configuration
KAFKA_CONFIG = {
    'bootstrap_servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
    'client_id': 'fraudshield-producer',
    'acks': 'all',  # Wait for all replicas to acknowledge
    'retries': 3,
    'retry_backoff_ms': 100,
    'request_timeout_ms': 30000,
}

# Consumer Configuration
KAFKA_CONSUMER_CONFIG = {
    'bootstrap_servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
    'group_id': 'fraudshield-consumer-group',
    'auto_offset_reset': 'earliest',  # Start from beginning if no offset
    'enable_auto_commit': True,
    'auto_commit_interval_ms': 1000,
    'session_timeout_ms': 30000,
    'heartbeat_interval_ms': 3000,
}

# Topics
KAFKA_TOPICS = {
    'TRANSACTIONS': 'financial-transactions',
    'PREDICTIONS': 'fraud-predictions',
    'ALERTS': 'fraud-alerts',
    'AUDIT_LOGS': 'audit-logs'
}

# Schema Registry (if using Avro/JSON Schema)
SCHEMA_REGISTRY_URL = os.getenv('SCHEMA_REGISTRY_URL', 'http://localhost:8081')

def get_kafka_producer_config() -> Dict[str, Any]:
    """Get Kafka producer configuration"""
    return KAFKA_CONFIG.copy()

def get_kafka_consumer_config() -> Dict[str, Any]:
    """Get Kafka consumer configuration"""
    return KAFKA_CONSUMER_CONFIG.copy()

def get_kafka_topic(topic_key: str) -> str:
    """Get Kafka topic name by key"""
    return KAFKA_TOPICS.get(topic_key, topic_key)