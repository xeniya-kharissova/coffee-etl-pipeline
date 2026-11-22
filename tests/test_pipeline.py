from coffee_etl.pipeline import validate_order

SAMPLE_CONFIG = {
    "menu" : ["LATTE", "CAPPUCINO", "FLAT WHITE"],
    "min_cups" : 1,
    "max_cups" : 5,
}

def test_valid_order():
    row = {
        "item_name": "  latte ",
        "client_name": "anna",
        "price": "4.5",
        "count": "2",
    }

    order, reason = validate_order(row, SAMPLE_CONFIG)

    assert order is not None
    assert reason is None
    assert order.item_name == "LATTE"
    assert order.client_name == "ANNA"
    assert order.order_total_cost() == 9.0

def test_item_not_in_menu():
    row = {
        "item_name": "tea",
        "client_name": "Anna",
        "price": "3.0",
        "count": "1",
    }
    order, reason = validate_order(row, SAMPLE_CONFIG)

    assert order is None
    assert reason == "Item is not in menu"

def test_price_less_than_zero():
    row = {
        "item_name": "  latte ",
        "client_name": "anna",
        "price": "-5",
        "count": "2",
    }
    order, reason = validate_order(row, SAMPLE_CONFIG)
    assert order is None
    assert reason == "Price must be > 0"

def test_amount_is_not_between_min_or_max():
    row = {
            "item_name": "latte",
            "client_name": "Anna",
            "price": "3.0",
            "count": 6,
        }
    order, reason = validate_order(row, SAMPLE_CONFIG)
    assert order is None
    assert reason == "Amount of cups must be between 1 and 5"

def test_missing_client_name():
    row = {
        "item_name": "  latte ",
        "client_name": None,
        "price": "4.5",
        "count": "2",
    }
    order, reason = validate_order(row, SAMPLE_CONFIG)
    assert order is None
    assert reason == "Client name is missing"

def test_price_is_not_numerical():
    row = {
        "item_name": "  latte ",
        "client_name": "anna",
        "price": "abc",
        "count": "2",
    }
    order, reason = validate_order(row, SAMPLE_CONFIG)
    assert order is None
    assert reason == "Price must be either fraction or integer"
