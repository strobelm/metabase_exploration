from psycopg2.extensions import register_adapter, AsIs
import numpy as np

from logger import logger
from data_loader import DataLoader
from db_config import DatabaseConfig, DataLoaderConfig
from db_manager import DatabaseManager

register_adapter(np.float64, AsIs)
register_adapter(np.int64, AsIs)


class ETLProcessor:
    def __init__(self) -> None:
        self.db_config = DatabaseConfig()
        self.data_config = DataLoaderConfig()
        self.db_manager = DatabaseManager(self.db_config)
        self.data_loader = DataLoader(self.db_manager, self.data_config)

    def run(self) -> int:
        try:
            logger.info("Starting data loading process")
            self.db_manager.connect()
            self.db_manager.create_tables()
            self.data_loader.load_from_csv_to_db()
            logger.info("Data loading process completed successfully")
            return 0
        except Exception as e:
            logger.error(f"Error in data loading process: {str(e)}")
            return 1
        finally:
            self.db_manager.close()


def main() -> int:
    processor = ETLProcessor()
    return processor.run()


if __name__ == "__main__":
    exit(main())
