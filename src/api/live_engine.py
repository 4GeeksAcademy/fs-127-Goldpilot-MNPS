import yfinance as yf
import pandas as pd
from datetime import datetime

# ¡Importamos las mismas estrategias exactas que en el backtest!
from api.strategies.low_risk import LowRiskStrategy
from api.strategies.medium_risk import MediumRiskStrategy
from api.strategies.high_risk import HighRiskStrategy

def get_live_data(ticker):
    df = yf.download(ticker, period="50d", interval="1d", progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df.dropna()

def evaluate_live_market(risk_level):
    if risk_level == 'high':
        logic = HighRiskStrategy()
    elif risk_level == 'medium':
        logic = MediumRiskStrategy()
    else:
        logic = LowRiskStrategy()

    gold_df = get_live_data('GC=F')
    dxy_df = get_live_data('DX-Y.NYB') if risk_level in ['low', 'medium'] else None
    nasdaq_df = get_live_data('NQ=F') if risk_level == 'low' else None

    if gold_df.empty:
        return {"status": "error", "msg": "No se pudo obtener el precio actual del Oro"}

    if risk_level == 'high':
        signal = logic.analyze(gold_df)
    elif risk_level == 'medium':
        signal = logic.analyze(gold_df, dxy_df)
    else:
        signal = logic.analyze(gold_df, nasdaq_df, dxy_df)

    current_price = gold_df['close'].iloc[-1]
    
    if signal['action'] in ["BUY", "SELL"]:
        sl, tp = logic.get_execution_levels(current_price, signal['action'])
        
        return {
            "status": "SIGNAL_FOUND",
            "action": signal['action'],
            "symbol": logic.symbol,
            "lot_size": logic.lot_size,
            "entry_price": round(current_price, 2),
            "stop_loss": round(sl, 2),
            "take_profit": round(tp, 2),
            "timestamp": datetime.now().isoformat()
        }
    
    return {
        "status": "WAITING",
        "msg": "Mercado analizado. Ningún setup cumple las reglas en este momento.",
        "current_price": round(current_price, 2),
        "timestamp": datetime.now().isoformat()
    }