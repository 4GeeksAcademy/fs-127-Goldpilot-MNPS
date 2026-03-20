from .ema_cross import EmaCrossStrategy
from .rsi_macd import RsiMacdStrategy
from .bollinger_squeeze import BollingerSqueezeStrategy
from .set_forget_scalper import SetForgetScalper

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
