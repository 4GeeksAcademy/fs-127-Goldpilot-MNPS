"""
AGGRESSOR PULSE - LIVE TRADING BOT
===================================
Strategy: H1 Bias → M15 EMA Channel → M5 CHoCH Execution
Performance (Backtest): +9.55% ROI | 57% Win Rate | 2.82:1 Avg RRR
"""

import asyncio
import websockets
import json
from datetime import datetime, timedelta
import pytz
from metaapi_cloud_sdk import MetaApi
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.absolute()))
from strategies.aggressor_pulse_strategy import AggressorPulseStrategy

# ==========================================
# 🔐 CONFIGURATION
# ==========================================
META_API_TOKEN = os.getenv("META_API_TOKEN", "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiIxNzFjZWQ4Yjg5ODdhMWQyM2JlOGFhMTAxM2YwZjVlZCIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiwibWV0aG9kcyI6WyJtZXRhc3RhdHMtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiMTcxY2VkOGI4OTg3YTFkMjNiZThhYTEwMTNmMGY1ZWQiLCJpYXQiOjE3NjY3Mjg2MzEsImV4cCI6MTc3NDUwNDYzMX0.TlcBJs-k1nzfPIaNLcYBHkFlAWnnJ9qa43CV7aFDYxWjVxp_ZkAJRbKhy4MYhStwHMdiDP8SLVf_Zd4Wfns5qvV_HNNCiCoDDLSw8xy02gctQsr6su5ZTYCSRLfscQZDk8mfZuVfj3wKNxAYE68TeyMlBc1oEQyaHJ7AuDDGhlLDmwJINX4hhfHBxvPbdYztW92DQ_mmp9PSuLU_sr0O9NywQyiYEFXFjCl1_C_55qShFE0-_PkvnQNAzy-6-kWnqMt6Q3yiZJH_EusHF92VxVhzPcqsSFEXCK1q9VkNHT1bK9gICvGGTMGUy0qr0O0d_8THdZrSbiZKi8t9QHgYy-O4BBMvUCYIHcyDUoigwHQGJoFm_n1ZEzpunmVCqWhjwpUXKeXwQebwdJ0OHyH3bW59Z-NT-Snk70-6oHseEpjd45zBiN8pMClVhXc1DvpMiPFnXmQ4hmSmTnskdAOakXhKbx3VRt4EwRbs8-_Pupp824Q0k852X7VODZ2owKX9gZHjjOKuIG3ZlNztj6StEwb_lDzuEc3r8BNNtntZW8UBkBy9T11lj1mry0SzxsP-NSUGUnfxCtqlXgMBni1uhnyY_JtadDMtXsZ9QDiF3Way8HyBhnE4DBD7-UcsHHQobSRpyyhTYqF8bH4pjmO-Mh1IqVJLLZkZi7NJ0RNCgNk")
WS_HOST = os.getenv("WS_HOST", "0.0.0.0")
WS_PORT = int(os.getenv("PORT", "8080"))

VAULTS = [
    {"id": "77c5fbff-beb8-422a-b085-c135c230a630", "name": "QUANT_DEMO", "is_real": False, "risk_pct": 0.02},
    {"id": "436348e0-be6e-49cc-a991-8895903e5288", "name": "MICRO_REAL", "is_real": True, "risk_pct": 0.01}
]

STATE = {
    "vaults": [],
    "analysis": {"type": "HEARTBEAT", "symbol": "GOLD.pro", "price": 0, "decision": "INIT", "reason": "Initializing Aggressor Pulse..."},
    "ready": False,
    "trade_notifications": [],
    "strategies": {}  # Per-vault strategy instances
}


class AggressorPulseLive:
    """Live trading engine using Aggressor Pulse strategy"""

    def __init__(self):
        self.api = MetaApi(META_API_TOKEN)
        self.connections = {}
        self.symbol = "GOLD.pro"

    async def connect(self):
        """Connect to MetaTrader accounts"""
        for vault in VAULTS:
            try:
                print(f"🔗 Connecting to {vault['name']}...")
                acc = await self.api.metatrader_account_api.get_account(vault['id'])

                if acc.state == 'UNDEPLOYED':
                    print(f"📦 Deploying {vault['name']}...")
                    await acc.deploy()

                print(f"⏳ Waiting for {vault['name']} to connect...")
                await acc.wait_connected()

                conn = acc.get_streaming_connection()
                await conn.connect()
                await conn.wait_synchronized()

                # Subscribe to market data
                await conn.subscribe_to_market_data(self.symbol)

                # Get initial balance
                ts = conn.terminal_state
                info = ts.account_information
                balance = info.get('equity', 5000 if not vault['is_real'] else 200)

                # Create strategy instance for this vault
                strategy = AggressorPulseStrategy(
                    wallet_name=vault['name'],
                    initial_balance=balance,
                    risk_pct=vault['risk_pct']
                )

                self.connections[vault['id']] = {
                    "conn": conn,
                    "meta": vault,
                    "acc_api": acc,
                    "strategy": strategy
                }

                STATE["strategies"][vault['id']] = strategy

                print(f"✅ {vault['name']} CONNECTED | Balance: ${balance:.2f}")
            except Exception as e:
                print(f"❌ VAULT ERROR {vault['name']}: {e}")

    async def get_candles(self, acc_api, timeframe, hours_back):
        """Fetch historical candles"""
        try:
            start = datetime.now(pytz.utc) - timedelta(hours=hours_back)

            # Calculate expected candles
            if timeframe == '1h':
                expected = hours_back + 5
            elif timeframe == '15m':
                expected = (hours_back * 4) + 5
            elif timeframe == '5m':
                expected = (hours_back * 12) + 5
            else:
                expected = 100

            candles = await acc_api.get_historical_candles(self.symbol, timeframe, start, expected)

            if candles:
                print(f"📊 Fetched {len(candles)} {timeframe} candles")
                return candles
            return []
        except Exception as e:
            print(f"❌ Error fetching {timeframe} candles: {e}")
            return []

    async def analyze_and_trade(self):
        """Main analysis and trading loop"""
        while True:
            try:
                # Update vault information FIRST (always send to frontend)
                v_list = []
                for v_id, data in self.connections.items():
                    ts = data['conn'].terminal_state
                    info = ts.account_information
                    if info and 'equity' in info:
                        # Update strategy balance
                        data['strategy'].balance = info['equity']

                        v_list.append({
                            "name": data['meta']['name'],
                            "is_real": data['meta']['is_real'],
                            "equity": info['equity'],
                            "profit": info['equity'] - info.get('balance', info['equity']),
                            "positions": [{
                                "id": p['id'],
                                "symbol": p['symbol'],
                                "profit": p.get('profit', 0),
                                "type": str(p['type']),
                                "volume": p['volume'],
                                "openPrice": p.get('openPrice', 0)
                            } for p in ts.positions]
                        })

                if v_list:
                    STATE["vaults"] = v_list
                    STATE["ready"] = True  # Mark as ready once we have vault data
                    print(f"💼 Vaults Updated: {len(v_list)} accounts, {sum(len(v['positions']) for v in v_list)} positions")

                # Get live price
                demo_conn = self.connections["77c5fbff-beb8-422a-b085-c135c230a630"]["conn"]
                symbol_price = demo_conn.terminal_state.price(self.symbol)
                live_price = symbol_price.get('bid', 0) if symbol_price else 0

                if live_price == 0:
                    print("⚠️ No live price available")
                    await asyncio.sleep(5)
                    continue

                # Run Aggressor Pulse Analysis
                demo_api = self.connections["77c5fbff-beb8-422a-b085-c135c230a630"]["acc_api"]

                # Fetch multi-timeframe data
                print(f"📡 Fetching candles for analysis... (Live Price: ${live_price:.2f})")

                candles_h1 = await self.get_candles(demo_api, '1h', hours_back=168)  # 7 days
                candles_m15 = await self.get_candles(demo_api, '15m', hours_back=48)  # 2 days
                candles_m5 = await self.get_candles(demo_api, '5m', hours_back=12)   # 12 hours

                if not candles_h1 or not candles_m15 or not candles_m5:
                    print("⚠️ Insufficient candle data - will retry in 30 seconds")
                    STATE["analysis"] = {
                        "type": "HEARTBEAT",
                        "symbol": self.symbol,
                        "price": round(live_price, 2),
                        "decision": "SCANNING",
                        "reason": "Fetching market data...",
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    }
                    await asyncio.sleep(30)
                    continue

                # Generate signal using strategy
                demo_strategy = STATE["strategies"]["77c5fbff-beb8-422a-b085-c135c230a630"]
                timestamp = datetime.now(pytz.utc)
                signal = demo_strategy.generate_signal(candles_h1, candles_m15, candles_m5, timestamp)

                if signal and not signal.get('rejected'):
                    # Valid signal - execute trade
                    print(f"🎯 SIGNAL: {signal['direction']} @ ${signal['entry']:.2f}")
                    print(f"   SL: ${signal['sl']:.2f} | TP: ${signal['tp']:.2f} | RRR: {signal['rrr']:.1f}:1")
                    print(f"   Reason: {signal['reason']}")

                    STATE["analysis"] = {
                        "type": "SIGNAL",
                        "symbol": self.symbol,
                        "price": signal['entry'],
                        "decision": signal['direction'],
                        "sl": signal['sl'],
                        "tp": signal['tp'],
                        "size": signal['lot_size'],
                        "reason": signal['reason'],
                        "timestamp": timestamp.strftime("%H:%M:%S")
                    }

                    # Execute on all vaults
                    await self.execute_trade(signal)

                elif signal and signal.get('rejected'):
                    # Signal rejected
                    print(f"❌ Signal rejected: {signal['reject_reason']}")
                    STATE["analysis"] = {
                        "type": "HEARTBEAT",
                        "symbol": self.symbol,
                        "price": round(live_price, 2),
                        "decision": "SCANNING",
                        "reason": f"Signal rejected: {signal['reject_reason']}",
                        "timestamp": timestamp.strftime("%H:%M:%S")
                    }
                else:
                    # No signal
                    h1_trend = demo_strategy.h1_trend
                    ema10 = demo_strategy.ema10_m15
                    ema20 = demo_strategy.ema20_m15

                    reason_parts = [f"H1 Trend: {h1_trend}"]
                    if ema10 and ema20:
                        reason_parts.append(f"M15 EMA10: ${ema10:.2f} | EMA20: ${ema20:.2f}")
                    reason_parts.append("Waiting for M15 channel + M5 CHoCH")

                    STATE["analysis"] = {
                        "type": "HEARTBEAT",
                        "symbol": self.symbol,
                        "price": round(live_price, 2),
                        "decision": "SCANNING",
                        "reason": " | ".join(reason_parts),
                        "timestamp": timestamp.strftime("%H:%M:%S")
                    }

            except Exception as e:
                print(f"❌ Analysis Loop Error: {e}")
                import traceback
                traceback.print_exc()

            # Update every 10 seconds (vault data updates frequently, analysis only when needed)
            await asyncio.sleep(10)

    async def execute_trade(self, signal):
        """Execute trade on all connected vaults"""
        executed_trades = []

        for v_id, data in self.connections.items():
            try:
                conn = data['conn']
                strategy = data['strategy']

                print(f"💼 Executing on {data['meta']['name']}...")

                if signal['direction'] == "BUY":
                    result = await conn.create_market_buy_order(
                        self.symbol,
                        signal['lot_size'],
                        signal['sl'],
                        signal['tp']
                    )
                else:
                    result = await conn.create_market_sell_order(
                        self.symbol,
                        signal['lot_size'],
                        signal['sl'],
                        signal['tp']
                    )

                print(f"✅ {data['meta']['name']}: {signal['direction']} {signal['lot_size']} lots")

                # Record in strategy
                trade = strategy.execute_trade(signal, datetime.now(pytz.utc))

                executed_trades.append({
                    "vault": data['meta']['name'],
                    "is_real": data['meta']['is_real'],
                    "direction": signal['direction'],
                    "entry": signal['entry'],
                    "sl": signal['sl'],
                    "tp": signal['tp'],
                    "size": signal['lot_size'],
                    "rrr": signal['rrr'],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

            except Exception as e:
                print(f"❌ Execution Error on {data['meta']['name']}: {e}")

        # Add notification
        if executed_trades:
            notification = {
                "type": "TRADE_EXECUTED",
                "signal": signal,
                "trades": executed_trades,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            STATE["trade_notifications"].append(notification)
            STATE["trade_notifications"] = STATE["trade_notifications"][-10:]


# ==========================================
# 🌐 WEBSOCKET SERVER
# ==========================================
async def health_check(path, _request_headers):
    """Handle HTTP health checks from Railway"""
    if path == "/health":
        return (200, [], b"OK\n")
    return None


async def socket_handler(websocket):
    print("🟢 FRONTEND CONNECTED")
    try:
        while True:
            if STATE["ready"]:
                await websocket.send(json.dumps({"type": "MULTI_VAULT_UPDATE", "vaults": STATE["vaults"]}))
                await websocket.send(json.dumps(STATE["analysis"]))

                # Send trade notifications
                if STATE["trade_notifications"]:
                    for notification in STATE["trade_notifications"]:
                        await websocket.send(json.dumps(notification))
                    STATE["trade_notifications"] = []

            await asyncio.sleep(2)
    except websockets.exceptions.ConnectionClosed:
        print("🔴 FRONTEND DISCONNECTED")


async def main():
    print("=" * 60)
    print("🚀 AGGRESSOR PULSE - LIVE TRADING BOT")
    print("=" * 60)
    print(f"Strategy: H1 Bias → M15 EMA Channel → M5 CHoCH")
    print(f"Backtest: +9.55% ROI | 57% Win Rate | 2.82:1 Avg RRR")
    print("=" * 60)

    engine = AggressorPulseLive()
    await engine.connect()

    # Start trading loop
    asyncio.create_task(engine.analyze_and_trade())

    # Start WebSocket server
    async with websockets.serve(
        socket_handler,
        WS_HOST,
        WS_PORT,
        ping_interval=20,
        ping_timeout=10,
        process_request=health_check
    ):
        print(f"🌐 WebSocket Server: ws://{WS_HOST}:{WS_PORT}")
        print("✅ AUTO-TRADING ACTIVE")
        print("=" * 60)
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
