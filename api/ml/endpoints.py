"""
Endpoints ML-Ready
"""

from fastapi import APIRouter, Depends
from typing import List, Dict
from api.database import db
from api.auth.jwt_handler import get_current_user

router = APIRouter(prefix="/api/v1/ml", tags=["Machine Learning"])

@router.get("/features", dependencies=[Depends(get_current_user)])
async def get_ml_features():
    """Retorna features prontas para ML"""
    if not db.is_loaded():
        return {"error": "Dados não carregados"}
    
    features = {
        "numeric_features": ["price", "rating"],
        "categorical_features": ["category", "availability"],
        "text_features": ["title"],
        "total_samples": db.get_total_count(),
        "feature_statistics": {
            "price": {"min": float(db.df["price"].min()), "max": float(db.df["price"].max()), "mean": float(db.df["price"].mean())},
            "rating": {"min": int(db.df["rating"].min()), "max": int(db.df["rating"].max()), "mean": float(db.df["rating"].mean())}
        }
    }
    return features

@router.get("/training-data", dependencies=[Depends(get_current_user)])
async def get_training_data(limit: int = 100):
    """Retorna dados de treinamento"""
    if not db.is_loaded():
        return {"error": "Dados não carregados"}
    
    data = db.df.head(limit)[["title", "price", "rating", "category", "availability"]].to_dict("records")
    return {"total": len(data), "data": data}

@router.post("/predictions", dependencies=[Depends(get_current_user)])
async def make_predictions(features: Dict):
    """Endpoint para predições (mock)"""
    return {
        "prediction": "mock_prediction",
        "confidence": 0.85,
        "model_version": "1.0.0",
        "features_used": list(features.keys())
    }
