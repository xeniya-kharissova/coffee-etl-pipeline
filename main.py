from coffee_etl.pipeline import (
    load_config,
    process_orders_pipeline,
    save_report_to_json
    )
from pathlib import Path
import logging
import argparse


if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="ETL pipeline for processing coffee shop orders"
    )
    parser.add_argument(
        "--input",
        type = Path,
        default = BASE_DIR / "orders.csv",
        help="Path to input CSV file with raw orders",
    )
    parser.add_argument(
        "--output-dir",
        type = Path,
        default=BASE_DIR / "output",
        help = "Directory for cleaned CSV, errors CSV, and JSON report",
    )
    parser.add_argument(
        "--config",
        type = Path,
        default=BASE_DIR / "config.json",
        help="Path to JSON configuration file",
    )
    args = parser.parse_args()
    input_path = args.input
    output_dir = args.output_dir
    config_path = args.config
    clean_path = output_dir / "cleaned_orders.csv"
    error_path = output_dir / "error.csv"
    report_path = output_dir / "report.json"
    output_dir.mkdir(parents=True, exist_ok=True)

    logs_dir = BASE_DIR / "logs" 
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / "pipeline.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers = [
            logging.StreamHandler(), #вывод в терминал
            logging.FileHandler(log_path, encoding="utf-8"), #дозапись в файл
        ]
    )
    logger = logging.getLogger(__name__)


    logger.info("=" * 60)
    logger.info("СТАРТ ОБРАБОТКИ ФАЙЛА ЗАКАЗОВ (DictReader)")
    logger.info("=" * 60)
    config = load_config(config_path)
    stats = process_orders_pipeline(input_path, clean_path, error_path, config)
    logger.info(stats)
    save_report_to_json(stats, report_path)

