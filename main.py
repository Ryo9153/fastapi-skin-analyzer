
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
   #受け取った画像を保存
   with open(f"temp_{file.filename}","wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

   #仮の診断結果
   result={
           "毛穴":"目立ちにくい",
           "水分量":"やや少なめ",
           "シミ":"なし"
　　　　　　 }
   
   os.remove(f"temp_{file.filename}")
   return JSONResponse(content={"result":result})