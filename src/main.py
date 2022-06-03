from fastapi import Response, FastAPI, status
from converter import YamlConverter
from model import ConfigData
from server_log import write_log


'''
A log file can be found at ./logs/app.log
'''

app = FastAPI()


@app.get('/')
async def home():
    return {"status": "ON"}


@app.post('/convert')
async def convert_drone2woodpecker(request_data: ConfigData, response: Response):
    t = request_data
    # if the configs is empty
    if not request_data.configs:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": [{"msg": "field is empty", }]}

    response_data = request_data

    for config in response_data.configs:
        # if the configs is not empty, but the data or name
        if not config.data or not config.name:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": [{"msg": "`name` or `data` is empty", }]}

        config.data = YamlConverter.drone2woodpecker(config.data)

    response_data = {"configs": response_data.configs}

    # according to woodpecker's docs, returned HTTP status code is 204 if there is
    # nothing change, and tell the system to use current config. Or else, return nomal.
    # if temp == request_data.configs:
    #     response.status_code = status.HTTP_204_NO_CONTENT
    
    return response_data
