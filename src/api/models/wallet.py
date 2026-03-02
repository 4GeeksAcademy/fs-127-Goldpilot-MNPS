from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from api.models.db import db


class MetaApiAccount(db.Model):
    __tablename__ = "metaapi_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # MetaApi-assigned account ID (returned after provisioning)
    account_id: Mapped[str] = mapped_column(String(255), nullable=False)
    # MT login number (stored for display; password is never persisted)
    login: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    # Broker server name e.g. "Exness-Trial", "ICMarkets-Demo01"
    server: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    # mt4 or mt5
    platform: Mapped[str] = mapped_column(String(10), default="mt4", nullable=False)
    broker_name: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    account_type: Mapped[str] = mapped_column(String(20), default="demo", nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="connected", nullable=False)
    region: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "account_id": self.account_id,
            "login": self.login,
            "server": self.server,
            "platform": self.platform,
            "broker_name": self.broker_name,
            "account_type": self.account_type,
            "status": self.status,
            "region": self.region,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
