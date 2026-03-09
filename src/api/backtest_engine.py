import collections
if not hasattr(collections, 'Iterable'):
    import collections.abc
    collections.Iterable = collections.abc.Iterable

import backtrader as bt
import yfinance as yf
import pandas as pd
from datetime import datetime

from api.strategies.low_risk import LowRiskStrategy
from api.strategies.medium_risk import MediumRiskStrategy
from api.strategies.high_risk import HighRiskStrategy

# ==========================================================
# 1. MOTOR MAESTRO CON PROTECCIÓN
# ==========================================================
class GoldPilotMasterStrategy(bt.Strategy):
    params = (('risk_level', 'low'),)

    def __init__(self):
        if self.params.risk_level == 'high':
            self.logic = HighRiskStrategy()
        elif self.params.risk_level == 'medium':
            self.logic = MediumRiskStrategy()
        else:
            self.logic = LowRiskStrategy()
            
        self.gold = self.datas[0]
        self.nasdaq = self.datas[1] if len(self.datas) > 1 else None
        self.dxy = self.datas[2] if len(self.datas) > 2 else None
        self.trade_history = []

    def notify_trade(self, trade):
        if trade.isclosed:
            # Forma más segura de obtener la fecha y tipo sin usar índices de lista
            date_str = self.data.datetime.date(0).isoformat()
            # trade.long es True si fue una compra
            trade_type = "BUY" if trade.long else "SELL"
            
            self.trade_history.append({
                "date": date_str,
                "type": trade_type,
                "entry_price": round(trade.price, 2),
                "exit_price": round(self.data.close[0], 2),
                "profit": round(trade.pnlcomm, 2),
                "result": "WIN ✅" if trade.pnlcomm > 0 else "LOSS ❌"
            })

    def next(self):
        if self.position or len(self) < 50:
            return

        gold_df = pd.DataFrame({
            'open': self.gold.open.get(size=50),
            'high': self.gold.high.get(size=50),
            'low': self.gold.low.get(size=50),
            'close': self.gold.close.get(size=50)
        })
        dxy_df = pd.DataFrame({'close': self.dxy.close.get(size=50)}) if self.dxy else None
        nasdaq_df = pd.DataFrame({'close': self.nasdaq.close.get(size=50)}) if self.nasdaq else None

        if self.params.risk_level == 'high':
            signal = self.logic.analyze(gold_df)
        elif self.params.risk_level == 'medium':
            signal = self.logic.analyze(gold_df, dxy_df)
        else:
            signal = self.logic.analyze(gold_df, nasdaq_df, dxy_df)

        if signal['action'] in ["BUY", "SELL"]:
            price = self.gold.close[0]
            sl, tp = self.logic.get_execution_levels(price, signal['action'])
            
            if signal['action'] == "BUY":
                self.buy_bracket(limitprice=tp, stopprice=sl, size=self.logic.lot_size)
            elif signal['action'] == "SELL":
                self.sell_bracket(limitprice=tp, stopprice=sl, size=self.logic.lot_size)

# ==========================================================
# 2. FUNCIÓN PARA FLASK CON VERIFICACIÓN DE DATOS
# ==========================================================
def execute_backtest_by_level(level):
    cerebro = bt.Cerebro()
    initial_cash = 10000.0 
    cerebro.broker.setcash(initial_cash)
    
    tickers = {'gold': 'GC=F'}
    if level in ['low', 'medium']: tickers['dxy'] = 'DX-Y.NYB'
    if level == 'low': tickers['nasdaq'] = 'NQ=F'

    data_count = 0
    for name, ticker in tickers.items():
        df = yf.download(ticker, start='2024-01-01', interval='1d', progress=False)
        df = df.dropna()
        
        if df.empty:
            continue # Si un ticker falla, no lo añadimos
            
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        data_feed = bt.feeds.PandasData(dataname=df, name=name)
        cerebro.adddata(data_feed)
        data_count += 1

    if data_count == 0:
        return {"status": "error", "error": "No se pudieron descargar datos del mercado"}

    cerebro.addstrategy(GoldPilotMasterStrategy, risk_level=level)
    results = cerebro.run()
    
    # Verificación de seguridad para evitar el list index out of range
    if not results:
        return {"status": "error", "error": "La simulación no generó resultados"}

    final_history = results[0].trade_history
    final_val = cerebro.broker.getvalue()

    return {
        "status": "success",
        "risk_level": level,
        "initial_balance": initial_cash,
        "final_balance": round(final_val, 2),
        "profit_loss": round(final_val - initial_cash, 2),
        "profit_percent": round(((final_val - initial_cash) / initial_cash) * 100, 2),
        "trades_count": len(final_history),
        "history": final_history
    }