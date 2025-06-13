from datetime import datetime
from unittest import mock

import pytest

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
def test_get_cheese(mock_input):
    """
    Test get_cheese returns the chosen cheese.
    """
    cheese = burger.get_cheese()
    assert cheese == "cheddar"



@mock.patch("burger.get_bun", return_value="white")
@mock.patch("burger.get_meat", return_value="beef")
@mock.patch("burger.get_sauce", return_value="ketchup and mustard")
@mock.patch("burger.get_cheese", return_value="cheddar")
@mock.patch("burger.calculate_burger_price", return_value=10.0)
def test_assemble_burger(
    mock_price, mock_cheese, mock_sauce, mock_meat, mock_bun
):
    """
    Test assemble_burger returns a string containing all components
    of the burger in the expected format.
    """
    burger_str = burger.assemble_burger()
    assert "white bun" in burger_str
    assert "beef" in burger_str
    assert "ketchup and mustard" in burger_str
    assert "cheddar cheese" in burger_str


@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_save_burger(mock_open):
    """
    Test save_burger writes burger data and burger count to files.
    """
    test_burger = "test burger"
    burger.save_burger(test_burger)
    # Should write burger and burger count to files
    assert mock_open.call_count >= 2
    mock_open().write.assert_any_call(test_burger)


@mock.patch("burger.assemble_burger", return_value="burger")
@mock.patch("burger.save_burger")
def test_main(mock_save, mock_assemble):
    """
    Test main function calls assemble_burger and save_burger once.
    """
    burger.main()
    mock_assemble.assert_called_once()
    mock_save.assert_called_once_with("burger")


@mock.patch("builtins.input", side_effect=["invalid", "invalid", "beef"])
def test_prompt_user_choice_invalid_then_valid(mock_input):
    """
    Test prompt_user_choice handles invalid input and eventually returns a valid choice.
    """
    choice = burger.prompt_user_choice("Choose a meat", burger.ALLOWED_MEATS)
    assert choice == "beef"


@mock.patch("builtins.input", side_effect=["invalid", "invalid", "invalid"])
def test_prompt_user_choice_exceeds_max_attempts(mock_input):
    """
    Test prompt_user_choice raises ValueError after max attempts with invalid input.
    """
    with pytest.raises(ValueError):
        burger.prompt_user_choice("Choose a meat", burger.ALLOWED_MEATS)


@mock.patch("builtins.input", return_value="testpassword")
@mock.patch("os.getenv", return_value=None)
def test_get_secret_sauce_password_from_input(mock_getenv, mock_input):
    """
    Test get_secret_sauce_password retrieves password from user input.
    """
    password = burger.get_secret_sauce_password()
    assert password == "testpassword"


@mock.patch("os.getenv", return_value="envpassword")
def test_get_secret_sauce_password_from_env(mock_getenv):
    """
    Test get_secret_sauce_password retrieves password from environment variable.
    """
    password = burger.get_secret_sauce_password()
    assert password == "envpassword"


@mock.patch("builtins.input", return_value="")
@mock.patch("os.getenv", return_value=None)
def test_get_secret_sauce_password_missing(mock_getenv, mock_input):
    """
    Test get_secret_sauce_password raises ValueError if neither environment variable nor input is provided.
    """
    with pytest.raises(ValueError):
        burger.get_secret_sauce_password()
