from fastapi import FastAPI
from converter import YamlConverter

app = FastAPI()


@app.get('/drone2woodpecker')
def convert_drone():
    data = YamlConverter.drone2woodpecker("pipeline:\n  backend:\n    image: alpine\n    commands:\n      - echo \"Hello there from ConfigAPI\"\n")
    print(data)
    return {"data": data}

