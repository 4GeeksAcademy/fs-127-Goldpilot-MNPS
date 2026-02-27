"""
============================================================
GoldPilot - MetaApiAccount Model (SQLAlchemy 2)
============================================================
Represents a user's linked MetaApi broker account.

MetaApi is a cloud service that connects to MetaTrader 4/5
brokers, allowing our bot to execute trades programmatically.

Table: metaapi_accounts
Relationship: One User -> One MetaApiAccount
============================================================
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.config import db


class MetaApiAccount(db.Model):
    """
    MetaApiAccount model — stores broker connection credentials.

    Attributes:
        id: Unique identifier (primary key)
        user_id: FK to the user who owns this account
        account_id: MetaApi account ID (from metaapi.cloud dashboard)
        api_token: MetaApi API token for authentication
        broker_name: Name of the broker (e.g., "IC Markets")
        account_type: "demo" or "live"
        status: Connection status ("connected", "disconnected", "error")
        last_synced_at: Last successful data sync timestamp
    """
    __tablename__ = "metaapi_accounts"

    # -- Primary Key --
    id: Mapped[int] = mapped_column(primary_key=True)

    # -- Foreign Key to User --
    # Each MetaApi account belongs to exactly one user
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,  # One account per user
        nullable=False
    )

    # -- MetaApi Credentials --
    account_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    api_token: Mapped[str] = mapped_column(
        Text,  # Tokens can be long, so we use Text instead of String
        nullable=False
    )

    # -- Broker Information --
    broker_name: Mapped[Optional[str]] = mapped_column(
        String(120),
        nullable=True
    )
    account_type: Mapped[str] = mapped_column(
        String(20),
        default="demo",  # Default to demo for safety
        nullable=False
    )

    # -- Connection Status --
    status: Mapped[str] = mapped_column(
        String(20),
        default="disconnected",
        nullable=False
    )

    # -- Timestamps --
    last_synced_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # -- Relationship back to User --
    user: Mapped["User"] = relationship("User", back_populates="metaapi_account")

    def serialize(self) -> dict:
        """
        Convert to dict for JSON response.

        NOTE: We mask the api_token for security — only show
        the last 8 characters so the user can identify it.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "account_id": self.account_id,
            "api_token_masked": f"...{self.api_token[-8:]}" if self.api_token else None,
            "broker_name": self.broker_name,
            "account_type": self.account_type,
            "status": self.status,
            "last_synced_at": self.last_synced_at.isoformat() if self.last_synced_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"<MetaApiAccount {self.broker_name} ({self.account_type})>"
