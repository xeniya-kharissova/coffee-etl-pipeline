from coffee_etl.pipeline import process_orders_pipeline
from pathlib import Path
import logging

if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent

    logs_dir = BASE_DIR / "logs" 
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / "pipeline.log"
    
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers = [
            logging.StreamHandler(), # вывод в терминал
            logging.FileHandler(log_path, encoding="utf-8"), # дозапись в файл
        ]
    )
    logger = logging.getLogger(__name__)
    

    input_path = BASE_DIR / "orders.csv"
    output_dir = BASE_DIR / "output"
    clean_path = output_dir / "cleaned_orders.csv"
    error_path = output_dir / "error.csv"
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("=" * 60)
    logger.info("СТАРТ ОБРАБОТКИ ФАЙЛА ЗАКАЗОВ (DictReader)")
    logger.info("=" * 60)
    logger.info(process_orders_pipeline(input_path, clean_path, error_path))

