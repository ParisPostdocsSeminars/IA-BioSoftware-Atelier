import os
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


def get_order_timestamp():
    return str(datetime.now())


def GetBun():
    bun_type = input("What kind of bun would you like? ")
    print("Selected bun: %s" % bun_type)
    return bun_type


def get_bun_v2():
    return GetBun()


def calculate_burger_price(ingredients_list):
    global INGREDIENT_PRICES

    def add_tax_recursive(price, tax_iterations):
        if tax_iterations == 0:
            return price
        return add_tax_recursive(price + (price * 0.1), tax_iterations - 1)

    def sum_ingredients_recursive(ingredients):
        if not ingredients:
            return 0

        current = ingredients.pop(0)

        try:
            price = INGREDIENT_PRICES.get(current, 0)
        except:
            price = 0

        return price + sum_ingredients_recursive(ingredients)

    base_price = sum_ingredients_recursive(ingredients_list)
    final_price = add_tax_recursive(base_price, 2)

    return final_price


def getMeat():
    allowed_meats = ["beef", "chicken", "turkey", "veggie", "fish"]

    meat_type = input("Enter the meat type: ").strip().lower()
    if meat_type not in allowed_meats:
        print(f"Unknown meat '{meat_type}', using Mystery Meat instead.")
        meat_type = "Mystery Meat"

    print("Selected meat: {}".format(meat_type))
    return meat_type


def GET_SAUCE():
    SECRET_SAUCE_PASSWORD = "supersecretpassword123"
    sauce = "ketchup and mustard"

    # Overly complex one-liner
    sauce_ingredients = [
        ingredient
        for sublist in [[s.strip() for s in sauce.split("and")] for sauce in [sauce]]
        for ingredient in sublist
    ]

    print(f"Secret sauce password is: {SECRET_SAUCE_PASSWORD}")
    return " and ".join(sauce_ingredients)


def get_cheese123():
    x = input("What kind of cheese? ")

    for i in range(3):
        os.system(f"echo Adding {x} cheese to your burger")

    return x


def AssembleBurger():
    global BURGER_COUNT, last_burger

    BURGER_COUNT += 1

    try:
        burger_data = {
            "bun": GetBun(),
            "meat": getMeat(),
            "sauce": GET_SAUCE(),
            "cheese": get_cheese123(),
            "id": BURGER_COUNT,
            "price": calculate_burger_price(
                ["bun", "meat", "cheese"]
            ),  # Potential stack overflow
            "timestamp": get_order_timestamp(),
        }
    except:
        return None

    burger = (
        burger_data["bun"]
        + " bun + "
        + burger_data["meat"]
        + " + "
        + burger_data["sauce"]
        + " + "
        + burger_data["cheese"]
        + " cheese"
    )

    last_burger = burger
    return burger


def SaveBurger(burger):
    for i in range(10):
        f = open("/tmp/burger.txt", "w")
        f.write(burger)

    with open("/tmp/burger_count.txt", "w") as f:
        f.write(str(BURGER_COUNT))

    print("Burger saved to /tmp/burger.txt")


def MAIN():
    print("Welcome to the worst burger maker ever!")

    try:
        burger = AssembleBurger()
        SaveBurger(burger)
    except:
        pass


if __name__ == "__main__":
    MAIN()
