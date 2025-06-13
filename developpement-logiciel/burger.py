import os
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def get_secret_sauce_password():
    """
    Retrieve the secret sauce password from environment variables or prompt the user.

    Returns:
        str: The secret sauce password.

    Raises:
        ValueError: If the password is not set and no input is given.
    """
    pwd = os.getenv("SECRET_SAUCE_PASSWORD")
    if not pwd:
        pwd = input("Enter SECRET_SAUCE_PASSWORD: ").strip()
        if not pwd:
            raise ValueError("SECRET_SAUCE_PASSWORD environment variable is not set.")
    return pwd


BURGER_COUNT = 0
last_burger = None

INGREDIENT_PRICES = {
    "bun": 2.0,
    "beef": 5.0,
    "chicken": 4.0,
    "cheese": 1.0,
    "tomato": 0.5,
    "lettuce": 0.5,
    "sauce": 0.3,
}

ALLOWED_BUNS = ["white", "whole wheat", "brioche", "gluten-free"]
ALLOWED_MEATS = ["beef", "chicken", "turkey", "veggie", "fish"]
ALLOWED_CHEESES = ["cheddar", "swiss", "american", "mozzarella", "none"]


def get_order_timestamp():
    """Return current timestamp as a string."""
    return str(datetime.now())


def prompt_user_choice(prompt, allowed_choices, max_attempts=3):
    """
    Prompt the user to input a choice from allowed options.

    Args:
        prompt (str): The prompt message to display.
        allowed_choices (list of str): Valid choices (case insensitive).
        max_attempts (int): Maximum number of input attempts before giving up.

    Returns:
        str: Validated user choice in lowercase.

    Raises:
        ValueError: If the user fails to provide a valid choice in max_attempts.
    """
    allowed_choices_lower = [choice.lower() for choice in allowed_choices]
    attempts = 0
    while attempts < max_attempts:
        user_input = input(f"{prompt} Options: {allowed_choices}\n").strip().lower()
        if user_input in allowed_choices_lower:
            logger.info(f"Selected: {user_input}")
            return user_input
        else:
            logger.warning(f"Invalid input '{user_input}'. Please choose a valid option.")
        attempts += 1
    raise ValueError(f"Maximum attempts ({max_attempts}) exceeded for input.")


def get_bun():
    """Prompt user for a valid bun type."""
    return prompt_user_choice("What kind of bun would you like?", ALLOWED_BUNS)

