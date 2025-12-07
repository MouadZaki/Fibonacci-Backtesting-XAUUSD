import pandas as pd

class FibStrategy:
    def __init__(self, stop_loss_pips=200, take_profit_pips=300):
        self.sl = stop_loss_pips
        self.tp = take_profit_pips

    def generate_signals(self, df: pd.DataFrame, fib_touches):
        signals = []
        for timestamp, level, price in fib_touches:
            # Convert level string to float for comparison
            level_float = float(level)
            direction = "long" if level_float < 0.5 else "short"
            signals.append({
                "time": timestamp,
                "direction": direction,
                "entry": price
            })
        return pd.DataFrame(signals)
