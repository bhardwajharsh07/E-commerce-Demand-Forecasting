import os
import sys
import pandas as pd

from src.logger import logging
from src.exception import CustomException


class DataIngestion:

    def __init__(self):
        self.source_data_path = os.path.join(
            "data", "raw", "DataCoSupplyChainDataset.csv"
        )
        self.raw_data_path = os.path.join("artifacts", "raw.csv")
        self.train_data_path = os.path.join("artifacts", "train.csv")
        self.test_data_path = os.path.join("artifacts", "test.csv")

    def initiate_data_ingestion(self):
        try:
            logging.info("Starting data ingestion")

            df = pd.read_csv(self.source_data_path, encoding="latin1")

            if df.empty:
                raise ValueError("The source dataset is empty.")

            logging.info(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns")

            # Identify and convert date columns.
            date_cols = [
                col for col in df.columns
                if "date" in col.lower()
            ]

            for col in date_cols:
                df[col] = pd.to_datetime(df[col], errors="coerce")

            # Use order date to preserve chronological order.
            order_date_col = "order date (DateOrders)"

            if order_date_col not in df.columns:
                raise ValueError(f"Required column '{order_date_col}' not found.")

            if df[order_date_col].isna().any():
                raise ValueError(
                    "Order dates contain missing or invalid values. "
                    "Inspect these records before splitting."
                )

            df = df.sort_values(order_date_col).reset_index(drop=True)

            os.makedirs("artifacts", exist_ok=True)

            df.to_csv(self.raw_data_path, index=False)
   
            # Split chronologically using calendar dates.
            # All transactions from the same date stay in one dataset.

            df["order_date_day"] = df[order_date_col].dt.normalize()

            unique_dates = (
                df["order_date_day"]
                .drop_duplicates()
                .sort_values()
                .reset_index(drop=True)
            )

            date_split_index = int(len(unique_dates) * 0.8)

            if date_split_index == 0 or date_split_index == len(unique_dates):
                raise ValueError("Insufficient unique dates for a chronological split.")

            split_date = unique_dates.iloc[date_split_index]

            train_set = df[df["order_date_day"] < split_date].copy()
            test_set = df[df["order_date_day"] >= split_date].copy()

            # Remove the temporary splitting column.
            train_set.drop(columns=["order_date_day"], inplace=True)
            test_set.drop(columns=["order_date_day"], inplace=True)

            if train_set.empty or test_set.empty:
                raise ValueError("Chronological split produced an empty dataset.")

            train_set.to_csv(self.train_data_path, index=False)
            test_set.to_csv(self.test_data_path, index=False)

            logging.info(f"Training data: {train_set.shape[0]} rows")

            logging.info(f"Testing data: {test_set.shape[0]} rows")

            logging.info(f"Chronological split date: {split_date}")

            logging.info("Data ingestion completed successfully")


            return self.train_data_path, self.test_data_path

        except Exception as e:
            logging.error("Data ingestion failed")
            raise CustomException(e, sys)

        