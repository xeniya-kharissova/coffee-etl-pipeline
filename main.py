from coffee_etl.pipeline import process_orders_pipeline
from pathlib import Path

if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent
    input_path = BASE_DIR / "orders.csv"
    output_dir = BASE_DIR / "output"
    clean_path = output_dir / "cleaned_orders.csv"
    error_path = output_dir / "error.csv"
    output_dir.mkdir(parents=True, exist_ok=True)



    print("=" * 60)
    print("СТАРТ ОБРАБОТКИ ФАЙЛА ЗАКАЗОВ (DictReader)")
    print("=" * 60)
    print(process_orders_pipeline(input_path, clean_path, error_path))
    print("Имя функции:", process_orders_pipeline.__name__)
