from coffee_etl.pipeline import process_orders_pipeline

if __name__ == "__main__":

    input_file = "orders.csv"
    clean_file = "cleaned_orders.csv"
    error_file = "error.csv"

    print("=" * 60)
    print("СТАРТ ОБРАБОТКИ ФАЙЛА ЗАКАЗОВ (DictReader)")
    print("=" * 60)
    print(process_orders_pipeline(input_file, clean_file, error_file))
    print("Имя функции:", process_orders_pipeline.__name__)
