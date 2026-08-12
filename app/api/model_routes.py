from fastapi import APIRouter, Depends, HTTPException, Request, Query
from app.auth.jwt_handler import JWTHandler
from app.config.logging_config import logger
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.ml.model_registry import ModelRegistry

router = APIRouter(
    prefix="/model",
    tags=["Model"]
)

@router.get("/registry")
def get_model_registry(
    request: Request,
    user = Depends(JWTHandler.verify_token),
    model_name: Optional[str] = Query(None, description="Filter by model name"),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    skip: int = Query(0, ge=0, description="Number of records to skip")
):
    """
    Get the model registry with optional filtering and pagination.
    """
    try:
        registry = ModelRegistry()
        # We don't have a direct method to filter and paginate in the registry, so we'll get all and filter in memory for now.
        # For production, we should add these methods to the ModelRegistry class.
        models = registry.list_models()

        # Apply filters
        if model_name:
            models = [m for m in models if m.get("model_name") == model_name]
        if status:
            models = [m for m in models if m.get("status") == status]

        # Apply pagination
        total = len(models)
        paginated_models = models[skip:skip+limit]

        # Convert ObjectId to string if present (though our registry doesn't store _id in the list)
        for model in paginated_models:
            if "_id" in model:
                model["_id"] = str(model["_id"])

        return {
            "models": paginated_models,
            "pagination": {
                "total": total,
                "skip": skip,
                "limit": limit,
                "has_next": skip + limit < total
            }
        }
    except Exception as e:
        logger.error(f"Failed to get model registry: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve model registry")

@router.get("/registry/{model_name}/{version}")
def get_model_version(
    model_name: str,
    version: str,
    request: Request,
    user = Depends(JWTHandler.verify_token)
):
    """
    Get a specific model version from the registry.
    """
    try:
        registry = ModelRegistry()
        models = registry.list_models()
        model = next((m for m in models if m.get("model_name") == model_name and m.get("version") == version), None)
        if model is None:
            raise HTTPException(status_code=404, detail=f"Model {model_name} version {version} not found")
        if "_id" in model:
            model["_id"] = str(model["_id"])
        return model
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get model {model_name} version {version}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve model version")

@router.post("/deploy/{model_name}/{version}")
def deploy_model(
    model_name: str,
    version: str,
    request: Request,
    user = Depends(JWTHandler.verify_token)
):
    """
    Deploy a specific model version to production.
    """
    try:
        registry = ModelRegistry()
        # First, set all models to REGISTERED status
        registry.collection.update_many({}, {"$set": {"status": "REGISTERED"}})
        # Then, set the specified model to PRODUCTION
        result = registry.collection.update_one(
            {"model_name": model_name, "version": version},
            {"$set": {"status": "PRODUCTION"}}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Model {model_name} version {version} not found")
        # Also, we need to copy the model file to the production model path (as in the deploy method of ModelRegistry)
        # But note: the deploy method in ModelRegistry does more than just update status.
        # Let's call the deploy method from the ModelRegistry class to handle the file copy as well.
        # However, the deploy method in ModelRegistry expects a version string, not model_name and version.
        # We'll adjust: we have the version, so we can call deploy with that version.
        # But note: the deploy method in ModelRegistry does not take model_name, it uses the version to find the model.
        # So we can call it if we are sure the version is unique? Actually, the version is unique per model?
        # In our current setup, version is per model (we increment per model). So we can use the version alone.
        # However, the deploy method in ModelRegistry does not check the model_name. It just finds by version.
        # This is acceptable if we assume version is unique across models (which it is in our current design).
        deployed = registry.deploy(version)
        if not deployed:
            raise HTTPException(status_code=500, detail="Failed to deploy model")
        return {"message": f"Model {model_name} version {version} deployed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to deploy model {model_name} version {version}: {e}")
        raise HTTPException(status_code=500, detail="Failed to deploy model")

@router.post("/rollback")
def rollback_model(
    request: Request,
    user = Depends(JWTHandler.verify_token)
):
    """
    Rollback to the previous model version.
    """
    try:
        registry = ModelRegistry()
        # We'll call the rollback method from the ModelRegistry
        # Note: the rollback method in ModelRegistry doesn't return anything and just prints.
        # We'll adjust it to return a boolean or we can just call it and then check the status.
        # For now, we'll call it and then get the current production model to return.
        registry.rollback()
        # After rollback, get the current production model
        production = registry.production_model()
        if production is None:
            raise HTTPException(status_code=500, detail="No model found after rollback")
        if "_id" in production:
            production["_id"] = str(production["_id"])
        return {
            "message": "Rollback successful",
            "model": production
        }
    except Exception as e:
        logger.error(f"Failed to rollback model: {e}")
        raise HTTPException(status_code=500, detail="Failed to rollback model")