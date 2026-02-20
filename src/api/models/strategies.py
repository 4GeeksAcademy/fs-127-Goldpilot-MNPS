from sqlalchemy import String, Boolean, ForeignKey, DateTime, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from api.models.db import db

class Strategy(db.Model):
    __tablename__ = 'strategies'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False) # Ej: "Low Risk"
    risk_level: Mapped[str] = mapped_column(String(20), nullable=False) # Ej: "low", "medium", "high"
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    
    # Parámetros técnicos del bot
    default_lot_size: Mapped[float] = mapped_column(Float, nullable=False)
    default_stop_loss: Mapped[int] = mapped_column(Integer, nullable=False) # Pips
    default_take_profit: Mapped[int] = mapped_column(Integer, nullable=False) # Pips

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "risk_level": self.risk_level,
            "lot_size": self.default_lot_size
        }

class UserStrategy(db.Model):
    __tablename__ = 'user_strategies'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relaciones
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    strategy_id: Mapped[int] = mapped_column(ForeignKey('strategies.id'), nullable=False)
    
    # Auditoría
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    # Relaciones SQLAlchemy para acceder a los objetos
    strategy = relationship("Strategy")
    # user = relationship("User") # Descomentar si necesitas acceder al usuario desde aquí

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "strategy_name": self.strategy.name,
            "active": self.is_active,
            "date": self.created_at
        }