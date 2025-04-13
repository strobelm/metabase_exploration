import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))
from db_config import DatabaseConfig, DataLoaderConfig


class TestDatabaseConfig(unittest.TestCase):
    def setUp(self):
        self.original_env = {}
        for var in ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]:
            self.original_env[var] = os.environ.get(var)

    def tearDown(self):
        for var, value in self.original_env.items():
            if value is None:
                if var in os.environ:
                    del os.environ[var]
            else:
                os.environ[var] = value

    def test_default_values(self):
        for var in ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]:
            if var in os.environ:
                del os.environ[var]

        config = DatabaseConfig()
        self.assertEqual(config.user, "postgres")
        self.assertEqual(config.password, "postgres")
        self.assertEqual(config.host, "localhost")
        self.assertEqual(config.port, "5432")
        self.assertEqual(config.name, "customer_support")

    def test_environment_variables(self):
        os.environ["DB_USER"] = "test_user"
        os.environ["DB_PASSWORD"] = "test_password"
        os.environ["DB_HOST"] = "test_host"
        os.environ["DB_PORT"] = "5433"
        os.environ["DB_NAME"] = "test_db"

        config = DatabaseConfig()
        self.assertEqual(config.user, "test_user")
        self.assertEqual(config.password, "test_password")
        self.assertEqual(config.host, "test_host")
        self.assertEqual(config.port, "5433")
        self.assertEqual(config.name, "test_db")


class TestDataLoaderConfig(unittest.TestCase):
    def setUp(self):
        self.original_env = {}
        for var in ["CSV_PATH"]:
            self.original_env[var] = os.environ.get(var)

    def tearDown(self):
        for var, value in self.original_env.items():
            if value is None:
                if var in os.environ:
                    del os.environ[var]
            else:
                os.environ[var] = value

    def test_default_values(self):
        if "CSV_PATH" in os.environ:
            del os.environ["CSV_PATH"]

        config = DataLoaderConfig()
        self.assertEqual(config.csv_path, "customer_tickets.csv.gz")

    def test_environment_variables(self):
        os.environ["CSV_PATH"] = "/path/to/test.csv.gz"

        config = DataLoaderConfig()
        self.assertEqual(config.csv_path, "/path/to/test.csv.gz")


if __name__ == "__main__":
    unittest.main()
