from app import app  
from api.models.db import db
from api.models import Strategy

with app.app_context():
    if Strategy.query.count() == 0:
        # Basado en tu archivo low_risk.py
        s1 = Strategy(
            name="low_risk",  # <-- El nombre interno para buscar el archivo Python luego
            display_name="Conservative Strategy",
            risk_level="low",
            description="Correlación inversa entre (Nasdaq + DXY) y Oro. Setup: Retest de cambio de tendencia con SMA 50. SL 100 pips.",
            max_trades_per_day=3,
            risk_reward_min=1.0,
            risk_reward_max=3.0,
            lot_size_factor=0.10, # Como en tu código: self.lot_size = 0.1
            is_active=True
        )
        
        # Basado en tu archivo medium_risk.py
        s2 = Strategy(
            name="medium_risk",
            display_name="Moderate Fibo & RSI",
            risk_level="medium",
            description="Confluencia de DXY para la dirección. Setup: Retroceso al 61.8% de Fibonacci en H1 + RSI en sobrecompra/venta. SL 60 pips.",
            max_trades_per_day=5,
            risk_reward_min=1.5,
            risk_reward_max=3.0,
            lot_size_factor=0.25, # Como en tu código: self.lot_size = 0.25
            is_active=True
        )
        
        # Basado en tu archivo high_risk.py
        s3 = Strategy(
            name="high_risk",
            display_name="Aggressive Breakout",
            risk_level="high",
            description="Session Breakout. Ignora el DXY. Ruptura del máximo o mínimo de las últimas 4 horas. Ratio 1:3 a todo o nada. SL 40 pips.",
            max_trades_per_day=10,
            risk_reward_min=3.0,
            risk_reward_max=5.0,
            lot_size_factor=0.50, # Como en tu código: self.lot_size = 0.50
            is_active=True
        )

        db.session.add_all([s1, s2, s3])
        db.session.commit()
        print("✅ ¡Estrategias sincronizadas con tus archivos de Python e insertadas en la BD!")
    else:
        print("⚠️ Las estrategias ya están en la base de datos.")