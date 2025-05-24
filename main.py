import onnxruntime as ort
from fastapi import FastAPI,File,UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import io

app = FastAPI()

try:
    session = ort.InferenceSession("skin_model_clean.onnx")
    input_name = session.get_inputs()[0].name
except Exception as e:
    session = None
    input_name =None
    print("ONNXモデルの読み込みに失敗", e)

def preprocess(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).resize((224, 224))
    img_array = np.array(image).astype(np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # (1, 224, 224, 3)
    return img_array

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if session is None:
        return JSONResponse(content={"error": "ONNXモデルが読み込まれていません"}, status_code=500)

    try:
        contents = await file.read()
        input_data = preprocess(contents)
        output = session.run(None, {inputs_name: input_data})
        result = float(output[0][0][0])
        return {"result": result, "score": round(result, 2)}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
