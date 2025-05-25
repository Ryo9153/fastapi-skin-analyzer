import onnxruntime as ort
from fastapi import FastAPI,File,UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import io

app = FastAPI()

session = ort.InferenceSession("skin_model_clean.onnx")

@app.get("/")
def read_root():
    return {"message": "Hello from Render!"}

@app.post("/analyze")
async def analyze_skin(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image = image.resize((224, 224))
        img_array = np.array(image).astype(np.float32) / 255.0
        img_array = np.transpose(img_array, (2, 0, 1))
        img_array = np.expand_dims(img_array, axis=0)
        inputs = {session.get_inputs()[0].name: img_array}
        outputs = session.run(None, inputs)
        result = int(np.argmax(outputs[0]))
        return JSONResponse(content={"result": result})
        
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
