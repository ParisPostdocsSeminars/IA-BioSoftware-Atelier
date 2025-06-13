import logging
import os
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def get_secret_sauce_password():
    """
    Return secret sauce password from environment or user input.

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
debug = True

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
    Prompt user for a choice from allowed options.

    Args:
        prompt (str): The prompt message to display.
        allowed_choices (list): List of valid choices.
        max_attempts (int, optional): Maximum input attempts before error. Defaults to 3.

    Returns:
        str: Validated user choice in lowercase.

    Raises:
        ValueError: If the user fails to provide a valid choice in max_attempts.
    """
    allowed_choices_lower = [choice.lower() for choice in allowed_choices]
    attempts = 0

    while attempts < max_attempts:
        user_input = input("%s Options: %s\n" % (prompt, allowed_choices)).strip().lower()
        if user_input in allowed_choices_lower:
            logger.info("Selected: %s", user_input)
            return user_input
        logger.warning("Invalid input '%s'. Please choose a valid option.", user_input)
        attempts += 1

    raise ValueError("Maximum attempts (%d) exceeded for input." % max_attempts)


def get_bun():
    """Prompt for a valid bun type and return it."""
    return prompt_user_choice("What kind of bun would you like?", ALLOWED_BUNS)


def get_bun_v2():
    """Return bun type (calls get_bun)."""
    return get_bun()


def get_meat():
    """Prompt for a valid meat type and return it."""
    return prompt_user_choice("Enter the meat type:", ALLOWED_MEATS)


def get_sauce():
    """Return the secret sauce ingredients."""
    sauce = "ketchup and mustard"
    sauce_ingredients = [ingredient.strip() for ingredient in sauce.split("and")]
    logger.info("Secret sauce password is: %s", get_secret_sauce_password())
    return " and ".join(sauce_ingredients)


def get_cheese():
    """Prompt for a valid cheese type and return it."""
    return prompt_user_choice("What kind of cheese?", ALLOWED_CHEESES)


def calculate_burger_price(ingredients_list):
    """
    Calculate burger price with recursive tax application.

    Args:
        ingredients_list (list): Ingredients in the burger.

    Returns:
        float: Final price after tax.
    """
    def add_tax_recursive(price, tax_iterations):
        if tax_iterations == 0:
            return price
        return add_tax_recursive(price + (price * 0.1), tax_iterations - 1)

    total = 0
    for ingredient in ingredients_list:
        total += INGREDIENT_PRICES.get(ingredient, 0)

    return add_tax_recursive(total, 2)


def assemble_burger():
    """
    Interactively assemble and describe a burger.

    Returns:
        str or None: Description of the burger or None if error.
    """
    global BURGER_COUNT, last_burger

    BURGER_COUNT += 1

    try:
        bun = get_bun()
        meat = get_meat()
        sauce = get_sauce()
        cheese = get_cheese()

        burger_data = {
            "bun": bun,
            "meat": meat,
            "sauce": sauce,
            "cheese": cheese,
            "id": BURGER_COUNT,
            "price": calculate_burger_price([bun, meat, "cheese"]),
            "timestamp": get_order_timestamp(),
        }
    except Exception as e:
        logger.error("Error assembling burger: %s", e)
        return None

    burger = (
        f"{burger_data['bun']} bun + "
        f"{burger_data['meat']} + "
        f"{burger_data['sauce']} + "
        f"{burger_data['cheese']} cheese"
    )

    last_burger = burger
    return burger


def save_burger(burger):
    """
    Save burger and burger count to files.

    Args:
        burger (str): Burger description.
    """
    try:
        os.makedirs("./tmp", exist_ok=True)
        with open("./tmp/burger.txt", "w") as f:
            f.write(burger)
        with open("./tmp/burger_count.txt", "w") as f:
            f.write(str(BURGER_COUNT))
        logger.info("Burger saved to ./tmp/burger.txt")
    except Exception as e:
        logger.error("Error saving burger: %s", e)


def main():
    """Run the burger maker program."""
    logger.info("Welcome to the worst burger maker ever!")

    try:
        burger = assemble_burger()
        if burger:
            save_burger(burger)
    except Exception as e:
        logger.error("Unexpected error: %s", e)


if __name__ == "__main__":
    main()
