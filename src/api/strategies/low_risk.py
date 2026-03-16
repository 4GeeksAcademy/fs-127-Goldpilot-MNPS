# src/api/strategies/low_risk.py
import pandas as pd
from api.strategies.base_strategy import BaseStrategyLogic

class LowRiskStrategy(BaseStrategyLogic):
    def __init__(self):
        super().__init__() # Hereda lot_size=0.1, SL=100 pips, RR 1:3
        self.symbol = "XAUUSD"

    def analyze(self, gold_data, nasdaq_data, dxy_data):
        if nasdaq_data is None or dxy_data is None:
            return {"action": "WAIT", "reason": "Faltan datos de correlación"}
        
        nasdaq_trend = self._get_trend_direction(nasdaq_data)
        dxy_trend = self._get_trend_direction(dxy_data)

        if nasdaq_trend == "UP" and dxy_trend == "UP":
            sentiment = "SELL" 
        elif nasdaq_trend == "DOWN" and dxy_trend == "DOWN":
            sentiment = "BUY"
        else:
            return {"action": "WAIT", "reason": "Divergencia Nasdaq/DXY"}

        if not self._check_retest(gold_data, sentiment):
            return {"action": "WAIT", "reason": f"Sentimiento {sentiment} sin Retest en SMA 50"}

        return {
            "action": sentiment,
            "symbol": self.symbol,
            "comment": "GoldPilot LowRisk V1"
        }

    def _get_trend_direction(self, df):
        if len(df) < 20: return "NEUTRAL"
        sma_20 = df['close'].rolling(window=20).mean().iloc[-1]
        current_price = df['close'].iloc[-1]
        return "UP" if current_price > sma_20 else "DOWN"

    def _check_retest(self, df, direction):
        if len(df) < 50: return False
        sma_50 = df['close'].rolling(window=50).mean().iloc[-1]
        current_price = df['close'].iloc[-1]
        
        threshold = current_price * 0.0015 
        distance = abs(current_price - sma_50)
        
        is_near_sma = distance <= threshold
        
        if direction == "BUY" and current_price < sma_50: return False
        if direction == "SELL" and current_price > sma_50: return False
            
        return is_near_sma