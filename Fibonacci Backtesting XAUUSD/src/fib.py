import numpy as np
import pandas as pd

FIB_RATIOS = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]

def compute_fib_levels(high, low):
    """
    Compute Fibonacci retracement levels between high and low.
    Returns dict with ratio keys (as strings) and level prices.
    """
    if high == low or pd.isna(high) or pd.isna(low):
        return {}
    
    diff = high - low
    levels = {}
    
    for ratio in FIB_RATIOS:
        levels[f"{ratio:.3f}"] = high - (diff * ratio)
    
    return levels

def detect_fib_touches(df_window, fib_levels, tolerance=0.0008):
    """
    Detect if current price touches any Fibonacci level.
    df_window: DataFrame window with at least current candle
    fib_levels: dict from compute_fib_levels()
    tolerance: as percentage (0.0008 = 0.08%)
    """
    if df_window.empty or not fib_levels:
        return []
    
    current = df_window.iloc[-1]
    touches = []
    
    for level_name, level_price in fib_levels.items():
        tolerance_amount = level_price * tolerance
        
        if current["Low"] <= level_price + tolerance_amount and \
           current["High"] >= level_price - tolerance_amount:
            touches.append((df_window.index[-1], level_name, level_price))
    
    return touches
