"""
Modelo Trade — Registro de operaciones de trading.
Almacena el historial completo de trades ejecutados por cada usuario.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.models.db import db


class Trade(db.Model):
    __tablename__ = 'trades'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    strategy_id: Mapped[int] = mapped_column(ForeignKey('strategies.id', ondelete='CASCADE'), nullable=False)
    wallet_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('metaapi_accounts.id'), nullable=True
    )
    meta_trade_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    symbol: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    trade_type: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    lot_size: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    open_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    close_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    stop_loss: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    take_profit: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    profit_loss: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    profit_pips: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    opened_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship('User')
    strategy = relationship('Strategy')

    def __repr__(self):
        return f'<Trade {self.id}: {self.symbol} {self.trade_type} {self.status}>'

    def serialize(self):
        """Serializa el trade a dict para la respuesta JSON."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "strategy_id": self.strategy_id,
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
            "profit_pips": self.profit_pips,
            "status": self.status,
            "opened_at": self.opened_at.isoformat() if self.opened_at else None,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
