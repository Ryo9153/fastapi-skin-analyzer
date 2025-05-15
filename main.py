
from fastapi import FastAPI,File,UploadFile
from fastapi.responses import JSONResponse
import shutil
import os


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Render!"}

@app.post("/analyze")
async def analyzer_skin(file:UploadFile=File(...)):
   with open(f"temp_{file.filename}","wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

   result={
           "pore":"not visible",
           "moisture":"slightly low",
           "spots":"none"
          }
   
   os.remove(f"temp_{file.filename}")
   return JSONResponse(content={"result":result})