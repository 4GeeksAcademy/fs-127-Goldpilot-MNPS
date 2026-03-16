# src/api/strategies/high_risk.py
import pandas as pd
from api.strategies.base_strategy import BaseStrategyLogic

class HighRiskStrategy(BaseStrategyLogic):
    def __init__(self):
        super().__init__() # Hereda las reglas de oro
        self.symbol = "XAUUSD"
        self.lot_size = 0.50 

    def analyze(self, gold_data, dxy_data=None):
        if len(gold_data) < 5:
            return {"action": "WAIT", "reason": "Faltan datos históricos"}

        recent_range = gold_data.tail(5).head(4) 
        range_high = recent_range['high'].max()
        range_low = recent_range['low'].min()
        
        current_price = gold_data['close'].iloc[-1]
        
        if current_price > range_high:
            sentiment = "BUY"
        elif current_price < range_low:
            sentiment = "SELL"
        else:
            return {"action": "WAIT", "reason": "Precio dentro del rango. Sin ruptura."}

        return {
            "action": sentiment,
            "symbol": self.symbol,
            "comment": "GoldPilot HighRisk V1 (Breakout 1:3)"
        }