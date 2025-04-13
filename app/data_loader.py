from data_transformer import DataTransformer
from db_config import DataLoaderConfig
from db_manager import DatabaseManager
import polars as pl
from logger import logger


class DataLoader:
    def __init__(self, db_manager: DatabaseManager, config: DataLoaderConfig) -> None:
        self.db_manager = db_manager
        self.config = config
        self.transformer = DataTransformer()

    def load_from_csv_to_db(self) -> None:
        if not self.db_manager.connection:
            raise RuntimeError("Database connection not established")

        try:
            logger.info(f"Loading data from {self.config.csv_path}")
            df = pl.read_csv(
                self.config.csv_path,
                infer_schema_length=None,
                null_values=["", "NULL", "null"],
                try_parse_dates=False,
            )

            logger.info(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns")

            df = self.transformer.transform_dataframe(df)

            # Clear existing data
            cursor = self.db_manager.connection.cursor()
            cursor.execute("TRUNCATE TABLE customer_tickets")
            self.db_manager.connection.commit()

            columns = ", ".join(df.columns)
            placeholders = ", ".join(["%s"] * len(df.columns))
            insert_query = (
                f"INSERT INTO customer_tickets ({columns}) VALUES ({placeholders})"
            )

            rows: list[tuple] = df.rows()

            cursor.executemany(insert_query, rows)
            self.db_manager.connection.commit()

            logger.info(f"Successfully inserted {len(rows)} rows into PostgreSQL")
            cursor.close()

        except Exception as e:
            if self.db_manager.connection:
                self.db_manager.connection.rollback()
            logger.error(f"Error loading data: {str(e)}")
            raise
