"""
Modelo Trade — Registro de operaciones de trading.
Almacena el historial completo de trades ejecutados por cada usuario.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from api.models.db import db


class Trade(db.Model):
    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    wallet_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("metaapi_accounts.id"), nullable=True
    )
    meta_trade_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, default="XAUUSD")
    trade_type: Mapped[str] = mapped_column(String(10), nullable=False)
    lot_size: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    open_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    close_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    stop_loss: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    take_profit: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    profit_loss: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    opened_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="open")

    def serialize(self):
        """Serializa el trade a dict para la respuesta JSON."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "wallet_id": self.wallet_id,
            "meta_trade_id": self.meta_trade_id,
            "symbol": self.symbol,
            "trade_type": self.trade_type,
            "lot_size": self.lot_size,
            "open_price": self.open_price,
            "close_price": self.close_price,
            "stop_loss": self.stop_loss,
            "take_profit": self.take_profit,
            "profit_loss": self.profit_loss,
            "opened_at": self.opened_at.isoformat() if self.opened_at else None,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
            "status": self.status,
        }
