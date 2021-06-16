## 필요한 라이브러리를 불러옵니다. 
import time
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import redis
from fastapi import FastAPI, File, UploadFile
from PIL import Image

import io
from starlette.responses import StreamingResponse

## pyspark를 불러옵니다.




#from pyspark import SparkContext
#sc = SparkContext(master="local", appName="first app")



image_pil = Image.open(path)
image = np.array(image_pil)

vector = plt.imshow(image)


app = FastAPI()

@app.post("/vector_image")
async def image_endpoint(*, vector):
    # Returns a cv2 image array from the document vector
    cv2img = my_function(vector)
    res, im_png = cv2.imencode(".png", cv2img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")


