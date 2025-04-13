import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))
from db_manager import DatabaseManager
from db_config import DatabaseConfig


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.config = DatabaseConfig()
        self.config.user = "test_user"
        self.config.password = "test_password"
        self.config.host = "test_host"
        self.config.port = "5432"
        self.config.name = "test_db"

        self.db_manager = DatabaseManager(self.config)

    @patch("db_manager.psycopg2.connect")
    def test_connect(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        connection = self.db_manager.connect()

        mock_connect.assert_called_once_with(
            user="test_user",
            password="test_password",
            host="test_host",
            port="5432",
            database="test_db",
        )

        self.assertEqual(connection, mock_connection)
        self.assertEqual(self.db_manager.connection, mock_connection)

    @patch("db_manager.psycopg2.connect")
    def test_create_tables(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        self.db_manager.connect()
        self.db_manager.create_tables()

        mock_cursor.execute.assert_called_once()
        self.assertTrue(
            "CREATE TABLE IF NOT EXISTS customer_tickets"
            in mock_cursor.execute.call_args[0][0]
        )
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()

    def test_close(self):
        mock_connection = MagicMock()
        self.db_manager.connection = mock_connection

        self.db_manager.close()

        mock_connection.close.assert_called_once()
        self.assertIsNone(self.db_manager.connection)


if __name__ == "__main__":
    unittest.main()
