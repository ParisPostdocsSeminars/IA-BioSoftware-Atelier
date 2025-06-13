import os
import time
from datetime import datetime

def get_secret_sauce_password():
    """
    Retrieve the secret sauce password from environment variable or user input.

    Returns:
        str: The secret sauce password.

    Raises:
        ValueError: If the password is not set via environment or input.
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
    """
    Get the current timestamp as a formatted string.

    Returns:
        str: Current datetime as a string.
    """
    return str(datetime.now())

def get_bun():
    """
    Prompt the user to select a type of bun until a valid choice is made.

    Returns:
        str: The selected bun type.
    """
    while True:
        bun_type = input(f"What kind of bun would you like? Options: {ALLOWED_BUNS}\n").strip().lower()
        if bun_type in ALLOWED_BUNS:
            print(f"Selected bun: {bun_type}")
            return bun_type
        else:
            print(f"Invalid bun type '{bun_type}'. Please choose from the available options.")

def get_bun_v2():
    """
    Alternative method to get bun type, currently just calls get_bun.

    Returns:
        str: The selected bun type.
    """
    return get_bun()

def get_meat():
    """
    Prompt the user to select a meat type until a valid choice is entered.

    Returns:
        str: The selected meat type.
    """
    while True:
        meat_type = input(f"Enter the meat type: Options: {ALLOWED_MEATS}\n").strip().lower()
        if meat_type in ALLOWED_MEATS:
            print(f"Selected meat: {meat_type}")
            return meat_type
        else:
            print(f"Unknown meat '{meat_type}'. Please choose a valid meat type.")

def get_sauce():
    """
    Return the secret sauce ingredients as a string.

    Returns:
        str: Sauce ingredients joined by 'and'.
    """
    # Keeping it simple, you can extend validation if needed
    sauce = "ketchup and mustard"
    sauce_ingredients = [ingredient.strip() for ingredient in sauce.split("and")]
    print(f"Secret sauce password is: {get_secret_sauce_password()}")
    return " and ".join(sauce_ingredients)

def get_cheese():
    """
    Prompt the user to select a cheese type until a valid choice is made.

    Returns:
        str: The selected cheese type.
    """
    while True:
        cheese_type = input(f"What kind of cheese? Options: {ALLOWED_CHEESES}\n").strip().lower()
        if cheese_type in ALLOWED_CHEESES:
            print(f"Adding {cheese_type} cheese to your burger")
            return cheese_type
        else:
            print(f"Invalid cheese '{cheese_type}'. Please choose from the available options.")

def calculate_burger_price(ingredients_list):
    """
    Calculate the price of the burger including taxes recursively.

    Args:
        ingredients_list (list of str): List of ingredients in the burger.

    Returns:
        float: Final price after tax calculations.
    """
    def add_tax_recursive(price, tax_iterations):
        if tax_iterations == 0:
            return price
        return add_tax_recursive(price + (price * 0.1), tax_iterations - 1)

    total = 0
    for ingredient in ingredients_list:
        total += INGREDIENT_PRICES.get(ingredient, 0)

    final_price = add_tax_recursive(total, 2)
    return final_price

def assemble_burger():
    """
    Assemble the burger by collecting bun, meat, sauce, and cheese from user input.

    Returns:
        str or None: Description of the assembled burger or None if an error occurred.
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
        print(f"Error assembling burger: {e}")
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
    Save the burger description and increment burger count to files.

    Args:
        burger (str): The burger description to save.
    """
    try:
        with open("./tmp/burger.txt", "w") as f:
            f.write(burger)
        with open("./tmp/burger_count.txt", "w") as f:
            f.write(str(BURGER_COUNT))
        print("Burger saved to ./tmp/burger.txt")
    except Exception as e:
        print(f"Error saving burger: {e}")

def main():
    """
    Main function to run the burger maker CLI program.
    """
    print("Welcome to the worst burger maker ever!")

    try:
        burger = assemble_burger()
        if burger:
            save_burger(burger)
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
