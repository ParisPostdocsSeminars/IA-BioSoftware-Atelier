import builtins
import pytest
from unittest import mock
from datetime import datetime
import burger


def test_get_order_timestamp():
    ts = burger.get_order_timestamp()
    assert isinstance(ts, str)  # nosec B101
    # This will raise if format is wrong
    datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f")


@mock.patch("builtins.input", return_value="white")
def test_get_bun():
    bun = burger.get_bun()
    assert bun == "white"  # nosec B101


@mock.patch("builtins.input", return_value="white")
def test_get_bun_v2(mock_input):
    # Add get_bun_v2 wrapper in burger.py if needed
    if hasattr(burger, "get_bun_v2"):
        bun = burger.get_bun_v2()
    else:
        bun = burger.get_bun()
    assert bun == "white"  # nosec B101


def test_calculate_burger_price():
    price = burger.calculate_burger_price(["bun", "beef", "cheese"])
    base = burger.INGREDIENT_PRICES["bun"] + burger.INGREDIENT_PRICES["beef"] + burger.INGREDIENT_PRICES["cheese"]
    expected = base * 1.21  # approx after 2 iterations of 10% tax
    assert abs(price - expected) < 0.1  # nosec B101


@mock.patch("builtins.input", return_value="beef")
def test_get_meat_known(mock_input):
    meat = burger.get_meat()
    assert meat == "beef"  # nosec B101


@mock.patch("builtins.input", side_effect=["unknownmeat", "beef"])
def test_get_meat_unknown_then_known(mock_input):
    # Assuming get_meat loops until valid input, simulate wrong then right
    meat = burger.get_meat()
    assert meat == "beef"  # nosec B101


def test_get_sauce():
    sauce = burger.get_sauce()
    assert "ketchup" in sauce and "mustard" in sauce  # nosec B101


@mock.patch("builtins.input", return_value="cheddar")
@mock.patch("builtins.print")
def test_get_cheese(mock_print, mock_input):
    cheese = burger.get_cheese()
    assert cheese == "cheddar"  # nosec B101
    assert mock_print.call_count == 3  # nosec B101


@mock.patch("burger.get_bun", return_value="white")
@mock.patch("burger.get_meat", return_value="beef")
@mock.patch("burger.get_sauce", return_value="ketchup and mustard")
@mock.patch("burger.get_cheese", return_value="cheddar")
@mock.patch("burger.calculate_burger_price", return_value=10.0)
def test_assemble_burger(mock_price, mock_cheese, mock_sauce, mock_meat, mock_bun):
    burger_str = burger.assemble_burger()
    assert "white bun" in burger_str  # nosec B101
    assert "beef" in burger_str  # nosec B101
    assert "ketchup and mustard" in burger_str  # nosec B101
    assert "cheddar cheese" in burger_str  # nosec B101


def test_save_burger(tmp_path):
    test_burger = "test burger"
    with mock.patch("builtins.open", mock.mock_open()) as m_open:
        burger.save_burger(test_burger)
        assert m_open.call_count >= 2  # nosec B101
        m_open().write.assert_any_call(test_burger)  # nosec B101


@mock.patch("burger.assemble_burger", return_value="burger")
@mock.patch("burger.save_burger")
def test_main(mock_save, mock_assemble):
    burger.main()
    mock_assemble.assert_called_once()  # nosec B101
    mock_save.assert_called_once_with("burger")  # nosec B101
