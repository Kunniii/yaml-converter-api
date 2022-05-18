from urllib import response
from fastapi import Request, FastAPI
from converter import YamlConverter
import json

app = FastAPI()


@app.post('/drone2woodpecker')
async def convert_drone(data: Request):
    print(data.json().__doc__())
    # return data