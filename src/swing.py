import pandas as pd
import numpy as np

def detect_swings(df, left=3, right=3):
    """
    Detect swing highs and lows using local extrema.
    Returns (highs_indices, lows_indices)
    """
    highs = []
    lows = []
    
    for i in range(left, len(df) - right):
        # Check if it's a swing high
        if df["High"].iloc[i] == df["High"].iloc[i-left:i+right+1].max():
            highs.append(i)
        
        # Check if it's a swing low
        if df["Low"].iloc[i] == df["Low"].iloc[i-left:i+right+1].min():
            lows.append(i)
    
    return highs, lows

def swing_high_low(df, lookback=50):
    """
    Calculate rolling swing highs and lows.
    """
    rolling_high = df["High"].rolling(window=lookback, min_periods=1).max()
    rolling_low = df["Low"].rolling(window=lookback, min_periods=1).min()
    
    return rolling_high, rolling_low