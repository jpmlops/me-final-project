import cv2
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pydantic import BaseModel
import shutil
from typing import List

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

# Directory to save uploaded files
UPLOAD_DIRECTORY = "./uploads"
FRAMES_DIRECTORY = "./frames"


if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

if not os.path.exists(FRAMES_DIRECTORY):
    os.makedirs(FRAMES_DIRECTORY)
    
app.mount("/frames", StaticFiles(directory="frames"), name="frames")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class FileResponse(BaseModel):
    filename: str
    
@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}

@app.post("/process-video", response_model=FileResponse)
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during file upload.")


@app.post("/extract_frames")
async def extract_frames(file: UploadFile = File(...), interval: int = Form(...)):
    try:
        # Save the uploaded video file
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the video to extract frames
        extract_frames_from_video(file_location, interval)
        
        return {"message": "Frames have been extracted and saved to the frames directory."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during video processing: {str(e)}")

def extract_frames_from_video(video_path: str, interval:int):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise HTTPException(status_code=400, detail="Could not open video file.")
    
    frame_count = 0
    success, frame = cap.read()
    while success:
        if frame_count % interval == 0:
            frame_filename = os.path.join(FRAMES_DIRECTORY, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_filename, frame)
            print(frame_count)
        frame_count += 1
        success, frame = cap.read()

    cap.release()

@app.get("/video-frames")
async def list_frames():
    if not os.path.exists(FRAMES_DIRECTORY):
        raise HTTPException(status_code=500, detail=f"An error occurred during frames list - Frames folder doesnt exist")
    
    frames = [f for f in os.listdir(FRAMES_DIRECTORY) if os.path.isfile(os.path.join(FRAMES_DIRECTORY, f))]
    return {"frames": frames}

@app.get("/video-frames-details/{frame_name}")
async def get_frame(frame_name: str):
    frame_path = os.path.join(FRAMES_DIRECTORY, frame_name)
    if os.path.exists(frame_path):
        return FileResponse(frame_path)
    else:
        raise HTTPException(status_code=404, detail="Frame not found.")
    

@app.get("/todo", tags=["todos"])
async def get_todos() -> dict:
    return { "data": todos }

@app.post("/todo", tags=["todos"])
async def add_todo(todo: dict) -> dict:
    todo.append(todo)
    return {
        "data": { "Todo added." }
    }
    
@app.put("/todo/{id}", tags=["todos"])
async def update_todo(id: int, body: dict) -> dict:
    for todo in todo:
        if int(todo["id"]) == id:
            todo["item"] = body["item"]
            return {
                "data": f"Todo with id {id} has been updated."
            }

    return {
        "data": f"Todo with id {id} not found."
    }
    
@app.delete("/todo/{id}", tags=["todos"])
async def delete_todo(id: int) -> dict:
    for todo in todos:
        if int(todo["id"]) == id:
            todos.remove(todo)
            return {
                "data": f"Todo with id {id} has been removed."
            }

    return {
        "data": f"Todo with id {id} not found."
    }