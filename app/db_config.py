import os


class DatabaseConfig:
    def __init__(self) -> None:
        self.user: str = os.environ.get("DB_USER", "postgres")
        self.password: str = os.environ.get("DB_PASSWORD", "postgres")
        self.host: str = os.environ.get("DB_HOST", "localhost")
        self.port: str = os.environ.get("DB_PORT", "5432")
        self.name: str = os.environ.get("DB_NAME", "customer_support")


class DataLoaderConfig:
    def __init__(self) -> None:
        self.csv_path: str = os.environ.get("CSV_PATH", "customer_tickets.csv.gz")
