import psycopg2
from psycopg2.extensions import connection as PgConnection

from db_config import DatabaseConfig
from logger import logger


class DatabaseManager:
    def __init__(self, config: DatabaseConfig) -> None:
        self.config = config
        self.connection: PgConnection | None = None

    def connect(self) -> PgConnection:
        try:
            self.connection = psycopg2.connect(
                user=self.config.user,
                password=self.config.password,
                host=self.config.host,
                port=self.config.port,
                database=self.config.name,
            )
            return self.connection
        except Exception as e:
            logger.error(f"Error connecting to PostgreSQL: {str(e)}")
            raise

    def create_tables(self) -> None:
        if not self.connection:
            raise RuntimeError("Database connection not established")

        try:
            cursor = self.connection.cursor()

            create_table_sql = """
            CREATE TABLE IF NOT EXISTS customer_tickets (
                ticket_id INTEGER PRIMARY KEY,
                customer_name VARCHAR(100),
                customer_email VARCHAR(100),
                customer_age INTEGER,
                customer_gender VARCHAR(20),
                product_purchased VARCHAR(100),
                date_of_purchase DATE,
                ticket_type VARCHAR(50),
                ticket_subject VARCHAR(200),
                ticket_description TEXT,
                ticket_status VARCHAR(50),
                resolution TEXT,
                ticket_priority VARCHAR(20),
                ticket_channel VARCHAR(50),
                first_response_time TIMESTAMP,
                time_to_resolution TIMESTAMP,
                customer_satisfaction_rating REAL
            );
            """

            cursor.execute(create_table_sql)
            self.connection.commit()
            cursor.close()
            logger.info("Database tables created successfully")
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            logger.error(f"Error creating tables: {str(e)}")
            raise

    def close(self) -> None:
        if self.connection:
            self.connection.close()
            self.connection = None
