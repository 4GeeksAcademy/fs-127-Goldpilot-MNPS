import pandas as pd

class MediumRiskStrategy:
    """
    Estrategia Moderada (Medium Risk)
    ---------------------------------
    Lógica: Confluencia de DXY para la dirección.
    Setup: Retroceso al 61.8% de Fibonacci en H1 + RSI en sobrecompra/venta.
    Gestión: Lot 0.25, SL 60 pips, TP en último máximo/mínimo H1.
    """

    def __init__(self):
        self.symbol = "XAUUSD"
        self.lot_size = 0.25
        self.sl_pips = 60  # 60 pips de Stop Loss
        
    def analyze(self, gold_data, dxy_data):
        """
        Analiza el mercado usando Fibonacci y RSI.
        :param gold_data: DataFrame con velas de ORO (H1)
        :param dxy_data: DataFrame con velas de DÓLAR (DXY)
        :return: Dict con la señal (BUY, SELL o WAIT)
        """
        
        # 1. ANÁLISIS MACRO (Solo DXY)
        dxy_trend = self._get_trend_direction(dxy_data)
        
        if dxy_trend == "UP":
            sentiment = "SELL" # Si el dólar sube, el oro baja
        elif dxy_trend == "DOWN":
            sentiment = "BUY"  # Si el dólar baja, el oro sube
        else:
            return {"action": "WAIT", "reason": "DXY sin tendencia clara"}

        # 2. ANÁLISIS TÉCNICO (Fibonacci + RSI)
        is_setup_valid = self._check_fibo_rsi_confluence(gold_data, sentiment)

        if not is_setup_valid:
            return {"action": "WAIT", "reason": f"Esperando confluencia Fibo 61.8 y RSI para {sentiment}"}

        # 3. GESTIÓN DE RIESGO
        current_price = gold_data['close'].iloc[-1]
        stop_loss = self._calculate_sl(current_price, sentiment)
        take_profit = self._calculate_tp(gold_data, sentiment)

        return {
            "action": sentiment,
            "symbol": self.symbol,
            "volume": self.lot_size,
            "price": current_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "comment": "GoldPilot MediumRisk V1 (Fibo+RSI)"
        }

    # =========================================
    # MÉTODOS AUXILIARES (Matemática Privada)
    # =========================================

    def _get_trend_direction(self, df):
        """Calcula la tendencia del DXY usando una SMA de 20 periodos."""
        if len(df) < 20: return "NEUTRAL"
        
        sma_20 = df['close'].rolling(window=20).mean().iloc[-1]
        current_price = df['close'].iloc[-1]
        
        return "UP" if current_price > sma_20 else "DOWN"

    def _check_fibo_rsi_confluence(self, df, direction):
        """
        Calcula el nivel 61.8% de Fibonacci del último impulso (40 velas)
        y verifica si el RSI (14) confirma el rebote.
        """
        if len(df) < 40: return False
        
        # 1. CÁLCULO DEL RSI (14 periodos)
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)
        
        avg_gain = gain.rolling(window=14, min_periods=1).mean()
        avg_loss = loss.rolling(window=14, min_periods=1).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]
        
        # 2. CÁLCULO DE FIBONACCI (Últimas 40 velas de H1)
        recent_data = df.tail(40)
        swing_high = recent_data['high'].max()
        swing_low = recent_data['low'].min()
        diff = swing_high - swing_low
        
        current_price = df['close'].iloc[-1]
        
        # Margen de error: aceptamos que el precio esté a un 0.15% del nivel Fibo exacto
        threshold = current_price * 0.0015 
        
        if direction == "BUY":
            # El Oro va a subir (porque DXY baja). Buscamos retroceso hacia ABAJO.
            fibo_618 = swing_high - (diff * 0.618)
            is_near_fibo = abs(current_price - fibo_618) <= threshold
            
            # Confluencia: Cerca del Fibo 61.8 Y RSI mostrando sobreventa (o cerca, < 40)
            return is_near_fibo and current_rsi < 40
            
        else: # SELL
            # El Oro va a bajar (porque DXY sube). Buscamos retroceso hacia ARRIBA.
            fibo_618 = swing_low + (diff * 0.618)
            is_near_fibo = abs(current_price - fibo_618) <= threshold
            
            # Confluencia: Cerca del Fibo 61.8 Y RSI mostrando sobrecompra (o cerca, > 60)
            return is_near_fibo and current_rsi > 60

    def _calculate_sl(self, price, direction):
        """Calcula el Stop Loss a 60 pips ($6.0 en el precio del Oro)"""
        pips_value = 6.0 
        return price - pips_value if direction == "BUY" else price + pips_value

    def _calculate_tp(self, df, direction):
        """El TP es el inicio del impulso de Fibonacci (Último máximo/mínimo)"""
        recent_data = df.tail(40)
        if direction == "BUY":
            return recent_data['high'].max() # Buscamos llegar al techo anterior
        else:
            return recent_data['low'].min()  # Buscamos llegar al suelo anterior