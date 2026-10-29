import os
import sys

import pandas as pd

from src.logger import logging
from src.exception import CustomException


class DataIngestion:

    def __init__(self):
        self.raw_data_path = os.path.join("artifacts", "raw.csv")
        self.train_data_path = os.path.join("artifacts", "train.csv")
        self.test_data_path = os.path.join("artifacts", "test.csv")

    def initiate_data_ingestion(self):
        try:
            logging.info("Starting data ingestion")

            data_path = os.path.join(
                "data",
                "raw",
                "DataCoSupplyChainDataset.csv"
            )

            df = pd.read_csv(data_path, encoding="latin1")

            logging.info(
                f"Loaded dataset with {df.shape[0]} rows and "
                f"{df.shape[1]} columns"
            )

            # Convert order date to datetime
            df["order date (DateOrders)"] = pd.to_datetime(
                df["order date (DateOrders)"],
                errors="coerce"
            )

            # Remove rows where the order date could not be interpreted
            df = df.dropna(
                subset=["order date (DateOrders)"]
            )

            # Sort chronologically before splitting
            df = df.sort_values(
                by="order date (DateOrders)"
            ).reset_index(drop=True)

            os.makedirs(
                os.path.dirname(self.raw_data_path),
                exist_ok=True
            )

            df.to_csv(
                self.raw_data_path,
                index=False,
                header=True
            )

            logging.info("Chronologically splitting data")

            split_index = int(len(df) * 0.8)

            train_set = df.iloc[:split_index].copy()
            test_set = df.iloc[split_index:].copy()

            train_set.to_csv(
                self.train_data_path,
                index=False,
                header=True
            )

            test_set.to_csv(
                self.test_data_path,
                index=False,
                header=True
            )

            logging.info(
                f"Training data shape: {train_set.shape}"
            )

            logging.info(
                f"Test data shape: {test_set.shape}"
            )

            logging.info("Data ingestion completed")

            return (
                self.train_data_path,
                self.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)