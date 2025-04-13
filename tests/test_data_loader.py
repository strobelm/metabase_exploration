import unittest
from unittest.mock import patch, MagicMock
import polars as pl
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))
from data_loader import DataLoader
from db_config import DataLoaderConfig
from db_manager import DatabaseManager


class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.db_manager = MagicMock(spec=DatabaseManager)
        self.db_manager.connection = MagicMock()

        self.config = DataLoaderConfig()
        self.config.csv_path = "test_data.csv.gz"

        self.data_loader = DataLoader(self.db_manager, self.config)
        self.data_loader.transformer = MagicMock()

    @patch("polars.read_csv")
    def test_load_from_csv_to_db(self, mock_read_csv):
        mock_df = MagicMock(spec=pl.DataFrame)
        mock_df.shape = (2, 17)
        mock_df.columns = ["col1", "col2"]
        mock_df.rows.return_value = [(1, "value1"), (2, "value2")]

        mock_read_csv.return_value = mock_df
        self.data_loader.transformer.transform_dataframe.return_value = mock_df

        mock_cursor = MagicMock()
        self.db_manager.connection.cursor.return_value = mock_cursor

        self.data_loader.load_from_csv_to_db()

        mock_read_csv.assert_called_once_with(
            self.config.csv_path,
            infer_schema_length=None,
            null_values=["", "NULL", "null"],
            try_parse_dates=False,
        )

        self.data_loader.transformer.transform_dataframe.assert_called_once_with(
            mock_df
        )

        mock_cursor.execute.assert_called_once_with("TRUNCATE TABLE customer_tickets")
        self.db_manager.connection.commit.assert_called()
        mock_cursor.executemany.assert_called_once()
        mock_cursor.close.assert_called_once()

    def test_load_from_csv_to_db_no_connection(self):
        self.db_manager.connection = None

        with self.assertRaises(RuntimeError):
            self.data_loader.load_from_csv_to_db()

    @patch("polars.read_csv")
    def test_load_from_csv_to_db_exception(self, mock_read_csv):
        mock_read_csv.side_effect = Exception("Test exception")

        with self.assertRaises(Exception):
            self.data_loader.load_from_csv_to_db()

        self.db_manager.connection.rollback.assert_called_once()


if __name__ == "__main__":
    unittest.main()
