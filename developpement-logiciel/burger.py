import time
from datetime import datetime

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
    return str(datetime.now())

def get_bun():
    while True:
        bun_type = input(f"What kind of bun would you like? Options: {ALLOWED_BUNS}\n").strip().lower()
        if bun_type in ALLOWED_BUNS:
            print(f"Selected bun: {bun_type}")
            return bun_type
        else:
            print(f"Invalid bun type '{bun_type}'. Please choose from the available options.")

def get_meat():
    while True:
        meat_type = input(f"Enter the meat type: Options: {ALLOWED_MEATS}\n").strip().lower()
        if meat_type in ALLOWED_MEATS:
            print(f"Selected meat: {meat_type}")
            return meat_type
        else:
            print(f"Unknown meat '{meat_type}'. Please choose a valid meat type.")

def get_sauce():
    # Keeping it simple, you can extend validation if needed
    SECRET_SAUCE_PASSWORD = "supersecretpassword123"
    sauce = "ketchup and mustard"
    sauce_ingredients = [ingredient.strip() for ingredient in sauce.split("and")]
    print(f"Secret sauce password is: {SECRET_SAUCE_PASSWORD}")
    return " and ".join(sauce_ingredients)

def get_cheese():
    while True:
        cheese_type = input(f"What kind of cheese? Options: {ALLOWED_CHEESES}\n").strip().lower()
        if cheese_type in ALLOWED_CHEESES:
            for _ in range(3):
                print(f"Adding {cheese_type} cheese to your burger")
            return cheese_type
        else:
            print(f"Invalid cheese '{cheese_type}'. Please choose from the available options.")

def calculate_burger_price(ingredients_list):
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
    try:
        with open("/tmp/burger.txt", "w") as f:
            f.write(burger)
        with open("/tmp/burger_count.txt", "w") as f:
            f.write(str(BURGER_COUNT))
        print("Burger saved to /tmp/burger.txt")
    except Exception as e:
        print(f"Error saving burger: {e}")

def main():
    print("Welcome to the worst burger maker ever!")

    try:
        burger = assemble_burger()
        if burger:
            save_burger(burger)
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
