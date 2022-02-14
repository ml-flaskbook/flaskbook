# Python Flask による Web アプリ開発入門
## Git Clone

```
$ git clone https://github.com/ml-flaskbook/flaskbook.git
```

## 仮想環境を作成する

### Mac/Linux

```
$ python3 -m venv venv
$ source venv/bin/activate
```

### Widows（PowerShell）

スクリプトを実行するために、Windows PowerShellで次のコマンドを実行し、実行ポリシーを変更する。

```
> PowerShell Set-ExecutionPolicy RemoteSigned CurrentUser
```

ポリシーを変更したら、次のコマンドを実行する

```
> py -m venv venv
> venv\Scripts\Activate.ps1
```

## 環境変数ファイル設置

```
$ cp -p .env.local .env
```

## パッケージインストール

```
(venv) $ pip install -r requirements.txt
```

## DBマイグレート

```
(venv) $ flask db init
(venv) $ flask db migrate
(venv) $ flask db upgrade
```

## 学習済みモデルを取得する

```
(venv) $ python
>>> import torch
>>> import torchvision
>>> model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
>>> torch.save(model, "model.pt")
```

`model.pt`を`apps/detector`配下へ移動する

## アプリケーション起動

```
(venv) $ flask run
```

## テスト実行

```
$ pytest tests/detector
```

## 第2部から読み始める場合

下記コマンドで第1部までの状態に切り替えられます。

```
$ git checkout -b part1 tags/part1
```