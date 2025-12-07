import pandas as pd

def simulate_trade(df, entry_time, direction, entry_price, sl_pips, tp_pips, fib_level):
    """
    Simulate a single trade and return exit time and outcome.
    outcome: 1=win, -1=loss, 0=breakeven/no exit
    
    For XAUUSD: 1 pip = 0.01 (gold moves in cents)
    """
    try:
        sub = df.loc[entry_time:]
    except KeyError:
        return None, 0, None
    
    if sub.empty:
        return None, 0, None
    
    # Convert pips to price points (1 pip = 0.01 for gold)
    pip_value = 0.01
    sl_price = sl_pips * pip_value
    tp_price = tp_pips * pip_value
    
    if direction == "long":
        sl = entry_price - sl_price
        tp = entry_price + tp_price
        
        for t, row in sub.iterrows():
            if row["Low"] <= sl:
                return t, -1, "SL"  # Stop loss hit
            if row["High"] >= tp:
                return t, 1, "TP"   # Take profit hit
        return sub.index[-1], 0, "Open"  # No exit
    
    elif direction == "short":
        sl = entry_price + sl_price
        tp = entry_price - tp_price
        
        for t, row in sub.iterrows():
            if row["High"] >= sl:
                return t, -1, "SL"  # Stop loss hit
            if row["Low"] <= tp:
                return t, 1, "TP"   # Take profit hit
        return sub.index[-1], 0, "Open"  # No exit
    
    return None, 0, None

def run_backtest(df, signals, sl_pips, tp_pips, touches=None):
    """
    Run backtest on all signals.
    Returns DataFrame with results.
    touches: optional list of (timestamp, level, price) for detailed journaling
    """
    results = []
    
    # Create a lookup for touches if provided
    touch_lookup = {}
    if touches:
        for ts, level, price in touches:
            if ts not in touch_lookup:
                touch_lookup[ts] = []
            touch_lookup[ts].append((level, price))
    
    for _, row in signals.iterrows():
        # Find the Fibonacci level for this signal
        fib_level = "Unknown"
        if row["time"] in touch_lookup:
            # Get the level closest to entry price
            levels = touch_lookup[row["time"]]
            closest = min(levels, key=lambda x: abs(x[1] - row["entry"]))
            fib_level = closest[0]
        
        end, outcome, exit_type = simulate_trade(
            df,
            row["time"],
            row["direction"],
            row["entry"],
            sl_pips,
            tp_pips,
            fib_level
        )
        
        if end is not None:
            # Calculate PnL
            if row["direction"] == "long":
                pnl = (df.loc[end, "Close"] - row["entry"]) * 100  # Simplified for display
            else:
                pnl = (row["entry"] - df.loc[end, "Close"]) * 100
            
            results.append({
                "entry_date": row["time"].date(),
                "entry_time": row["time"].time(),
                "exit_date": end.date(),
                "exit_time": end.time(),
                "direction": row["direction"].upper(),
                "entry_price": row["entry"],
                "exit_price": df.loc[end, "Close"],
                "fib_level": fib_level,
                "outcome": "WIN" if outcome == 1 else ("LOSS" if outcome == -1 else "OPEN"),
                "exit_reason": exit_type if exit_type else "No Exit",
                "pnl_pips": (df.loc[end, "Close"] - row["entry"]) * 100 if row["direction"] == "long" else (row["entry"] - df.loc[end, "Close"]) * 100
            })
    
    return pd.DataFrame(results)
