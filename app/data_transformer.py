from datetime import datetime
import polars as pl

from logger import logger


class DataTransformer:
    @staticmethod
    def parse_datetime(dt_str: str | None) -> datetime | None:
        if not dt_str or str(dt_str).strip() == "":
            return None
        try:
            return datetime.strptime(str(dt_str), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            logger.warning(f"Could not parse datetime: {dt_str}")
            return None

    @classmethod
    def transform_dataframe(cls, df: pl.DataFrame) -> pl.DataFrame:
        df = df.with_columns(
            [
                pl.col("Ticket ID").cast(pl.Int64),
                pl.col("Customer Age").cast(pl.Int64),
                pl.col("Customer Satisfaction Rating").cast(pl.Float64),
                pl.col("Date of Purchase").str.strptime(pl.Date, "%Y-%m-%d"),
            ]
        )

        column_mapping: dict[str, str] = {
            "Ticket ID": "ticket_id",
            "Customer Name": "customer_name",
            "Customer Email": "customer_email",
            "Customer Age": "customer_age",
            "Customer Gender": "customer_gender",
            "Product Purchased": "product_purchased",
            "Date of Purchase": "date_of_purchase",
            "Ticket Type": "ticket_type",
            "Ticket Subject": "ticket_subject",
            "Ticket Description": "ticket_description",
            "Ticket Status": "ticket_status",
            "Resolution": "resolution",
            "Ticket Priority": "ticket_priority",
            "Ticket Channel": "ticket_channel",
            "First Response Time": "first_response_time",
            "Time to Resolution": "time_to_resolution",
            "Customer Satisfaction Rating": "customer_satisfaction_rating",
        }

        df = df.rename(column_mapping)

        df = df.with_columns(
            [
                pl.col("first_response_time").map_elements(
                    cls.parse_datetime, return_dtype=pl.Datetime
                ),
                pl.col("time_to_resolution").map_elements(
                    cls.parse_datetime, return_dtype=pl.Datetime
                ),
            ]
        )

        return df
