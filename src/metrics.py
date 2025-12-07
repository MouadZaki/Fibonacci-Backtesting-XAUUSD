import pandas as pd
import numpy as np

def compute_winrate(results_df):
    """
    Calculate win rate from backtest results.
    outcome: 1=win, -1=loss, 0=breakeven
    """
    if results_df.empty:
        return 0.0
    
    wins = (results_df["outcome"] == 1).sum()
    total = len(results_df)
    
    return (wins / total * 100) if total > 0 else 0.0

def compute_rr_ratio(take_profit_pips, stop_loss_pips):
    """Calculate risk-reward ratio."""
    if stop_loss_pips == 0:
        return 0.0
    
    return take_profit_pips / stop_loss_pips

def weekday_distribution(results_df):
    """Analyze performance by weekday."""
    if results_df.empty or "entry_time" not in results_df.columns:
        return {}
    
    results_df = results_df.copy()
    results_df["weekday"] = pd.to_datetime(results_df["entry_time"]).dt.weekday
    results_df["is_win"] = results_df["outcome"] == 1
    
    weekday_stats = {}
    for day in range(7):
        day_trades = results_df[results_df["weekday"] == day]
        if len(day_trades) > 0:
            win_rate = (day_trades["is_win"].sum() / len(day_trades)) * 100
            weekday_stats[day] = {
                "trades": len(day_trades),
                "win_rate": win_rate
            }
    
    return weekday_stats

def calculate_performance_metrics(results_df):
    """Calculate comprehensive performance metrics."""
    if results_df.empty:
        return {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "win_rate": 0.0
        }
    
    total = len(results_df)
    wins = (results_df["outcome"] == 1).sum()
    losses = (results_df["outcome"] == -1).sum()
    
    win_rate = (wins / total * 100) if total > 0 else 0.0
    
    return {
        "total_trades": total,
        "winning_trades": wins,
        "losing_trades": losses,
        "win_rate": win_rate
    }