# ml_api

## Part 4 からはじめる場合

### プロジェクトのセットアップ

#### Mac/Linux

```
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip install -r requirements.txt
```

#### Windows（PowerShell）

```
> py -3 -m venv venv
> venv\Scripts\Activate.ps1
> pip install -r requirements.txt
```

### DB Migrate

```
(venv) $ flask db migrate
(venv) $ flask db upgrade
```

### 実行

```
(venv) flask run
```
