# flaskbook_api

## Part 3 からはじめる場合

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

### 実行

```
(venv) flask run
```

### PyTorchの学習済みモデルの作成・保存

```
$ python
Python 3.9.7 (v3.9.7:1016ef3790, Aug 30 2021, 16:39:15)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> import torchvision
>>> model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
>>> torch.save(model, "model.pt")
```
