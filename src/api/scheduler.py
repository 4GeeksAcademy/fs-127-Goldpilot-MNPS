"""
Background Scheduler — Auto-trading loop for active bots.
Runs every 15 minutes and evaluates V4 Ghost PDH/PDL signals for all users
whose bot is active (UserStrategy.is_active=True).

MetaAPI call budget per run: 2 calls per active user (candles + account-info).
4 users × 2 calls × 96 runs/day = 768 calls/day — within 2000/day limit.
"""
import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler(daemon=True)


def init_scheduler(app):
    """Register bot-signal job and start the scheduler."""

    def run_bot_signals():
        with app.app_context():
            from api.models.strategies import UserStrategy
            from api.models.wallet import MetaApiAccount
            from api.models.trade import Trade
            from api.models.db import db
            from api.trade_engine import evaluate_signal, place_order, check_prop_firm_guard
            from api.controllers.dashboard_controller import _fetch_wallet_balance

            active_strategies = UserStrategy.query.filter_by(is_active=True).all()
            if not active_strategies:
                return

            logger.info("Scheduler: evaluating signals for %d active bot(s)", len(active_strategies))

            for us in active_strategies:
                try:
                    # Use the strategy's linked wallet if set, else first connected account
                    if us.wallet_id and us.wallet:
                        account = us.wallet
                    else:
                        account = MetaApiAccount.query.filter_by(
                            user_id=us.user_id, status="connected"
                        ).first()
                    if not account:
                        continue

                    # Prop firm daily loss guard
                    if account.is_prop_firm:
                        guard = check_prop_firm_guard(account)
                        if guard["blocked"]:
                            logger.warning(
                                "Scheduler: prop firm daily loss limit — user=%d %s",
                                us.user_id, guard["reason"],
                            )
                            continue

                    bal    = _fetch_wallet_balance(account)
                    equity = bal.get("equity") or bal.get("balance") or 5_000.0

                    signal = evaluate_signal(account, us.strategy.risk_level, equity)
                    if signal["status"] != "SIGNAL_FOUND":
                        logger.debug(
                            "Scheduler: user=%d status=%s", us.user_id, signal["status"]
                        )
                        continue

                    meta_resp, meta_err = place_order(account, signal)
                    if not meta_resp:
                        logger.warning("Scheduler: place_order failed for user=%d: %s", us.user_id, meta_err)
                        continue

                    trade = Trade(
                        user_id       = us.user_id,
                        strategy_id   = us.strategy_id,
                        wallet_id     = account.id,
                        meta_trade_id = str(meta_resp.get("positionId") or meta_resp.get("orderId") or ""),
                        symbol        = "XAUUSD",
                        trade_type    = signal["action"],
                        lot_size      = signal["volume"],
                        open_price    = signal["entry"],
                        stop_loss     = signal.get("sl"),
                        take_profit   = signal.get("tp"),
                        status        = "open",
                        opened_at     = datetime.utcnow(),
                    )
                    db.session.add(trade)
                    db.session.commit()
                    logger.info(
                        "Scheduler: TRADE_PLACED user=%d action=%s entry=%s",
                        us.user_id, signal["action"], signal["entry"],
                    )

                except Exception:
                    logger.exception("Scheduler: error processing user=%d", us.user_id)
                    # never crash the loop — continue to next user

    scheduler.add_job(
        run_bot_signals,
        "interval",
        minutes=15,
        id="bot_signals",
        replace_existing=True,
    )

    if not scheduler.running:
        scheduler.start()
        logger.info("Scheduler started — evaluating bot signals every 15 min")
