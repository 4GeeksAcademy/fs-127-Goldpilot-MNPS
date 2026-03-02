import pandas as pd

class HighRiskStrategy:
    """
    Estrategia Agresiva (High Risk)
    -------------------------------
    Lógica: Session Breakout (Ruptura de rango de sesión). Ignora el DXY.
    Setup: Ruptura del máximo o mínimo de las últimas 4 horas.
    Gestión: Lot 0.50, SL 40 pips, TP 120 pips (Ratio 1:3 a todo o nada).
    """

    def __init__(self):
        self.symbol = "XAUUSD"
        self.lot_size = 0.50
        self.sl_pips = 40
        self.tp_pips = 120  # Ratio 1:3 matemático
        
    def analyze(self, gold_data, dxy_data=None):
        """
        Analiza el mercado buscando rupturas de rango (Breakouts).
        El dxy_data es opcional aquí porque no lo usamos para esta estrategia.
        """
        if len(gold_data) < 5:
            return {"action": "WAIT", "reason": "Faltan datos históricos"}

        # Tomamos las velas recientes para definir el "Rango"
        recent_range = gold_data.tail(5).head(4) 
        range_high = recent_range['high'].max()
        range_low = recent_range['low'].min()
        
        # La vela actual (la que está intentando romper el rango)
        current_candle = gold_data.iloc[-1]
        current_price = current_candle['close']
        
        # Lógica de Ruptura (Breakout)
        is_breaking_high = current_price > range_high
        is_breaking_low = current_price < range_low
        
        if is_breaking_high:
            sentiment = "BUY"
        elif is_breaking_low:
            sentiment = "SELL"
        else:
            return {"action": "WAIT", "reason": "Precio dentro del rango. Sin ruptura."}

        # Calculamos SL y TP matemáticos directos (Ratio 1:3)
        stop_loss = self._calculate_sl(current_price, sentiment)
        take_profit = self._calculate_tp(current_price, sentiment)

        return {
            "action": sentiment,
            "symbol": self.symbol,
            "volume": self.lot_size,
            "price": current_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "comment": "GoldPilot HighRisk V1 (Breakout 1:3)"
        }

    def _calculate_sl(self, price, direction):
        """SL muy ajustado de 40 pips ($4.0 en el oro)"""
        pips_value = 4.0
        return price - pips_value if direction == "BUY" else price + pips_value

    def _calculate_tp(self, price, direction):
        """TP agresivo de 120 pips ($12.0 en el oro) para Ratio 1:3"""
        pips_value = 12.0
        return price + pips_value if direction == "BUY" else price - pips_value