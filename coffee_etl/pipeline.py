import csv
import json
import logging
from collections import Counter, defaultdict
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from coffee_etl.decorators import measure_time, retry

logger = logging.getLogger(__name__)

VALID_MENU = {"ESPRESSO", "AMERICANO", "CAPPUCCINO", "LATTE", "FLAT WHITE"}


@dataclass
class Order:
    item_name: str
    client_name: str
    price: float
    count: int

    def order_total_cost(self):
        return self.price * self.count


def load_config(config_path: Path) -> dict:
    try:
        with open(config_path, mode="r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info(f"VALID DATA SUCCESSFULLY LOADED FROM {config_path}")
            return data
    except Exception as e:
        logger.error(f"FAILED TO LOAD VALID MENU. ERROR REASON: {e}")
        raise


def extract_orders_from_csv(file_path: Path) -> Iterator[dict]:
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if not row or not any(row.values()):
                continue
            yield row


def validate_order(row: dict, config: dict) -> tuple[Order | None, None | str]:
    item_name = str(row.get("item_name") or "").strip().upper()
    if not item_name:
        return (None, "Item name is missing")
    if item_name not in config["menu"]:
        return (None, "Item is not in menu")
    client_name = str(row.get("client_name") or "").strip().upper()
    if not client_name:
        return (None, "Client name is missing")
    try:
        price = float(row.get("price", 0))
    except (TypeError, ValueError):
        return (None, "Price must be either fraction or integer")
    if price <= 0:
        return (None, "Price must be > 0")

    try:
        count = int(row.get("count", 0))
    except (TypeError, ValueError):
        return (None, "Amount of cups must be integer")
    if count < config["min_cups"] or count > config["max_cups"]:
        return (
            None,
            f"Amount of cups must be between {config['min_cups']} and {config['max_cups']}",
        )
    order = Order(item_name, client_name, price, count)
    return (order, None)


@measure_time
@retry(retries=3, delay=0.5)
def process_orders_pipeline(
    input_path: Path, clean_path: Path, error_path: Path, config: dict
) -> dict:
    stats = {"total": 0, "clean": 0, "error": 0, "revenue": 0}
    drinks_sold = Counter()
    revenue_by_client = defaultdict(float)
    error_reasons = Counter()
    with (
        open(clean_path, mode="w", encoding="utf-8", newline="") as clean_file,
        open(error_path, mode="w", encoding="utf-8", newline="") as error_file,
    ):
        c_writer = csv.DictWriter(
            clean_file, fieldnames=["item_name", "client_name", "price", "count"]
        )
        e_writer = csv.DictWriter(
            error_file,
            fieldnames=["item_name", "client_name", "price", "count", "error_reason"],
        )
        c_writer.writeheader()
        e_writer.writeheader()
        for raw_row in extract_orders_from_csv(input_path):
            stats["total"] += 1
            order, reason = validate_order(raw_row, config)
            if order:
                stats["clean"] += 1
                drinks_sold[order.item_name] += order.count
                order_cost = order.order_total_cost()
                revenue_by_client[order.client_name] += order_cost
                stats["revenue"] += order_cost
                c_writer.writerow(
                    {
                        "item_name": order.item_name,
                        "client_name": order.client_name,
                        "price": order.price,
                        "count": order.count,
                    }
                )
            else:
                stats["error"] += 1
                error_reasons[reason] += 1
                e_writer.writerow({**raw_row, "error_reason": reason})
    stats["top_drinks"] = drinks_sold.most_common()
    stats["revenue_by_client"] = dict(revenue_by_client)
    stats["error_reasons"] = error_reasons.most_common()
    return stats


def save_report_to_json(stats: dict, report_path: Path) -> None:
    try:
        with open(report_path, mode="w", encoding="utf-8") as file:
            json.dump(stats, file, indent=4, ensure_ascii=False)
            logger.info(f"REPORT IS SAVED SUCCESSFULLY TO {report_path}")
    except (OSError, TypeError) as e:
        logger.error(f"FAILED TO SAVE REPORT. ERROR REASON: {e}")
