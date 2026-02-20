import pandas as pd

class LowRiskStrategy:
    """
    Estrategia Conservadora (Low Risk)
    ----------------------------------
    Lógica: Correlación inversa entre (Nasdaq + DXY) y Oro.
    Setup: Retest de cambio de tendencia (usando SMA 50 como referencia).
    Gestión: Lot 0.1, SL 100 pips, TP en Resistencia H4.
    """

    def __init__(self):
        self.symbol = "XAUUSD"
        self.lot_size = 0.1
        self.sl_pips = 100  # 100 pips de Stop Loss fijo

    def analyze(self, gold_data, nasdaq_data, dxy_data):
        """
        Analiza el mercado y devuelve una señal.
        :param gold_data: DataFrame con velas de ORO (H4 o H1)
        :param nasdaq_data: DataFrame con velas de NASDAQ
        :param dxy_data: DataFrame con velas de DÓLAR (DXY)
        :return: Dict con la señal (BUY, SELL o WAIT)
        """
        
        # 1. ANÁLISIS MACRO (Correlación)
        # -------------------------------
        nasdaq_trend = self._get_trend_direction(nasdaq_data)
        dxy_trend = self._get_trend_direction(dxy_data)

        # Regla: Si Nasdaq y Dolar van a la misma dirección, el Oro suele ir al revés.
        if nasdaq_trend == "UP" and dxy_trend == "UP":
            sentiment = "SELL" # Oro debería bajar
        elif nasdaq_trend == "DOWN" and dxy_trend == "DOWN":
            sentiment = "BUY"  # Oro debería subir
        else:
            return {"action": "WAIT", "reason": "No hay correlación clara (Nasdaq/DXY divergentes)"}

        # 2. ANÁLISIS TÉCNICO (El Gatillo - Retest)
        # -----------------------------------------
        # Verificamos si el precio del Oro está haciendo un "Retest"
        is_retest_valid = self._check_retest(gold_data, sentiment)

        if not is_retest_valid:
            return {"action": "WAIT", "reason": f"Sentimiento {sentiment} pero sin Retest válido"}

        # 3. GESTIÓN DE RIESGO (TP y SL)
        # ------------------------------
        current_price = gold_data['close'].iloc[-1]
        
        stop_loss = self._calculate_sl(current_price, sentiment)
        take_profit = self._calculate_tp_h4(gold_data, sentiment)

        # Devolvemos la orden lista para que Dev D la envíe a MetaApi
        return {
            "action": sentiment, # "BUY" o "SELL"
            "symbol": self.symbol,
            "volume": self.lot_size,
            "price": current_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "comment": "GoldPilot LowRisk V1"
        }

    # =========================================
    # MÉTODOS AUXILIARES (Matemática Privada)
    # =========================================

    def _get_trend_direction(self, df):
        """Devuelve 'UP' o 'DOWN' basado en la media móvil simple (SMA) de 20 periodos."""
        if len(df) < 20: return "NEUTRAL" # Datos insuficientes
        
        sma_20 = df['close'].rolling(window=20).mean().iloc[-1]
        current_price = df['close'].iloc[-1]
        
        return "UP" if current_price > sma_20 else "DOWN"

    def _check_retest(self, df, direction):
        """
        Detecta un retest: El precio se acerca a la SMA 50 después de una ruptura.
        """
        if len(df) < 50: return False

        sma_50 = df['close'].rolling(window=50).mean().iloc[-1]
        current_price = df['close'].iloc[-1]
        
        # Distancia: Aceptamos si el precio está a menos del 0.15% de la media
        threshold = current_price * 0.0015 
        distance = abs(current_price - sma_50)
        
        is_near_sma = distance <= threshold
        
        # Filtro adicional: Si es BUY, el precio debe estar ligeramente por encima de la SMA
        if direction == "BUY" and current_price < sma_50:
            return False # El soporte se rompió, ya no es retest válido
            
        if direction == "SELL" and current_price > sma_50:
            return False # La resistencia se rompió
            
        return is_near_sma

    def _calculate_sl(self, price, direction):
        """Calcula SL a 100 pips (aprox $10 en precio del oro)"""
        pips_value = 10.0 
        if direction == "BUY":
            return price - pips_value
        else:
            return price + pips_value

    def _calculate_tp_h4(self, df, direction):
        """Busca el último soporte/resistencia relevante en las últimas 40 velas"""
        lookback = 40
        recent_data = df.tail(lookback)
        
        if direction == "BUY":
            # TP en el máximo más alto reciente (Resistencia)
            return recent_data['high'].max()
        else:
            # TP en el mínimo más bajo reciente (Soporte)
            return recent_data['low'].min()