# src/api/strategies/high_risk.py
import pandas as pd
from api.strategies.base_strategy import BaseStrategyLogic

class HighRiskStrategy(BaseStrategyLogic):
    """
    Estrategia Agresiva (High Risk)
    -------------------------------
    Lógica: Session Breakout (Ruptura de rango de sesión).
    Setup: Ruptura del máximo o mínimo de las últimas 4 velas.
    """

    def __init__(self):
        super().__init__() # Hereda las reglas de oro
        self.symbol = "XAUUSD"
        # Sobreescribimos el lote de la base (0.1) para mantener su naturaleza agresiva
        self.lot_size = 0.50 

    def analyze(self, gold_data, dxy_data=None):
        """
        Analiza el mercado buscando rupturas de rango (Breakouts).
        """
        if len(gold_data) < 5:
            return {"action": "WAIT", "reason": "Faltan datos históricos"}

        # 1. DEFINICIÓN DEL RANGO (Últimas 4 velas, excluyendo la actual)
        recent_range = gold_data.tail(5).head(4) 
        range_high = recent_range['high'].max()
        range_low = recent_range['low'].min()
        
        # 2. GATILLO (Precio de cierre actual)
        current_price = gold_data['close'].iloc[-1]
        
        if current_price > range_high:
            sentiment = "BUY"
        elif current_price < range_low:
            sentiment = "SELL"
        else:
            return {"action": "WAIT", "reason": "Precio dentro del rango. Sin ruptura."}

        # 3. RETORNO DE SEÑAL
        # El motor aplicará SL 100 pips y TP 300 pips (Ratio 1:3) automáticamente
        return {
            "action": sentiment,
            "symbol": self.symbol,
            "comment": "GoldPilot HighRisk V1 (Breakout 1:3)"
        }