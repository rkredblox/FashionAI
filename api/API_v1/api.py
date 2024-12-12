from fastapi import APIRouter
from .Endpoint import Measurement
api_router = APIRouter()

api_router.include_router(Measurement.router, prefix='/demo', tags=['Measurement'])