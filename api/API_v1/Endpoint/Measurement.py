from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi import APIRouter

router  = APIRouter()

size_chart = {
    "measurements": [
        {"size": "XS", "chest": list(range(74, 85)), "waist": list(range(64, 70))},
        {"size": "S", "chest": list(range(86, 95)), "waist": list(range(71, 80))},
        {"size": "M", "chest": list(range(96, 105)), "waist": list(range(81, 90))},
        {"size": "L", "chest": list(range(106, 115)), "waist": list(range(91, 100))},
        {"size": "XL", "chest": list(range(117, 125)), "waist": list(range(103, 108))},
        {"size": "2XL", "chest": list(range(127, 136)), "waist": list(range(115, 125))},
        {"size": "3XL", "chest": list(range(137, 146)), "waist": list(range(129, 143))},
        {"size": "4XL", "chest": list(range(147, 156)), "waist": list(range(145, 156))},
        {"size": "5XL", "chest": list(range(157, 166)), "waist": list(range(158, 169))},
    ]
}


class MeasurementSizeRequest(BaseModel):
    chest: int
    waist: int

class MeasurementSizeResponse(BaseModel):
    size: str

@router.post("/size_calculation/", response_model=MeasurementSizeResponse)
def size(request: MeasurementSizeRequest):
    chest_cm = request.chest
    waist_cm = request.waist
    print(chest_cm, waist_cm, "Input Measurements")

    for measurement in size_chart["measurements"]:
        if chest_cm in measurement["chest"] and waist_cm in measurement["waist"]:
            print("Matching size found")
            return MeasurementSizeResponse(size=measurement["size"])

    raise HTTPException(status_code=404, detail="Size not found")


