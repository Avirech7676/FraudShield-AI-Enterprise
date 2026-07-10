from app.streaming.stream_engine import StreamEngine

def test_stream_single_iteration():
    """
    Test a single iteration of the streaming engine to verify components are connected.
    """
    engine = StreamEngine()
    
    # Run one single production and consumption step
    transaction = engine.producer.produce()
    assert transaction is not None
    assert "transaction_id" in transaction
    
    prediction = engine.consumer.consume(transaction)
    assert prediction is not None
    assert "Prediction" in prediction
    assert "Risk_Score" in prediction

if __name__ == "__main__":
    print("Starting Streaming Engine...")
    engine = StreamEngine()
    engine.start()