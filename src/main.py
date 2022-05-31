from fastapi import Response, FastAPI, status
from converter import YamlConverter
from model import ConfigData

app = FastAPI()


@app.get('/')
async def home():
    return {"status": "ON"}


@app.post('/convert')
async def convert_drone2woodpecker(request_data: ConfigData, response: Response):

    # if the configs is empty
    if not request_data.configs:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": [{"msg": "field is empty", }]}

    for config in request_data.configs:
        # if the configs is not empty, but the data or name
        if not config.data or not config.name:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": [{"msg": "`name` or `data` is empty", }]}

        config.data = YamlConverter.drone2woodpecker(config.data)

    # according to woodpecker's docs, returned HTTP status code is 204
    # response.status_code = status.HTTP_204_NO_CONTENT
    return {"pipelines": request_data.configs}
