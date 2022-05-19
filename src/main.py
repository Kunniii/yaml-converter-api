from urllib import response
from fastapi import Request, FastAPI

from converter import YamlConverter
from model import PostData

import json

app = FastAPI()

@app.get('/')
async def home():
    return {"status": "ON"}

@app.post('/convert')
async def convert_drone2woodpecker(drone_data: PostData):
    try:
        woodpecker_yaml = YamlConverter.drone2woodpecker(drone_data.data)
        return {"status": "OK", "data": woodpecker_yaml}
    except:
        return {"status": "ERROR"}