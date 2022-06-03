# YAML Converter API

This project is to have a API to convert `drone.ci` yaml workflow format into `woodpecker-ci` one.

## How this work?

Run this project using Docker.

Make a `post` request to `localhost:port/convert`.

The `port` is your mapped port in `docker-conpose.yaml`. Default port is 80.

The post data should look like this

```json
{
    "configs": [
    {
      "name": ".woodpecekr.yaml",
      "data": "kind: pipeline\ntype: docker\nname: frontend\n\nsteps:\n  - name: frontend\n    image: node\n    commands:\n      - npm install\n      - npm test\n"
    }
  ]
}
```

The return data is your `woodpecker-ci` yaml.

```json
{
  "configs": [
    {
      "name": ".woodpecekr.yaml",
      "data": "pipeline:\n  frontend:\n    commands:\n    - npm install\n    - npm test\n    image: node\n"
    }
  ]
}
```
