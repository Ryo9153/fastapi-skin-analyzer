
import tensorflow as tf
import tf2onnx

model = tf.keras.models.load_model("skin_diagnosis_model.h5")
spec = (tf.TensorSpec((None, 224, 224, 3), tf.float32, name="input"),)

output_path = "model/skin_diagnosis_model.onnx"
model_proto, _ =tf2onnx.convert.from_keras(
   model,
   input_signature=spec,
   output_path=output_path
)

print("変換完了!skin_diagnosis_model.onnx を保存しました")
