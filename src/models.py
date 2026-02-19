"""
GOLDPILOT Database Models
SQLAlchemy ORM Models for PostgreSQL (Production)
"""

from sqlalchemy import (
    Column, Integer, String, Boolean, Float, Text,
    DateTime, ForeignKey, UniqueConstraint, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User account model"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    role = Column(String(20), default='user')
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    notification_email = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user_strategies = relationship('UserStrategy', back_populates='user', cascade='all, delete-orphan')
    meta_api_account = relationship('MetaApiAccount', back_populates='user', uselist=False, cascade='all, delete-orphan')
    trades = relationship('Trade', back_populates='user', cascade='all, delete-orphan')
    notifications = relationship('Notification', back_populates='user', cascade='all, delete-orphan')
    activity_logs = relationship('ActivityLog', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"


class Strategy(Base):
    """Trading strategy model (seeded data - not user-editable)"""
    __tablename__ = 'strategies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    display_name = Column(String(100))
    risk_level = Column(String(10))
    description = Column(Text)
    max_trades_per_day = Column(Integer)
    risk_reward_min = Column(Float)
    risk_reward_max = Column(Float)
    lot_size_factor = Column(Float)
    is_active = Column(Boolean, default=True)

    # Relationships
    user_strategies = relationship('UserStrategy', back_populates='strategy', cascade='all, delete-orphan')
    trades = relationship('Trade', back_populates='strategy', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Strategy(id={self.id}, name='{self.name}', risk_level='{self.risk_level}')>"


class MetaApiAccount(Base):
    """MetaTrader API account connection model"""
    __tablename__ = 'meta_api_accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    meta_account_id = Column(String(255))
    meta_token = Column(String(255))  # Should be encrypted in application layer
    account_type = Column(String(10))  # 'demo' or 'real'
    broker = Column(String(50))
    is_connected = Column(Boolean, default=False)
    last_synced_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship('User', back_populates='meta_api_account')

    def __repr__(self):
        return f"<MetaApiAccount(id={self.id}, user_id={self.user_id}, account_type='{self.account_type}')>"


class UserStrategy(Base):
    """User-strategy association model (max 1 active per user)"""
    __tablename__ = 'user_strategies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    strategy_id = Column(Integer, ForeignKey('strategies.id', ondelete='CASCADE'), nullable=False)
    is_active = Column(Boolean, default=True)
    activated_at = Column(DateTime)
    deactivated_at = Column(DateTime)

    # Relationships
    user = relationship('User', back_populates='user_strategies')
    strategy = relationship('Strategy', back_populates='user_strategies')

    # Indexes
    __table_args__ = (
        Index('idx_user_strategies_user_id', 'user_id'),
        Index('idx_user_strategies_strategy_id', 'strategy_id'),
        # Unique constraint: only one active strategy per user
        Index('idx_user_strategies_one_active', 'user_id', unique=True,
              postgresql_where=(Column('is_active') == True)),
    )

    def __repr__(self):
        return f"<UserStrategy(id={self.id}, user_id={self.user_id}, strategy_id={self.strategy_id}, is_active={self.is_active})>"


class Trade(Base):
    """Trade execution model"""
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    strategy_id = Column(Integer, ForeignKey('strategies.id', ondelete='CASCADE'), nullable=False)
    meta_trade_id = Column(String(255))
    symbol = Column(String(20))  # e.g., XAUUSD
    trade_type = Column(String(10))  # 'BUY' or 'SELL'
    lot_size = Column(Float)
    open_price = Column(Float)
    close_price = Column(Float)
    stop_loss = Column(Float)
    take_profit = Column(Float)
    profit_loss = Column(Float)
    profit_pips = Column(Float)
    status = Column(String(10))
    opened_at = Column(DateTime)
    closed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship('User', back_populates='trades')
    strategy = relationship('Strategy', back_populates='trades')

    # Indexes
    __table_args__ = (
        Index('idx_trades_user_id', 'user_id'),
        Index('idx_trades_strategy_id', 'strategy_id'),
        Index('idx_trades_created_at', 'created_at'),
    )

    def __repr__(self):
        return f"<Trade(id={self.id}, symbol='{self.symbol}', type='{self.trade_type}', status='{self.status}')>"


class Notification(Base):
    """User notification model"""
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    type = Column(String(30))
    title = Column(String(200))
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship('User', back_populates='notifications')

    # Indexes
    __table_args__ = (
        Index('idx_notifications_user_id', 'user_id'),
    )

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type='{self.type}', is_read={self.is_read})>"


class ActivityLog(Base):
    """System activity log model"""
    __tablename__ = 'activity_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    action = Column(String(50))
    details = Column(Text)
    ip_address = Column(String(45))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship('User', back_populates='activity_logs')

    # Indexes
    __table_args__ = (
        Index('idx_activity_logs_user_id', 'user_id'),
        Index('idx_activity_logs_created_at', 'created_at'),
    )

    def __repr__(self):
        return f"<ActivityLog(id={self.id}, user_id={self.user_id}, action='{self.action}')>"


# Database initialization and session management
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def init_db(database_url: str):
    """
    Initialize the database connection and create all tables.

    Args:
        database_url: SQLAlchemy database URL
                     Example: 'postgresql://user:password@localhost/goldpilot'

    Returns:
        engine, SessionLocal
    """
    engine = create_engine(database_url, echo=True)
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return engine, SessionLocal


# Example usage
if __name__ == '__main__':
    # For development (SQLite)
    DATABASE_URL = "sqlite:///./goldpilot.db"

    # For production (PostgreSQL)
    # DATABASE_URL = "postgresql://user:password@localhost/goldpilot"

    engine, SessionLocal = init_db(DATABASE_URL)
    print("Database initialized successfully!")
