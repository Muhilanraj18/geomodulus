import os
import pandas as pd


class DataPreprocessor:

    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        return pd.read_excel(self.file_path)

    def clean_data(self, df):

        # Remove unwanted columns
        df = df.drop(
            columns=[
                "S. No.",
                "Unnamed: 14",
                "Unnamed: 15"
            ],
            errors="ignore"
        )

        print("\nDataset Shape :", df.shape)

        print("\nMissing Values")
        print(df.isnull().sum())

        return df


if __name__ == "__main__":

    DATA_PATH = os.path.join(
        "data",
        "raw",
        "Correlation by ML_Data (1).xlsx"
    )

    processor = DataPreprocessor(DATA_PATH)

    df = processor.load_data()

    df = processor.clean_data(df)

    print("\nRemaining Columns")
    print(df.columns.tolist())