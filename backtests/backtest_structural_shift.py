"""
STRUCTURAL SHIFT STRATEGY: 60-DAY BACKTEST
==========================================
Architect: Senior Quantitative Developer
Asset: XAUUSD (Gold)
Period: Last 60 Days
Logic: H4 Structural Shifts → M15 Retest Execution

Expected Profile:
- Win Rate: 20-30%
- Average RRR: 1:5 to 1:10
- Strategy Type: Structural Sniper (Low Frequency, High Conviction)
"""

import asyncio
from datetime import datetime, timedelta
import pytz
from metaapi_cloud_sdk import MetaApi
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(parent_dir))

from dotenv import load_dotenv
from strategies.golden_ratio_strategy import GoldenRatioStrategy
import json

load_dotenv()

META_API_TOKEN = os.getenv('METAAPI_TOKEN')
ACCOUNT_ID = os.getenv('METAAPI_ACCOUNT_ID', '436348e0-be6e-49cc-a991-8895903e5288')


class StructuralShiftBacktest:
    """60-Day backtest for Structural Shift Strategy"""

    def __init__(self):
        self.demo_wallet = GoldenRatioStrategy("DEMO", 5000, risk_pct=0.01, min_lot=0.01)
        self.real_wallet = GoldenRatioStrategy("REAL", 200, risk_pct=0.01, min_lot=0.01)
        self.api_requests = 0
        self.rejected_signals = []  # Track RR-filtered trades

    async def fetch_historical_data(self):
        """Fetch last 60 days of H4 and M15 data"""
        print("🔄 Connecting to MetaAPI...")

        api = MetaApi(META_API_TOKEN)
        account = await api.metatrader_account_api.get_account(ACCOUNT_ID)

        if account.state != 'DEPLOYED':
            print(f"⚠️ Deploying account...")
            await account.deploy()

        print("⏳ Waiting for broker connection...")
        await account.wait_connected()

        connection = account.get_streaming_connection()
        await connection.connect()
        await connection.wait_synchronized()

        print("✅ Connected! Fetching 60-day data...")

        # Last 60 days
        start_date = datetime.now(pytz.utc) - timedelta(days=60)

        print("📊 Fetching H4 candles (Sovereign Structure)...")
        candles_h4 = await account.get_historical_candles('GOLD.pro', '4h', start_date, 400)
        self.api_requests += 1

        print("📊 Fetching M15 candles (Execution Timeframe)...")
        candles_m15 = await account.get_historical_candles('GOLD.pro', '15m', start_date, 6000)
        self.api_requests += 1

        print(f"✅ Data fetched: {len(candles_h4)} H4, {len(candles_m15)} M15 candles\n")

        await connection.close()

        return {
            'h4': candles_h4,
            'm15': candles_m15
        }

    async def run_backtest(self):
        """Execute backtest"""
        print("\n" + "="*80)
        print("🎯 GOLDEN RATIO STRATEGY: 60-DAY BACKTEST")
        print("="*80)
        print("Senior Quantitative Developer - Production Ready")
        print("Asset: XAUUSD (Gold)")
        print("Logic: H4 Trend Engine → M15 Early Entry → Golden Ratio Filter")
        print("\nKey Features:")
        print("  - Minimum 1:3 RR Filter (No more 0.1 RR trades!)")
        print("  - M15 Early Entry (Catches session opens)")
        print("  - Hard 20:00 UTC Exit (No overnight)")
        print("  - Expected: 30-50% win rate, 3-5:1 average RR\n")
        print(f"VAULT A (DEMO):  ${self.demo_wallet.balance:,.2f}")
        print(f"VAULT B (REAL):  ${self.real_wallet.balance:,.2f}")
        print("="*80 + "\n")

        # Fetch data
        data = await self.fetch_historical_data()

        print("🔍 Scanning for structural shift setups...\n")

        candles_m15 = data['m15']
        trade_counter = 0

        # Walk through M15 candles
        for i, candle in enumerate(candles_m15):
            timestamp = candle['time'] if isinstance(candle['time'], datetime) else datetime.fromtimestamp(candle['time'], tz=pytz.utc)

            # Get data up to current candle
            current_h4 = [c for c in data['h4'] if c['time'] <= candle['time']]
            current_m15 = candles_m15[:i+1]

            # Need enough history
            if len(current_h4) < 30 or len(current_m15) < 20:
                continue

            # Generate signals for both wallets
            demo_signal = self.demo_wallet.generate_signal(current_h4, current_m15, timestamp)
            real_signal = self.real_wallet.generate_signal(current_h4, current_m15, timestamp)

            # Track rejected signals
            if demo_signal and demo_signal.get('rejected'):
                self.rejected_signals.append({
                    'timestamp': timestamp,
                    'reason': demo_signal.get('reject_reason'),
                    'rrr': demo_signal.get('rrr', 0)
                })
                continue

            if demo_signal and real_signal:
                trade_counter += 1
                print(f"🎯 TRADE #{trade_counter}")
                print(f"   Time: {timestamp.strftime('%Y-%m-%d %H:%M UTC')}")
                print(f"   Signal: {demo_signal['direction']} @ ${demo_signal['entry']:.2f}")
                print(f"   SL: ${demo_signal['sl']:.2f} | TP: ${demo_signal['tp']:.2f}")
                print(f"   RRR: {demo_signal['rrr']:.1f}:1 | Risk: ${demo_signal['risk']:.2f}")
                print(f"   H4 Trend: {demo_signal['h4_trend']} | Session: {demo_signal['session']}")
                print(f"   Supply Zone: {demo_signal.get('supply_zone', 'N/A')}")
                print(f"   Target Type: {demo_signal.get('target_type', 'N/A')}")
                print(f"\n   DEMO Lot: {demo_signal['lot_size']} | Risk: ${demo_signal['risk']:.2f}")
                print(f"   REAL Lot: {real_signal['lot_size']} | Risk: ${real_signal['risk']:.2f}\n")

                # Execute trades
                demo_trade = self.demo_wallet.execute_trade(demo_signal, timestamp)
                real_trade = self.real_wallet.execute_trade(real_signal, timestamp)

                # Simulate outcomes
                future_candles = candles_m15[i+1:]
                self.demo_wallet.simulate_trade_outcome(demo_trade, future_candles)
                self.real_wallet.simulate_trade_outcome(real_trade, future_candles)

                # Report outcomes
                if demo_trade['outcome'] in ['WIN', 'LOSS']:
                    outcome_emoji = {"WIN": "✅", "LOSS": "❌"}[demo_trade['outcome']]

                    print(f"   {outcome_emoji} {demo_trade['outcome']}")
                    print(f"   Exit Reason: {demo_trade.get('exit_reason', 'N/A')}")
                    print(f"   DEMO P&L: ${demo_trade['pnl']:+,.2f} | Balance: ${self.demo_wallet.balance:,.2f}")
                    print(f"   REAL P&L: ${real_trade['pnl']:+,.2f} | Balance: ${self.real_wallet.balance:,.2f}")

                    if demo_trade['exit_time']:
                        exit_time = demo_trade['exit_time'] if isinstance(demo_trade['exit_time'], datetime) else datetime.fromtimestamp(demo_trade['exit_time'], tz=pytz.utc)
                        print(f"   Exit: ${demo_trade['exit_price']:.2f} @ {exit_time.strftime('%Y-%m-%d %H:%M UTC')}")
                        print(f"   Actual RRR: {abs(demo_trade['pnl'] / (demo_trade['risk'] * demo_trade['lot_size'] * 10)):.2f}:1\n")

                elif demo_trade['outcome'] == 'TIME_STOP':
                    print(f"   ⏰ TIME_STOP (EOD 20:00 UTC)")
                    print(f"   Exit Reason: {demo_trade.get('exit_reason', 'N/A')}")
                    print(f"   DEMO P&L: ${demo_trade['pnl']:+,.2f} | Balance: ${self.demo_wallet.balance:,.2f}")
                    print(f"   REAL P&L: ${real_trade['pnl']:+,.2f} | Balance: ${self.real_wallet.balance:,.2f}")

                    if demo_trade['exit_time']:
                        exit_time = demo_trade['exit_time'] if isinstance(demo_trade['exit_time'], datetime) else datetime.fromtimestamp(demo_trade['exit_time'], tz=pytz.utc)
                        print(f"   Exit: ${demo_trade['exit_price']:.2f} @ {exit_time.strftime('%Y-%m-%d %H:%M UTC')}\n")

            elif demo_signal and not real_signal:
                # Real wallet gated the trade (risk too high)
                print(f"⚠️ TRADE GATED (Real Wallet)")
                print(f"   Time: {timestamp.strftime('%Y-%m-%d %H:%M UTC')}")
                print(f"   Reason: $200 wallet - SL too wide (>5% risk at 0.01 lot)\n")

        # Generate report
        self.generate_report()

    def generate_report(self):
        """Generate detailed report"""
        print("\n" + "="*80)
        print("📊 STRUCTURAL SHIFT STRATEGY: 60-DAY BACKTEST RESULTS")
        print("="*80)

        demo_stats = self.demo_wallet.get_stats()
        real_stats = self.real_wallet.get_stats()

        # VAULT A (DEMO)
        print(f"\n{'='*80}")
        print("VAULT A (DEMO $5K)")
        print(f"{'='*80}")
        demo_initial = 5000
        demo_final = self.demo_wallet.balance
        demo_pnl = demo_stats.get('total_pnl', 0)
        demo_roi = (demo_pnl / demo_initial * 100) if demo_initial > 0 else 0

        print(f"Initial Balance:      ${demo_initial:,.2f}")
        print(f"Final Balance:        ${demo_final:,.2f}")
        print(f"Total P&L:            ${demo_pnl:+,.2f}")
        print(f"ROI:                  {demo_roi:+.2f}%")
        print(f"\nTrade Statistics:")
        print(f"  Total Trades:       {demo_stats.get('total_trades', 0)}")
        print(f"  Wins:               {demo_stats.get('wins', 0)} ({demo_stats.get('win_rate', 0):.1f}%)")
        print(f"  Losses:             {demo_stats.get('losses', 0)}")
        print(f"  Time Stops:         {demo_stats.get('time_stops', 0)}")
        print(f"  Open:               {demo_stats.get('open', 0)}")
        print(f"\nRisk Metrics:")
        print(f"  Average Win:        ${demo_stats.get('avg_win', 0):,.2f}")
        print(f"  Average Loss:       ${demo_stats.get('avg_loss', 0):,.2f}")
        print(f"  Average RRR:        {demo_stats.get('avg_rrr', 0):.2f}:1")
        if demo_stats.get('avg_loss', 0) != 0:
            ratio = abs(demo_stats.get('avg_win', 0) / demo_stats.get('avg_loss', 0))
            print(f"  Win/Loss Ratio:     {ratio:.2f}:1")

        # VAULT B (REAL)
        print(f"\n{'='*80}")
        print("VAULT B (REAL $200)")
        print(f"{'='*80}")
        real_initial = 200
        real_final = self.real_wallet.balance
        real_pnl = real_stats.get('total_pnl', 0)
        real_roi = (real_pnl / real_initial * 100) if real_initial > 0 else 0

        print(f"Initial Balance:      ${real_initial:,.2f}")
        print(f"Final Balance:        ${real_final:,.2f}")
        print(f"Total P&L:            ${real_pnl:+,.2f}")
        print(f"ROI:                  {real_roi:+.2f}%")
        print(f"\nTrade Statistics:")
        print(f"  Total Trades:       {real_stats.get('total_trades', 0)}")
        print(f"  Wins:               {real_stats.get('wins', 0)} ({real_stats.get('win_rate', 0):.1f}%)")
        print(f"  Losses:             {real_stats.get('losses', 0)}")
        print(f"  Time Stops:         {real_stats.get('time_stops', 0)}")
        print(f"  Open:               {real_stats.get('open', 0)}")
        print(f"\nRisk Metrics:")
        print(f"  Average Win:        ${real_stats.get('avg_win', 0):,.2f}")
        print(f"  Average Loss:       ${real_stats.get('avg_loss', 0):,.2f}")
        print(f"  Average RRR:        {real_stats.get('avg_rrr', 0):.2f}:1")
        if real_stats.get('avg_loss', 0) != 0:
            ratio = abs(real_stats.get('avg_win', 0) / real_stats.get('avg_loss', 0))
            print(f"  Win/Loss Ratio:     {ratio:.2f}:1")

        # Golden Ratio Filter Analysis
        print(f"\n{'='*80}")
        print("GOLDEN RATIO FILTER ANALYSIS")
        print(f"{'='*80}")
        print(f"\nRejected Signals (RR < 3.0:1):")
        print(f"  Total Rejected:     {len(self.rejected_signals)}")
        if self.rejected_signals:
            avg_rejected_rr = sum(s['rrr'] for s in self.rejected_signals) / len(self.rejected_signals)
            print(f"  Average RR:         {avg_rejected_rr:.2f}:1")
            print(f"\nFilter saved you from {len(self.rejected_signals)} low-RR trades!")

        # Strategy Validation
        print(f"\n{'='*80}")
        print("STRATEGY VALIDATION")
        print(f"{'='*80}")

        if demo_stats.get('avg_rrr', 0) >= 5.0 and demo_roi > 0:
            print("✅ STRUCTURAL SHIFT LOGIC VALIDATED")
            print(f"\nKey Metrics:")
            print(f"  - Average RRR: {demo_stats.get('avg_rrr', 0):.1f}:1 (Target: >5:1)")
            print(f"  - Win Rate: {demo_stats.get('win_rate', 0):.1f}% (Expected: 20-30%)")
            print(f"  - ROI: {demo_roi:.1f}%")
            print(f"\nConclusion:")
            print(f"  High RRR compensates for low win rate - asymmetric edge confirmed")
        else:
            print("⚠️ STRATEGY NEEDS REFINEMENT")
            print(f"\nObservations:")
            print(f"  - Average RRR: {demo_stats.get('avg_rrr', 0):.1f}:1")
            print(f"  - Win Rate: {demo_stats.get('win_rate', 0):.1f}%")
            print(f"  - ROI: {demo_roi:.1f}%")

        print(f"\n{'='*80}")

        # Save results
        self.save_results()

    def save_results(self):
        """Save JSON results"""
        report = {
            "strategy": "STRUCTURAL_SHIFT",
            "test_period": "Last 60 days",
            "demo": {
                "initial_balance": 5000,
                "final_balance": self.demo_wallet.balance,
                "stats": self.demo_wallet.get_stats(),
                "trades": self.demo_wallet.trades
            },
            "real": {
                "initial_balance": 200,
                "final_balance": self.real_wallet.balance,
                "stats": self.real_wallet.get_stats(),
                "trades": self.real_wallet.trades
            },
            "generated_at": datetime.now(pytz.utc).isoformat()
        }

        filename = "STRUCTURAL_SHIFT_RESULTS.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        print(f"\n💾 Detailed results saved to {filename}")


async def main():
    backtest = StructuralShiftBacktest()
    await backtest.run_backtest()


if __name__ == "__main__":
    asyncio.run(main())
