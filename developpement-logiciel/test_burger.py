import os
import pytest
from unittest import mock
from datetime import datetime
import burger

# Fixture to mock the secret sauce password input or env var
@pytest.fixture(autouse=True)
def set_secret_sauce_password(monkeypatch):
    # Prefer env var for simplicity, but can mock input if needed
    monkeypatch.setenv("SECRET_SAUCE_PASSWORD", "testpassword")


def test_get_order_timestamp():
    ts = burger.get_order_timestamp()
    assert isinstance(ts, str)
    # This will raise if format is wrong
    datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f")


@mock.patch("builtins.input", return_value="white")
def test_get_bun(mock_input):
    bun = burger.get_bun()
    assert bun == "white"


@mock.patch("builtins.input", return_value="white")
def test_get_bun_v2(mock_input):
    # If get_bun_v2 exists
    if hasattr(burger, "get_bun_v2"):
        bun = burger.get_bun_v2()
    else:
        bun = burger.get_bun()
    assert bun == "white"


def test_calculate_burger_price():
    price = burger.calculate_burger_price(["bun", "beef", "cheese"])
    base = (
        burger.INGREDIENT_PRICES["bun"]
        + burger.INGREDIENT_PRICES["beef"]
        + burger.INGREDIENT_PRICES["cheese"]
    )
    expected = base * 1.21  # after 2 iterations of 10% tax
    assert abs(price - expected) < 0.1


@mock.patch("builtins.input", return_value="beef")
def test_get_meat_known(mock_input):
    meat = burger.get_meat()
    assert meat == "beef"


@mock.patch("builtins.input", side_effect=["unknownmeat", "beef"])
def test_get_meat_unknown_then_known(mock_input):
    meat = burger.get_meat()
    assert meat == "beef"


# Mock input for secret sauce password inside get_sauce to avoid interactive input
@mock.patch("builtins.input", return_value="testpassword")
def test_get_sauce(mock_input):
    sauce = burger.get_sauce()
    assert "ketchup" in sauce and "mustard" in sauce


@mock.patch("builtins.input", return_value="cheddar")
@mock.patch("builtins.print")
def test_get_cheese(mock_print, mock_input):
    cheese = burger.get_cheese()
    assert cheese == "cheddar"
    assert mock_print.call_count == 1


@mock.patch("burger.get_bun", return_value="white")
@mock.patch("burger.get_meat", return_value="beef")
@mock.patch("burger.get_sauce", return_value="ketchup and mustard")
@mock.patch("burger.get_cheese", return_value="cheddar")
@mock.patch("burger.calculate_burger_price", return_value=10.0)
def test_assemble_burger(
    mock_price, mock_cheese, mock_sauce, mock_meat, mock_bun
):
    burger_str = burger.assemble_burger()
    assert "white bun" in burger_str
    assert "beef" in burger_str
    assert "ketchup and mustard" in burger_str
    assert "cheddar cheese" in burger_str


@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_save_burger(mock_open):
    test_burger = "test burger"
    burger.save_burger(test_burger)
    # Should write burger and burger count to files
    assert mock_open.call_count >= 2
    mock_open().write.assert_any_call(test_burger)


@mock.patch("burger.assemble_burger", return_value="burger")
@mock.patch("burger.save_burger")
def test_main(mock_save, mock_assemble):
    burger.main()
    mock_assemble.assert_called_once()
    mock_save.assert_called_once_with("burger")
