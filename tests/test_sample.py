def test_func1():
    assert 1 == 1


def test_func2():
    assert 2 == 2


# フィクスチャの関数を引数で指定すると関数の実行結果が渡される
def test_func3(app_data):
    assert app_data == 3
