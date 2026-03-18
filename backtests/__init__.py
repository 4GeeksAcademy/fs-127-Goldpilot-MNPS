from strategies.ema_cross import EmaCrossStrategy
from strategies.rsi_macd import RsiMacdStrategy
from strategies.bollinger_squeeze import BollingerSqueezeStrategy
from strategies.set_forget_scalper import SetForgetScalper

STRATEGY_MAP = {
    "ema_cross":          EmaCrossStrategy,
    "rsi_macd":           RsiMacdStrategy,
    "bollinger_squeeze":  BollingerSqueezeStrategy,
    "set_forget_scalper": SetForgetScalper,
}

__all__ = [
    "EmaCrossStrategy",
    "RsiMacdStrategy",
    "BollingerSqueezeStrategy",
    "SetForgetScalper",
    "STRATEGY_MAP",
]
