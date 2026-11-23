import pytest

from coffee_etl.pipeline import (
    load_config,
    process_orders_pipeline,
    validate_order,
)


@pytest.fixture
def sample_config():
    return {
        "menu": ["LATTE", "CAPPUCCINO", "FLAT WHITE"],
        "min_cups": 1,
        "max_cups": 5,
    }


def test_valid_order(sample_config):
    row = {
        "item_name": "  latte ",
        "client_name": "anna",
        "price": "4.5",
        "count": "2",
    }

    order, reason = validate_order(row, sample_config)

    assert order is not None
    assert reason is None
    assert order.item_name == "LATTE"
    assert order.client_name == "ANNA"
    assert order.order_total_cost() == 9.0


def test_item_not_in_menu(sample_config):
    row = {
        "item_name": "tea",
        "client_name": "Anna",
        "price": "3.0",
        "count": "1",
    }
    order, reason = validate_order(row, sample_config)

    assert order is None
    assert reason == "Item is not in menu"


def test_price_less_than_zero(sample_config):
    row = {
        "item_name": "  latte ",
        "client_name": "anna",
        "price": "-5",
        "count": "2",
    }
    order, reason = validate_order(row, sample_config)
    assert order is None
    assert reason == "Price must be > 0"


def test_amount_is_not_between_min_or_max(sample_config):
    row = {
        "item_name": "latte",
        "client_name": "Anna",
        "price": "3.0",
        "count": 6,
    }
    order, reason = validate_order(row, sample_config)
    assert order is None
    assert reason == "Amount of cups must be between 1 and 5"


def test_missing_client_name(sample_config):
    row = {
        "item_name": "  latte ",
        "client_name": None,
        "price": "4.5",
        "count": "2",
    }
    order, reason = validate_order(row, sample_config)
    assert order is None
    assert reason == "Client name is missing"


def test_price_is_not_numerical(sample_config):
    row = {
        "item_name": "  latte ",
        "client_name": "anna",
        "price": "abc",
        "count": "2",
    }
    order, reason = validate_order(row, sample_config)
    assert order is None
    assert reason == "Price must be either fraction or integer"


def test_process_orders_pipeline(tmp_path, sample_config):
    input_path = tmp_path / "orders.csv"
    input_path.write_text(
        "item_name,client_name,price,count\n"
        "cappuccino  ,John,4.50,1\n"
        "ESPRESSO,,3.00,2\n"
        "latte,  Alice  ,-4.00,1\n"
        "FLAT WHITE,Bob,5.00,10\n",
        encoding="utf-8",
    )
    clean_path = tmp_path / "cleaned_orders.csv"
    error_path = tmp_path / "error.csv"
    stats = process_orders_pipeline(input_path, clean_path, error_path, sample_config)
    assert clean_path.exists()
    assert error_path.exists()
    assert stats["total"] == 4
    assert stats["clean"] == 1
    assert stats["error"] == 3
    assert stats["revenue"] == 4.50


def test_load_config(tmp_path):
    missing_path = tmp_path / "no_such_cofig.json"
    with pytest.raises(FileNotFoundError):
        load_config(missing_path)
