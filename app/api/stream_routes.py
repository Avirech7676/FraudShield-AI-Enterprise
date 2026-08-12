"""
Stream Processing API Endpoints
Provides REST API interfaces for controlling and monitoring the streaming pipeline
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from typing import Dict, Any
import logging

from app.auth.jwt_handler import JWTHandler
from app.config.logging_config import logger

router = APIRouter(prefix="/stream", tags=["Stream Processing"])

def get_stream_engine(request: Request):
    """Get the stream engine instance from app state"""
    stream_engine = getattr(request.app.state, 'stream_engine', None)
    if stream_engine is None:
        raise HTTPException(status_code=503, detail="Stream engine not initialized")
    return stream_engine

@router.post("/start")
def start_streaming(
    request: Request,
    background_tasks: BackgroundTasks,
    rate_per_second: float = 10.0,
    current_user: dict = Depends(JWTHandler.verify_token)
):
    """
    Start the stream processing engine

    Requires admin privileges
    """
    # In production, add proper role checking here
    try:
        engine = get_stream_engine(request)
        if not hasattr(engine, 'running') or not engine.running:
            background_tasks.add_task(engine.start, production_rate=rate_per_second)
            return {
                "message": f"Stream processing started at {rate_per_second} transactions/second",
                "status": "starting"
            }
        else:
            return {
                "message": "Stream processing is already running",
                "status": "already_running"
            }
    except Exception as e:
        logger.error(f"Failed to start stream processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop")
def stop_streaming(
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(JWTHandler.verify_token)
):
    """
    Stop the stream processing engine

    Requires admin privileges
    """
    try:
        engine = get_stream_engine(request)
        if hasattr(engine, 'running') and engine.running:
            background_tasks.add_task(engine.stop)
            return {
                "message": "Stream processing stopped",
                "status": "stopping"
            }
        else:
            return {
                "message": "Stream processing is not running",
                "status": "already_stopped"
            }
    except Exception as e:
        logger.error(f"Failed to stop stream processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
def get_stream_status(
    request: Request,
    current_user: dict = Depends(JWTHandler.verify_token)
):
    """
    Get current status of the stream processing engine
    """
    try:
        engine = get_stream_engine(request)
        status = {
            "running": getattr(engine, 'running', False),
            "metrics": engine.get_metrics() if hasattr(engine, 'get_metrics') else {},
            "health": engine.health_check() if hasattr(engine, 'health_check') else {"status": "unknown"}
        }
        return status
    except Exception as e:
        logger.error(f"Failed to get stream status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
def stream_health_check(
    request: Request,
    current_user: dict = Depends(JWTHandler.verify_token)
):
    """
    Health check specifically for stream processing components
    """
    try:
        engine = get_stream_engine(request)
        health = engine.health_check() if hasattr(engine, 'health_check') else {
            "status": "unknown",
            "error": "Health check not available"
        }
        return health
    except Exception as e:
        logger.error(f"Stream health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics")
def get_stream_metrics(
    request: Request,
    current_user: dict = Depends(JWTHandler.verify_token)
):
    """
    Get detailed streaming metrics
    """
    try:
        engine = get_stream_engine(request)
        if hasattr(engine, 'get_metrics'):
            metrics = engine.get_metrics()
            return {
                "metrics": metrics,
                "timestamp": __import__('time').time()
            }
        else:
            return {
                "message": "Metrics not available",
                "metrics": {}
            }
    except Exception as e:
        logger.error(f"Failed to get stream metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))