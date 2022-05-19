# YAML Converter API
This project is to have a API to convert `drone.ci` yaml workflow format in to `woodpecker-ci` one.

## How this work?
Run this project.

Make a `post` request to `0.0.0.0/convert`. Data format is 
```json
{
    "data": < drone.io ci yaml content >
}
```
The return data is your converted `woodpecker-ci` yaml.