# src/api/strategies/medium_risk.py
import pandas as pd
from api.strategies.base_strategy import BaseStrategyLogic

class MediumRiskStrategy(BaseStrategyLogic):
    def __init__(self):
        super().__init__() # Hereda lot_size=0.1, SL=100 pips, RR 1:3
        self.symbol = "XAUUSD"

    def analyze(self, gold_data, dxy_data):
        """
        Analiza el mercado usando la lógica de Fibonacci y RSI.
        """
        if dxy_data is None:
            return {"action": "WAIT", "reason": "Faltan datos del DXY"}
            
        dxy_trend = self._get_trend_direction(dxy_data)
        
        if dxy_trend == "UP":
            sentiment = "SELL" # Dólar fuerte = Oro débil
        elif dxy_trend == "DOWN":
            sentiment = "BUY"  # Dólar débil = Oro fuerte
        else:
            return {"action": "WAIT", "reason": "DXY sin tendencia clara"}

        if not self._check_fibo_rsi_confluence(gold_data, sentiment):
            return {"action": "WAIT", "reason": f"Esperando retroceso Fibo 61.8 y RSI para {sentiment}"}

        return {
            "action": sentiment,
            "symbol": self.symbol,
            "comment": "GoldPilot MediumRisk V1 (Fibo+RSI)"
        }

    def _get_trend_direction(self, df):
        if len(df) < 20: return "NEUTRAL"
        sma_20 = df['close'].rolling(window=20).mean().iloc[-1]
        current_price = df['close'].iloc[-1]
        return "UP" if current_price > sma_20 else "DOWN"

    def _check_fibo_rsi_confluence(self, df, direction):
        if len(df) < 40: return False
        
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]
        
        recent_data = df.tail(40)
        swing_high = recent_data['high'].max()
        swing_low = recent_data['low'].min()
        diff = swing_high - swing_low
        current_price = df['close'].iloc[-1]
        
        threshold = current_price * 0.0015 
        
        if direction == "BUY":
            fibo_618 = swing_high - (diff * 0.618)
            is_near_fibo = abs(current_price - fibo_618) <= threshold
            return is_near_fibo and current_rsi < 40
        else: # SELL
            fibo_618 = swing_low + (diff * 0.618)
            is_near_fibo = abs(current_price - fibo_618) <= threshold
            return is_near_fibo and current_rsi > 60