import calc
import pytest

# 加算関数 add のテスト
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-5, -3, -8),
    (7, -2, 5),
    (0, 5, 5),
    (3, 0, 3),
])
def test_add(a, b, expected):
    assert calc.add(a, b) == expected

# 減算関数 subtract のテスト
@pytest.mark.parametrize("a, b, expected", [
    (5, 3, 2),
    (-3, -5, 2),
    (7, -2, 9),
    (5, 0, 5),
    (0, 3, -3),
])
def test_subtract(a, b, expected):
    assert calc.subtract(a, b) == expected

# 乗算関数 multiply のテスト
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 6),
    (-2, -3, 6),
    (2, -3, -6),
    (5, 0, 0),
    (0, 3, 0),
])
def test_multiply(a, b, expected):
    assert calc.multiply(a, b) == expected

# 除算関数 divide のテスト
@pytest.mark.parametrize("a, b, expected", [
    (6, 3, 2),
    (-6, -3, 2),
    (6, -3, -2),
])
def test_divide(a, b, expected):
    assert calc.divide(a, b) == expected


@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
    (10, 5, 15),
])

def test_add_param(a, b, expected):
    assert calc.add(a, b) == expected

# bが0の場合、ValueErrorを発生させる除算関数
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# 除算関数 divide が0で除算した場合にエラーを返すことを検証する
@pytest.mark.parametrize("a, b", [
    (5, 0),
    (0, 0),
])
def test_divide_by_zero(a, b):
    with pytest.raises(ValueError, match="0で除算された"):
        calc.divide(a, b)

# 通常の除算が正しく行われるかをテスト
def test_divide_normal():
    result = divide(10, 2)
    assert result == 5
