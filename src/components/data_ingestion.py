import sys

import pandas as pd

from src.logger import logging
from src.exception import CustomException


def load_raw_data(path: str) -> pd.DataFrame:
    try:
        logging.info("Starting data ingestion for E-commerce Demand Forecasting project")

        df = pd.read_csv(path, encoding="latin1")

        logging.info(
            f"Loaded raw dataset with {df.shape[0]} rows and {df.shape[1]} columns"
        )

        return df

    except Exception as e:
        logging.error("Data ingestion failed")
        raise CustomException(e, sys)