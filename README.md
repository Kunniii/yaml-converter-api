# YAML Converter API

This project is to have a API to convert `drone.ci` yaml workflow format in to `woodpecker-ci` one.

## How this work?

Run this project.

Make a `post` request to `localhost:port/convert`.

The `port` is your mapped port in `docker-conpose.yaml`. Default port is 80.

Post data should look like this

```json
{
    "configs": [
    {
      "name": ".woodpecekr.yml",
      "data": "kind: pipeline\ntype: docker\nname: frontend\n\nsteps:\n  - name: frontend\n    image: node\n    commands:\n      - npm install\n      - npm test\n"
    }
  ]
}
```

The return data is your `woodpecker-ci` yaml.

```json
{
  "pipelines": [
    {
      "name": ".woodpecekr.yml",
      "data": "pipeline:\n  frontend:\n    commands:\n    - npm install\n    - npm test\n    image: node\n"
    }
  ]
}
```
