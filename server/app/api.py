import cv2
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pydantic import BaseModel
import shutil
from keras.models import load_model
from pymongo.collection import Collection
from Db.mongo import db
from models.video import Video
from datetime import datetime
import imutils
from pymongo import MongoClient
import numpy as np

app = FastAPI()

# Create a global variable for the MongoDB client and database
client: MongoClient = None
db: Collection = None

@app.on_event("startup")
def db_event():
    global client, db
    print("startup has begun!!")
    client = MongoClient("mongodb://localhost:27017/")
    db = client.me_video
    
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
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"video_{timestamp}.mp4"
        file_location = os.path.join(UPLOAD_DIRECTORY, new_filename)
        
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"filename": new_filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during file upload.")

@app.get("/find-abnormal-case/{video_file}")
async def find_abnormal_case(video_file: str):
    file_location = os.path.join(UPLOAD_DIRECTORY, video_file)
    print("video file path: ", file_location)
    model=load_model("saved_model.keras")
    flag=0
    cap = cv2.VideoCapture(file_location)
    print(cap.isOpened())
    while cap.isOpened():
        imagedump=[]
        ret,frame=cap.read()

        for i in range(10):
            ret,frame=cap.read()
            
            if not hasattr(frame,'shape'):
                flag=1
                break
            
            image = imutils.resize(frame,width=640,height=360)

            frame=cv2.resize(frame, (640,360), interpolation = cv2.INTER_AREA)
            gray=0.2989*frame[:,:,0]+0.5870*frame[:,:,1]+0.1140*frame[:,:,2]
            gray=(gray-gray.mean())/gray.std()
            gray=np.clip(gray,0,1)
            imagedump.append(gray)
        
        if flag==1:
            break

        imagedump=np.array(imagedump)
        #print(imagedump)

        imagedump.resize(227,227,10)
        imagedump=np.expand_dims(imagedump,axis=0)
        imagedump=np.expand_dims(imagedump,axis=4)
        
        #print(imagedump)

        output = model.predict(imagedump)

        loss = mean_squared_loss(imagedump,output)
        
        print(loss)

        if frame.any()==None:
            print("none")

        if cv2.waitKey(10) & 0xFF==ord('q'):
            break
        if (loss>0.00066 and loss<0.000675) or (loss>0.00069 and loss<0.00071):                
            print('Abnormal Event Detected')
            cv2.putText(image,"Abnormal Event",(100,100),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),4,cv2.LINE_AA)

        # cv2.imshow("video",image)

    cap.release()
    cv2.destroyAllWindows()
    
@app.post("/extract_frames")
async def extract_frames(file: UploadFile = File(...), interval: int = Form(...)):
    try:
        # Save the uploaded video file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"video_{timestamp}.mp4"
        
        file_location = os.path.join(UPLOAD_DIRECTORY, new_filename)
        
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            db = client.me_video
            collection = db.video
            item = collection.insert_one({"name": new_filename, "slug": f"video_{timestamp}", "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()})
            # item = collection.insert_one({"name": new_filename, "slug": "video_{timestamp}", "created_at": datetime.now, "updated_at": datetime.now})
            print("item: ", item)
        
        # Process the video to extract frames
        extract_frames_from_video(file_location, interval, f"video_{timestamp}")
        
        return {"message": "Frames have been extracted and saved to the frames directory."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during video processing: {str(e)}")

def extract_frames_from_video(video_path: str, interval:int, path: str):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise HTTPException(status_code=400, detail="Could not open video file.")
    
    frame_count = 0
    success, frame = cap.read()    
    nested_dir = os.path.join(FRAMES_DIRECTORY, path)
    os.makedirs(nested_dir, exist_ok=True)
    while success:
        if frame_count % interval == 0:
            frame_filename = os.path.join(nested_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_filename, frame)
            print(frame_count)
        frame_count += 1
        success, frame = cap.read()

    cap.release()

@app.get("/video-frames")
async def list_frames():
    # if not os.path.exists(FRAMES_DIRECTORY):
    #     raise HTTPException(status_code=500, detail=f"An error occurred during frames list - Frames folder doesnt exist")
    db = client.me_video
    collection = db.video
    # frames = [f for f in os.listdir(FRAMES_DIRECTORY) if os.path.isfile(os.path.join(FRAMES_DIRECTORY, f))]
    frames = list(collection.find())
    for item in frames:
        item["_id"] = str(item["_id"])
        
    return {"frames": frames}

@app.get("/frames-list/{folder}")
async def list_frames(folder:str):
    frame_path = os.path.join(FRAMES_DIRECTORY, folder)
    if not os.path.exists(frame_path):
        raise HTTPException(status_code=500, detail=f"An error occurred during frames list - Frames folder doesnt exist")

    frames = [f for f in os.listdir(frame_path) if os.path.isfile(os.path.join(frame_path, f))]        
    return {"frames": frames}

@app.get("/video-frames-details/{frame_name}")
async def get_frame(frame_name: str):
    frame_path = os.path.join(FRAMES_DIRECTORY, frame_name)
    if os.path.exists(frame_path):
        return FileResponse(frame_path)
    else:
        raise HTTPException(status_code=404, detail="Frame not found.")    

def mean_squared_loss(x1,x2):
    difference=x1-x2
    a,b,c,d,e=difference.shape
    n_samples=a*b*c*d*e
    sq_difference=difference**2
    Sum=sq_difference.sum()
    distance=np.sqrt(Sum)
    mean_distance=distance/n_samples

    return mean_distance