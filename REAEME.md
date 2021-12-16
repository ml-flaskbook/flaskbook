
## Git Cloneする

``
$ git clone https://github.com/ml-flaskbook/flaskbook.git
```

## 仮想環境を作成する

### Mac/Linuxt

```
$ python3 -m venv venv
$ source venv/bin/activate
```

### Widows（PowerShell）

スクリプトを実行するために、Windows PowerShelで次のコマンドを実行し、実行ポリシーを変更する。

```
> PowerShell Set-ExecutionPolicy RemoteSigned CurrentUser
```

ポリシーを変更したら、次のコマンドを実行する

```
> py -m venv venv
> venv\Scripts\Activate.ps1
```
