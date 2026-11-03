
import os
import sys
import pickle

import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.logger import logging
from src.exception import CustomException


class DateTimeFeatureExtractor(BaseEstimator, TransformerMixin):
    """Convert datetime columns into reusable calendar features."""

    def fit(self, X, y=None):
        self.date_cols_ = X.select_dtypes(
            include=["datetime", "datetimetz"]
        ).columns.tolist()

        return self

    def transform(self, X):
        X = X.copy()

        for col in self.date_cols_:
            dates = pd.to_datetime(X[col], errors="coerce")

            X[f"{col}_year"] = dates.dt.year
            X[f"{col}_month"] = dates.dt.month
            X[f"{col}_day"] = dates.dt.day
            X[f"{col}_dayofweek"] = dates.dt.dayofweek
            X[f"{col}_hour"] = dates.dt.hour

            X = X.drop(columns=[col])

        return X


class DataTransformation:

    def __init__(self):
        self.preprocessor_path = os.path.join(
            "artifacts", "preprocessor.pkl"
        )

    def get_data_transformer(self, numeric_cols, categorical_cols):
        try:
            numeric_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]
            )

            categorical_pipeline = Pipeline(
                steps=[
                    (
                        "imputer",
                        SimpleImputer(strategy="most_frequent"),
                    ),
                    (
                        "onehot",
                        OneHotEncoder(handle_unknown="ignore"),
                    ),
                ]
            )

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num", numeric_pipeline, numeric_cols),
                    ("cat", categorical_pipeline, categorical_cols),
                ],
                remainder="drop",
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            logging.info("Starting data transformation")

            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            target_col = "Order Item Quantity"

            if target_col not in train_df.columns:
                raise ValueError(
                    f"Target column '{target_col}' not found."
                )

            if target_col not in test_df.columns:
                raise ValueError(
                    f"Target column '{target_col}' not found in test data."
                )

            # Remove target, identifiers, high-cardinality fields,
            # empty fields and columns that can cause data leakage.
            drop_cols = [
                # Target and identifiers
                target_col,
                "Order Id",
                "Order Item Id",
                "Order Customer Id",
                "Customer Id",

                # Personal information
                "Customer Email",
                "Customer Password",
                "Customer Fname",
                "Customer Lname",
                "Customer Street",
                "Customer City",
                "Customer Zipcode",

                # High-cardinality geographical information
                "Order City",
                "Order State",
                "Order Zipcode",

                # Unnecessary product information
                "Product Image",
                "Product Description",

                # Financial values derived from transactions
                "Order Item Total",
                "Sales",
                "Benefit per order",
                "Order Profit Per Order",

                # Post-order information and outcomes
                "shipping date (DateOrders)",
                "Order Status",
                "Delivery Status",
                "Late_delivery_risk",
                "Days for shipping (real)",
            ]

            drop_cols = [
                col for col in drop_cols
                if col in train_df.columns
            ]

            # Convert date columns consistently in both datasets.
            date_cols = [
                col for col in train_df.columns
                if "date" in col.lower()
                and col not in drop_cols
            ]

            for col in date_cols:
                train_df[col] = pd.to_datetime(
                    train_df[col], errors="coerce"
                )

                test_df[col] = pd.to_datetime(
                    test_df[col], errors="coerce"
                )

            # Separate features and target.
            X_train = train_df.drop(columns=drop_cols)
            y_train = train_df[target_col]

            X_test = test_df.drop(
                columns=[
                    col for col in drop_cols
                    if col in test_df.columns
                ]
            )

            y_test = test_df[target_col]

            # Extract datetime features.
            datetime_extractor = DateTimeFeatureExtractor()

            X_train = datetime_extractor.fit_transform(X_train)
            X_test = datetime_extractor.transform(X_test)

            # Align test features with training features.
            X_test = X_test.reindex(columns=X_train.columns)

            # Remove columns having no observed values in training data.
            empty_cols = X_train.columns[
                X_train.isna().all()
            ].tolist()

            if empty_cols:
                logging.warning(
                    f"Dropping completely empty columns: {empty_cols}"
                )

                X_train = X_train.drop(columns=empty_cols)
                X_test = X_test.drop(columns=empty_cols)

            # Identify numerical and categorical features.
            numeric_cols = X_train.select_dtypes(
                include=["number"]
            ).columns.tolist()

            categorical_cols = X_train.select_dtypes(
                include=["object", "category", "bool", "string"]
            ).columns.tolist()

            logging.info(
                f"Numeric columns: {len(numeric_cols)}"
            )

            logging.info(
                f"Categorical columns: {len(categorical_cols)}"
            )

            logging.info(
                f"Dropped columns: {drop_cols + empty_cols}"
            )

            # Create the column transformation pipeline.
            column_preprocessor = self.get_data_transformer(
                numeric_cols,
                categorical_cols,
            )

            # Combine datetime extraction and preprocessing.
            preprocessor = Pipeline(
                steps=[
                    ("datetime_features", datetime_extractor),
                    ("preprocessor", column_preprocessor),
                ]
            )

            # Fit only on training data and transform test data.
            X_train_original = train_df.drop(columns=drop_cols)

            X_test_original = test_df.drop(
                columns=[
                    col for col in drop_cols
                    if col in test_df.columns
                ]
            )

            X_train_arr = preprocessor.fit_transform(
                X_train_original
            )

            X_test_arr = preprocessor.transform(
                X_test_original
            )

            # Save the complete reusable preprocessing pipeline.
            os.makedirs("artifacts", exist_ok=True)

            with open(self.preprocessor_path, "wb") as f:
                pickle.dump(preprocessor, f)

            logging.info(
                "Saved preprocessing pipeline successfully"
            )

            logging.info(
                f"Training features shape: {X_train_arr.shape}"
            )

            logging.info(
                f"Testing features shape: {X_test_arr.shape}"
            )

            logging.info("Data transformation completed successfully")

            return X_train_arr, y_train, X_test_arr, y_test

        except Exception as e:
            logging.error("Data transformation failed")
            raise CustomException(e, sys)
