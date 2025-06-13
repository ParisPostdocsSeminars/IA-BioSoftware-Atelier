import pytest
from unittest import mock
from datetime import datetime
import burger


@pytest.fixture(autouse=True)
def set_secret_sauce_password(monkeypatch):
    """
    Fixture to set the SECRET_SAUCE_PASSWORD environment variable
    for all tests to avoid interactive input.
    """
    monkeypatch.setenv("SECRET_SAUCE_PASSWORD", "testpassword")


def test_get_order_timestamp():
    """
    Test that get_order_timestamp returns a string
    representing the current timestamp in the expected format.
    """
    ts = burger.get_order_timestamp()
    assert isinstance(ts, str)
    # This will raise if format is wrong
    datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f")


@mock.patch("builtins.input", return_value="white")
def test_get_bun(mock_input):
    """
    Test get_bun prompts the user and returns a valid bun choice.
    """
    bun = burger.get_bun()
    assert bun == "white"


@mock.patch("builtins.input", return_value="white")
def test_get_bun_v2(mock_input):
    """
    Test get_bun_v2 if available, else fallback to get_bun,
    ensuring it returns a valid bun choice.
    """
    if hasattr(burger, "get_bun_v2"):
        bun = burger.get_bun_v2()
    else:
        bun = burger.get_bun()
    assert bun == "white"


def test_calculate_burger_price():
    """
    Test calculate_burger_price correctly computes the price
    including compound tax on a sample list of ingredients.
    """
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
    """
    Test get_meat returns a valid known meat choice immediately.
    """
    meat = burger.get_meat()
    assert meat == "beef"


@mock.patch("builtins.input", side_effect=["unknownmeat", "beef"])
def test_get_meat_unknown_then_known(mock_input):
    """
    Test get_meat prompts again after invalid input
    and eventually returns a valid meat choice.
    """
    meat = burger.get_meat()
    assert meat == "beef"


@mock.patch("builtins.input", return_value="testpassword")
def test_get_sauce(mock_input):
    """
    Test get_sauce returns expected sauces, mocking password input.
    """
    sauce = burger.get_sauce()
    # Breaking assertion into parts for better clarity
    assert "ketchup" in sauce
    assert "mustard" in sauce


@mock.patch("builtins.input", return_value="cheddar")
@mock.patch("builtins.print")
def test_get_cheese(mock_print, mock_input):
    """
    Test get_cheese returns the chosen cheese and prints confirmation.
    """
    cheese = burger.get_cheese()
    assert cheese == "cheddar"
    assert mock_print.call_count == 1


@mock.patch("burger.get_bun", return_value="white")
@mock.patch("burger.get_meat", return_value="beef")
@mock.patch("burger.get_sauce", return_value="ketchup and mustard")
@mock.patch("burger.get_cheese", return_value="cheddar")
@mock.patch("burger.calculate_burger_price", return_value=10.0)
def test_assemble_burger(
    moc
