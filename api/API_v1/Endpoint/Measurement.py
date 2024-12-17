from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import List, Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import shutil
import os
from typing import Optional
import cv2
from datetime import datetime


router  = APIRouter()

# Directory to store the uploaded images
IMAGE_DIR = "images"

# Ensure the directory exists
os.makedirs(IMAGE_DIR, exist_ok=True)

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


@router.post("/capture_image/", response_description="Upload an image")
async def upload_image(file: UploadFile = File(...)):
    """
    Capture and save the uploaded image file to the local directory.
    """
    try:
        file_location = os.path.join(IMAGE_DIR, file.filename)
        
        # Save the uploaded file
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return JSONResponse(content={"message": "Image uploaded successfully", "file_name": file.filename, "location": file_location})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")
    

@router.post("/capture_webcam_image/", response_description="Capture image using webcam")
async def capture_webcam_image():
    """
    Capture an image from the webcam and save it to the local directory.
    """
    try:
        # Initialize the webcam
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise HTTPException(status_code=500, detail="Could not open webcam.")

        # Capture a single frame
        ret, frame = cap.read()
        if not ret:
            raise HTTPException(status_code=500, detail="Failed to capture image from webcam.")

        # Generate a unique filename using timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"webcam_image_{timestamp}.jpg"
        file_path = os.path.join(IMAGE_DIR, file_name)

        # Save the image
        cv2.imwrite(file_path, frame)

        # Release the webcam
        cap.release()
        cv2.destroyAllWindows()

        return JSONResponse(content={"message": "Image captured successfully", "file_name": file_name, "location": file_path})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error capturing image: {str(e)}")




@router.put("/update_image/", response_description="Update an existing image")
async def update_image(existing_file_name: str, file: UploadFile = File(...)):
    """
    Update an existing image file in the local directory.
    """
    try:
        file_location = os.path.join(IMAGE_DIR, existing_file_name)
        
        # Check if the existing file exists
        if not os.path.exists(file_location):
            raise HTTPException(status_code=404, detail="File not found. Cannot update.")
        
        # Replace the existing file
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return JSONResponse(content={"message": "Image updated successfully", "file_name": existing_file_name})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update image: {str(e)}")
