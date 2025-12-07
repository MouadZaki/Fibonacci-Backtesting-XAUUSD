import pandas as pd
import os

def load_local_data(filename="xau_1h.csv"):
    path = os.path.join(os.path.dirname(__file__), "..", "data", filename)
    path = os.path.abspath(path)

    df = pd.read_csv(path)

    # Merge date + time columns if needed
    if "Date" in df.columns and "Time" in df.columns:
        df["datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"])
    elif "Date" in df.columns:
        df["datetime"] = pd.to_datetime(df["Date"])
    else:
        raise ValueError("CSV must contain Date or Date+Time columns")

    df = df.sort_values("datetime")
    df = df.set_index("datetime")

    # Make sure columns exist
    required = ["Open", "High", "Low", "Close"]
    for c in required:
        if c not in df.columns:
            raise ValueError(f"Missing column: {c}")

    return df[required]   # Backtesting only needs OHLC
