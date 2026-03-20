import asyncio
import websockets
import json
import pandas as pd
from datetime import datetime, timedelta
import pytz
from metaapi_cloud_sdk import MetaApi
import warnings

warnings.filterwarnings("ignore")

# ==========================================
# 🔐 CONFIGURATION
# ==========================================
META_API_TOKEN = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiIxNzFjZWQ4Yjg5ODdhMWQyM2JlOGFhMTAxM2YwZjVlZCIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiwibWV0aG9kcyI6WyJtZXRhc3RhdHMtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiMTcxY2VkOGI4OTg3YTFkMjNiZThhYTEwMTNmMGY1ZWQiLCJpYXQiOjE3NjY3Mjg2MzEsImV4cCI6MTc3NDUwNDYzMX0.TlcBJs-k1nzfPIaNLcYBHkFlAWnnJ9qa43CV7aFDYxWjVxp_ZkAJRbKhy4MYhStwHMdiDP8SLVf_Zd4Wfns5qvV_HNNCiCoDDLSw8xy02gctQsr6su5ZTYCSRLfscQZDk8mfZuVfj3wKNxAYE68TeyMlBc1oEQyaHJ7AuDDGhlLDmwJINX4hhfHBxvPbdYztW92DQ_mmp9PSuLU_sr0O9NywQyiYEFXFjCl1_C_55qShFE0-_PkvnQNAzy-6-kWnqMt6Q3yiZJH_EusHF92VxVhzPcqsSFEXCK1q9VkNHT1bK9gICvGGTMGUy0qr0O0d_8THdZrSbiZKi8t9QHgYy-O4BBMvUCYIHcyDUoigwHQGJoFm_n1ZEzpunmVCqWhjwpUXKeXwQebwdJ0OHyH3bW59Z-NT-Snk70-6oHseEpjd45zBiN8pMClVhXc1DvpMiPFnXmQ4hmSmTnskdAOakXhKbx3VRt4EwRbs8-_Pupp824Q0k852X7VODZ2owKX9gZHjjOKuIG3ZlNztj6StEwb_lDzuEc3r8BNNtntZW8UBkBy9T11lj1mry0SzxsP-NSUGUnfxCtqlXgMBni1uhnyY_JtadDMtXsZ9QDiF3Way8HyBhnE4DBD7-UcsHHQobSRpyyhTYqF8bH4pjmO-Mh1IqVJLLZkZi7NJ0RNCgNk"

VAULTS = [
    {"id": "77c5fbff-beb8-422a-b085-c135c230a630", "name": "QUANT_DEMO", "is_real": False, "risk_pct": 0.02},
    {"id": "436348e0-be6e-49cc-a991-8895903e5288", "name": "MICRO_REAL", "is_real": True, "risk_pct": 0.01}
]

STATE = {
    "vaults": [],
    "analysis": {"type": "HEARTBEAT", "symbol": "GOLD.pro", "price": 0, "decision": "INIT", "reason": "System Booting..."},
    "chart_data": [],
    "ready": False
}

class AurumEngine:
    def __init__(self):
        self.api = MetaApi(META_API_TOKEN)
        self.connections = {}

    async def connect(self):
        for vault in VAULTS:
            try:
                acc = await self.api.metatrader_account_api.get_account(vault['id'])
                if acc.state == 'UNDEPLOYED': await acc.deploy()
                await acc.wait_connected()
                conn = acc.get_streaming_connection()
                await conn.connect()
                await conn.wait_synchronized()
                # Subscribe to GOLD.pro quotes for real-time prices
                await conn.subscribe_to_market_data("GOLD.pro")
                self.connections[vault['id']] = {"conn": conn, "meta": vault, "acc_api": acc}
                print(f"✅ VAULT SYNCED: {vault['name']}")
            except Exception as e: print(f"❌ VAULT ERROR {vault['name']}: {e}")

    async def execute_all(self, signal):
        for v_id, data in self.connections.items():
            try:
                conn = data['conn']
                ts = conn.terminal_state.account_information
                if ts:
                    equity = ts.get('equity', 50)
                    risk_amt = equity * data['meta']['risk_pct']
                    sl_dist = max(0.5, abs(signal['price'] - signal['sl']))
                    size = max(0.01, round(risk_amt / (sl_dist * 100), 2))
                    if signal['decision'] == "BUY":
                        await conn.create_market_buy_order("GOLD.pro", size, signal['sl'], signal['tp'])
                    else:
                        await conn.create_market_sell_order("GOLD.pro", size, signal['sl'], signal['tp'])
            except Exception as e: print(f"Order Failure: {e}")

    async def run_hunt(self):
        while True:
            try:
                v_list = []
                for v_id, data in self.connections.items():
                    ts = data['conn'].terminal_state
                    info = ts.account_information
                    if info and 'equity' in info:
                        v_list.append({
                            "name": data['meta']['name'], "is_real": data['meta']['is_real'],
                            "equity": info['equity'], "profit": info['equity'] - info.get('balance', info['equity']),
                            "positions": [{"id": p['id'], "symbol": p['symbol'], "profit": p.get('profit', 0), "type": str(p['type']), "volume": p['volume'], "openPrice": p.get('openPrice', 0)} for p in ts.positions]
                        })
                if v_list: STATE["vaults"] = v_list

                if "77c5fbff-beb8-422a-b085-c135c230a630" in self.connections:
                    demo_conn = self.connections["77c5fbff-beb8-422a-b085-c135c230a630"]["conn"]
                    demo_api = self.connections["77c5fbff-beb8-422a-b085-c135c230a630"]["acc_api"]

                    # Get real-time price from terminal state
                    symbol_price = demo_conn.terminal_state.price("GOLD.pro")
                    live_price = symbol_price.get('bid', 0) if symbol_price else 0

                    start = datetime.now(pytz.utc) - timedelta(hours=12)
                    gold_c = await demo_api.get_historical_candles("GOLD.pro", '15m', start, 100)

                    if gold_c:
                        df = pd.DataFrame(gold_c)
                        chart_list = []
                        for c in gold_c:
                            # MetaApi returns UTC datetime strings - convert properly to Unix timestamp
                            dt = pd.to_datetime(c['time'])
                            if dt.tzinfo is None:
                                dt = dt.tz_localize('UTC')
                            unix_ts = int(dt.timestamp())
                            chart_list.append({"time": unix_ts, "open": c['open'], "high": c['high'], "low": c['low'], "close": c['close']})
                        STATE["chart_data"] = chart_list

                        # Use live price if available, otherwise use last candle close
                        curr = live_price if live_price > 0 else df['close'].iloc[-1]
                        hi, lo = df['high'].max(), df['low'].min()
                        trigger = hi - (hi - lo) * 0.382
                        signal, sl, tp = "WAIT", 0, 0

                        if curr <= trigger:
                            sl, tp = curr - 5.0, hi
                            if (tp - curr) / (curr - sl) >= 3.0: signal = "BUY"

                        STATE["analysis"] = {
                            "type": "SIGNAL" if signal != "WAIT" else "HEARTBEAT",
                            "symbol": "GOLD.pro", "price": round(curr, 2), "decision": signal if signal != "WAIT" else "SCANNING",
                            "sl": round(sl, 2), "tp": round(tp, 2), "size": 0.25,
                            "reason": f"RRR Analysis: {round((tp-curr)/(curr-sl),1) if sl!=tp else 0} | Live Bid: ${live_price:.2f}",
                            "timestamp": datetime.now().strftime("%H:%M:%S")
                        }
                        print(f"📊 Live Price: ${live_price:.2f} | Candle Close: ${df['close'].iloc[-1]:.2f}")
                        STATE["ready"] = True
            except Exception as e: print(f"Loop Lag: {e}")
            await asyncio.sleep(5)

async def socket_handler(websocket):
    print("🟢 COMMANDER JOINED")
    try:
        while True:
            if STATE["ready"]:
                await websocket.send(json.dumps({"type": "MULTI_VAULT_UPDATE", "vaults": STATE["vaults"]}))
                await websocket.send(json.dumps(STATE["analysis"]))
                if STATE["chart_data"]:
                    await websocket.send(json.dumps({"type": "CHART_UPDATE", "data": STATE["chart_data"]}))
            await asyncio.sleep(2)
    except websockets.exceptions.ConnectionClosed:
        print("🔴 COMMANDER LEFT")

async def main():
    engine = AurumEngine()
    await engine.connect()
    asyncio.create_task(engine.run_hunt())
    async with websockets.serve(socket_handler, "localhost", 8080, ping_interval=20, ping_timeout=10):
        print("🚀 WebSocket Server Running on ws://localhost:8080")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())