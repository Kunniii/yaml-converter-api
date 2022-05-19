from urllib import response
from fastapi import Request, FastAPI

from converter import YamlConverter
from model import ConfigData, Config

import json

app = FastAPI()

@app.get('/')
async def home():
    return {"status": "ON"}

@app.post('/convert', status_code=200)
async def convert_drone2woodpecker(config_data: ConfigData):
    for config in config_data.config:
        config.data = YamlConverter.drone2woodpecker(config.data)
    return {"pipelines":config_data.config}