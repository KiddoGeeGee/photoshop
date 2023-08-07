import cv2
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

import utils.roop as roop
from utils.utils import convert_to_b64_list, decode_base64_to_image
from CodeFormer.app import inference_app
from search import fs, search

face_swapper = roop.getFaceSwapModel("models/roop/inswapper_128.onnx")
face_enhancer = None


class Item(BaseModel):
    source_img: str
    target_img: str 

app  = FastAPI()
@app.post("/v1/main")
async def main(item: Item):
    source_img = item.source_img
    target_img = item.target_img
    source_img = decode_base64_to_image(source_img)
    target_img = decode_base64_to_image(target_img)
    roop_res = roop.main(source_img,target_img, face_swapper)
    scale = min(roop_res.size)//512
    roop_res = roop_res.resize((roop_res.size[0]//scale, roop_res.size[1]//scale))
    roop_res = cv2.cvtColor(np.array(roop_res),cv2.COLOR_RGB2BGR)
    res = inference_app(roop_res,
                        background_enhance=True,
                        face_upsample=True,
                        upscale=1,
                        codeformer_fidelity=1,
                        )
    res = convert_to_b64_list([res])[0]
    return res

@app.get("/v1/search")
async def search_(query):
    res = search(query)
    return res

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0")
