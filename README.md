# YAML Converter API
This project is to have a API to convert `drone.ci` yaml workflow format in to `woodpecker-ci` one.

## How this work?
Run this project.

Make a `post` request to `0.0.0.0/convert`. Data format should look like this
```json
{
    "config": [
    {
      "name": ".woodpecekr.yml",
      "data": "kind: pipeline\ntype: docker\nname: frontend\n\nsteps:\n  - name: frontend\n    image: node\n    commands:\n      - npm install\n      - npm test\n"
    }
  ]
}
```
The return data is your converted `woodpecker-ci` yaml.
```json
{
  "pipelines": [
    {
      "name": "Some name",
      "data": "pipeline:\n  frontend:\n    commands:\n    - npm install\n    - npm test\n    image: node\n"
    }
  ]
}
```