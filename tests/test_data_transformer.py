import unittest
from datetime import datetime, date
import polars as pl
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))
from data_transformer import DataTransformer


class TestDataTransformer(unittest.TestCase):
    def test_parse_datetime(self):
        transformer = DataTransformer()

        self.assertEqual(
            transformer.parse_datetime("2023-01-01 12:30:45"),
            datetime(2023, 1, 1, 12, 30, 45),
        )
        self.assertIsNone(transformer.parse_datetime(None))
        self.assertIsNone(transformer.parse_datetime(""))
        self.assertIsNone(transformer.parse_datetime("invalid-date"))

    def test_transform_dataframe(self):
        transformer = DataTransformer()

        test_df = pl.DataFrame(
            {
                "Ticket ID": ["1", "2"],
                "Customer Name": ["John Doe", "Jane Smith"],
                "Customer Email": ["john@example.com", "jane@example.com"],
                "Customer Age": ["30", "25"],
                "Customer Gender": ["Male", "Female"],
                "Product Purchased": ["Laptop", "Phone"],
                "Date of Purchase": ["2023-01-01", "2023-02-15"],
                "Ticket Type": ["Technical issue", "Billing inquiry"],
                "Ticket Subject": ["Can't boot", "Wrong charge"],
                "Ticket Description": ["My laptop won't start", "I was charged twice"],
                "Ticket Status": ["Open", "Closed"],
                "Resolution": [None, "Refunded extra charge"],
                "Ticket Priority": ["High", "Low"],
                "Ticket Channel": ["Email", "Phone"],
                "First Response Time": ["2023-01-02 10:30:00", "2023-02-16 09:15:00"],
                "Time to Resolution": [None, "2023-02-16 14:45:00"],
                "Customer Satisfaction Rating": [None, "4.5"],
            }
        )

        transformed_df = transformer.transform_dataframe(test_df)

        self.assertIn("ticket_id", transformed_df.columns)
        self.assertIn("customer_name", transformed_df.columns)

        self.assertEqual(transformed_df["ticket_id"].dtype, pl.Int64)
        self.assertEqual(transformed_df["customer_age"].dtype, pl.Int64)
        self.assertEqual(
            transformed_df["customer_satisfaction_rating"].dtype, pl.Float64
        )
        self.assertEqual(transformed_df["date_of_purchase"].dtype, pl.Date)

        self.assertEqual(transformed_df["ticket_id"][0], 1)
        self.assertEqual(transformed_df["customer_age"][1], 25)
        self.assertEqual(transformed_df["date_of_purchase"][0], date(2023, 1, 1))
        self.assertEqual(
            transformed_df["first_response_time"][0], datetime(2023, 1, 2, 10, 30, 0)
        )


if __name__ == "__main__":
    unittest.main()
