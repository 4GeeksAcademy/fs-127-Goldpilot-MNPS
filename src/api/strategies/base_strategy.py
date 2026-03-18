class BaseStrategyLogic:
    def __init__(self):
        self.lot_size = 0.1      # Regla: Mínimo 0.1 lotes
        self.sl_distance = 10.0  # Regla: 100 pips ($10 USD en Oro)
        self.tp_distance = 30.0  # Regla: Ratio 1:3 ($30 USD en Oro)

    def get_execution_levels(self, price, direction):
        if direction == "BUY":
            sl = price - self.sl_distance
            tp = price + self.tp_distance
        else:
            sl = price + self.sl_distance
            tp = price - self.tp_distance
        return sl, tp