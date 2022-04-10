# Python Flask による Web アプリ開発入門
## Git Clone

```
$ git clone https://github.com/ml-flaskbook/flaskbook.git
```

## Build and Run Docker Image

```
$ docker build ./ -t flaskbook-api
# ローカルで動作確認時（ローカルをマウント）
$ docker run  -p 15000:5000 --name flaskbook-api -v $(pwd)/flaskbook_api/api:/opt/flaskbook_api/api flaskbook-api
```

## Check

```
$ curl -X POST http://localhost:15000/prediction_example -H "Content-Type: application/json" -d '{"filename":"test.jpg"}'
```

```
{
  "input": {
    "filename": "test.jpg"
  },
  "result": "OK"
}
```