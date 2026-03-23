"""
STRATEGY V4: LAST 7 DAYS BACKTEST
==================================
Test Period: Last 7 days (Dec 23-30, 2025)
Wallets:
  - DEMO: $5,000 (1% risk per trade)
  - REAL: $200 (1% risk per trade)

Purpose: Quick validation of V4 strategy with recent market data
Strategy: V4 Liquidity Sniper (1:1 BE + 1:3 TP + No Filters)
"""

import asyncio
from datetime import datetime, timedelta
import pytz
from metaapi_cloud_sdk import MetaApi
import os
import sys
from dotenv import load_dotenv
import json

# Add parent directory to path to import strategy
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from strategies.strategy_v12_renaissance import StrategyV12

load_dotenv()

META_API_TOKEN = os.getenv('METAAPI_TOKEN')
# Use DEMO account for backtesting (more likely to be available)
ACCOUNT_ID = os.getenv('METAAPI_ACCOUNT_ID', '77c5fbff-beb8-422a-b085-c135c230a630')


class V4Last7DaysBacktest:
    """Run V4 strategy on last 7 days of data"""

    def __init__(self):
        self.demo_wallet = StrategyV12("DEMO", 5000, risk_pct=0.01)
        self.real_wallet = StrategyV12("REAL", 200, risk_pct=0.01)
        self.api_requests = 0

    async def fetch_historical_data(self):
        """Fetch last 7 days of data"""
        print("🔄 Connecting to MetaAPI...")

        api = MetaApi(META_API_TOKEN)
        account = await api.metatrader_account_api.get_account(ACCOUNT_ID)

        if account.state != 'DEPLOYED':
            print(f"⚠️ Deploying account...")
            await account.deploy()

        print("⏳ Waiting for broker connection (timeout: 5 minutes)...")
        try:
            await account.wait_connected(timeout_in_seconds=300)
        except Exception as e:
            print(f"⚠️ Connection timeout - Broker may be closed (weekend/holiday)")
            print(f"💡 Note: Forex markets are closed on weekends")
            raise e

        connection = account.get_streaming_connection()
        await connection.connect()
        await connection.wait_synchronized(timeout_in_seconds=300)

        # Calculate date range (last 7 days)
        end_date = datetime.now(pytz.utc)
        start_date = end_date - timedelta(days=7)

        print(f"✅ Connected! Fetching 7-day data ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})...")

        # Fetch candles for last 7 days
        # 7 days = ~672 15-min candles (96 per day)
        print("📊 Fetching 15-minute candles...")
        candles_15m = await account.get_historical_candles('GOLD.pro', '15m', start_date, 700)
        self.api_requests += 1

        # 7 days = ~168 1-hour candles (24 per day)
        print("📊 Fetching 1-hour candles...")
        candles_1h = await account.get_historical_candles('GOLD.pro', '1h', start_date, 180)
        self.api_requests += 1

        # 7 days = ~42 4-hour candles (6 per day)
        print("📊 Fetching 4-hour candles...")
        candles_4h = await account.get_historical_candles('GOLD.pro', '4h', start_date, 50)
        self.api_requests += 1

        print(f"✅ Data fetched: {len(candles_15m)} 15m, {len(candles_1h)} 1h, {len(candles_4h)} 4h candles")

        await connection.close()

        return {
            '15m': candles_15m,
            '1h': candles_1h,
            '4h': candles_4h
        }

    async def run_backtest(self):
        """Execute dual-wallet backtest on last 7 days"""
        print("\n" + "="*80)
        print("🎯 STRATEGY V4: LAST 7 DAYS BACKTEST")
        print("="*80)

        end_date = datetime.now(pytz.utc)
        start_date = end_date - timedelta(days=7)

        print(f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} (7 days)")
        print("Strategy: V4 Liquidity Sniper (1:1 BE + 1:3 TP + No Filters)")
        print(f"\nVAULT A (DEMO):  Initial: ${self.demo_wallet.balance:,.2f} | Risk: 1% per trade")
        print(f"VAULT B (REAL):  Initial: ${self.real_wallet.balance:,.2f} | Risk: 1% per trade")
        print("="*80 + "\n")

        # Fetch data
        data = await self.fetch_historical_data()

        print("\n🔍 Scanning for liquidity sweeps (V4 logic)...\n")

        candles_15m = data['15m']
        trade_counter = 0

        for i, candle in enumerate(candles_15m):
            timestamp = candle['time'] if isinstance(candle['time'], datetime) else datetime.fromtimestamp(candle['time'], tz=pytz.utc)

            # Prepare data up to current candle
            current_data = {
                '15m': candles_15m[:i+1],
                '1h': [c for c in data['1h'] if c['time'] <= candle['time']],
                '4h': [c for c in data['4h'] if c['time'] <= candle['time']]
            }

            # Generate signal for DEMO wallet
            demo_signal = self.demo_wallet.generate_signal(candle, current_data, timestamp, i)

            # Generate signal for REAL wallet (same logic, different position size)
            real_signal = self.real_wallet.generate_signal(candle, current_data, timestamp, i)

            # Both wallets should get same signals (only lot size differs)
            if demo_signal and real_signal:
                trade_counter += 1
                print(f"🎯 TRADE #{trade_counter}")
                print(f"   Time: {timestamp.strftime('%Y-%m-%d %H:%M UTC')}")
                print(f"   Signal: {demo_signal['decision']} @ ${demo_signal['price']:.2f}")
                print(f"   SL: ${demo_signal['sl']:.2f} | TP: ${demo_signal['tp']:.2f}")
                print(f"   Level: {demo_signal['level']} | Structure: {demo_signal['structure']}")
                print(f"\n   DEMO Lot: {demo_signal['lot_size']} | Risk: ${demo_signal['risk']:.2f}")
                print(f"   REAL Lot: {real_signal['lot_size']} | Risk: ${real_signal['risk']:.2f}\n")

                # Execute trades
                demo_trade = self.demo_wallet.execute_trade(demo_signal, timestamp)
                real_trade = self.real_wallet.execute_trade(real_signal, timestamp)

                # Simulate outcomes
                future_candles = candles_15m[i+1:]
                self.demo_wallet.simulate_trade_outcome(demo_trade, future_candles)
                self.real_wallet.simulate_trade_outcome(real_trade, future_candles)

                # Report outcomes
                if demo_trade['outcome'] in ['WIN', 'LOSS', 'BREAKEVEN']:
                    outcome_emoji = {"WIN": "✅", "LOSS": "❌", "BREAKEVEN": "➖"}[demo_trade['outcome']]
                    be_emoji = " 🔒" if demo_trade['breakeven_moved'] else ""

                    print(f"   {outcome_emoji}{be_emoji} {demo_trade['outcome']}")
                    print(f"   DEMO P&L: ${demo_trade['pnl']:+,.2f} | New Balance: ${self.demo_wallet.balance:,.2f}")
                    print(f"   REAL P&L: ${real_trade['pnl']:+,.2f} | New Balance: ${self.real_wallet.balance:,.2f}")

                    if demo_trade['breakeven_moved']:
                        print(f"   🔒 Breakeven protection activated at 1:1 RR")

                    exit_time = demo_trade['exit_time'] if isinstance(demo_trade['exit_time'], datetime) else datetime.fromtimestamp(demo_trade['exit_time'], tz=pytz.utc)
                    print(f"   Exit: ${demo_trade['exit_price']:.2f} @ {exit_time.strftime('%Y-%m-%d %H:%M UTC')}\n")

        # Generate comprehensive report
        self.generate_report()

    def generate_report(self):
        """Generate 7-day backtest report"""
        print("\n" + "="*80)
        print("📊 STRATEGY V4: LAST 7 DAYS BACKTEST RESULTS")
        print("="*80)

        demo_stats = self.demo_wallet.get_stats()
        real_stats = self.real_wallet.get_stats()

        # VAULT A (DEMO) Results
        print(f"\n{'='*80}")
        print("VAULT A (DEMO $5K)")
        print(f"{'='*80}")
        initial_demo = self.demo_wallet.balance - demo_stats['total_pnl']
        print(f"Initial Balance:      ${initial_demo:,.2f}")
        print(f"Final Balance:        ${self.demo_wallet.balance:,.2f}")
        print(f"Total P&L:            ${demo_stats['total_pnl']:+,.2f}")
        print(f"ROI:                  {(demo_stats['total_pnl'] / initial_demo * 100):+.2f}%")
        print(f"\nTrade Statistics:")
        print(f"  Total Trades:       {demo_stats['total_trades']}")
        print(f"  Wins:               {demo_stats['wins']} ({demo_stats['win_rate']:.1f}%)")
        print(f"  Losses:             {demo_stats['losses']}")
        print(f"  Breakevens:         {demo_stats['breakevens']} ({demo_stats['be_rate']:.1f}%) 🛡️")
        print(f"  Open:               {demo_stats['open']}")
        print(f"  Survival Rate:      {demo_stats['survival_rate']:.1f}% (Win + BE)")
        print(f"\nAverage Metrics:")
        print(f"  Average Win:        ${demo_stats['avg_win']:,.2f}")
        print(f"  Average Loss:       ${demo_stats['avg_loss']:,.2f}")
        if demo_stats['avg_loss'] != 0:
            print(f"  Win/Loss Ratio:     {abs(demo_stats['avg_win'] / demo_stats['avg_loss']):.1f}:1")

        # VAULT B (REAL) Results
        print(f"\n{'='*80}")
        print("VAULT B (REAL $200)")
        print(f"{'='*80}")
        initial_real = self.real_wallet.balance - real_stats['total_pnl']
        print(f"Initial Balance:      ${initial_real:,.2f}")
        print(f"Final Balance:        ${self.real_wallet.balance:,.2f}")
        print(f"Total P&L:            ${real_stats['total_pnl']:+,.2f}")
        print(f"ROI:                  {(real_stats['total_pnl'] / initial_real * 100):+.2f}%")
        print(f"\nTrade Statistics:")
        print(f"  Total Trades:       {real_stats['total_trades']}")
        print(f"  Wins:               {real_stats['wins']} ({real_stats['win_rate']:.1f}%)")
        print(f"  Losses:             {real_stats['losses']}")
        print(f"  Breakevens:         {real_stats['breakevens']} ({real_stats['be_rate']:.1f}%) 🛡️")
        print(f"  Open:               {real_stats['open']}")
        print(f"  Survival Rate:      {real_stats['survival_rate']:.1f}% (Win + BE)")
        print(f"\nAverage Metrics:")
        print(f"  Average Win:        ${real_stats['avg_win']:,.2f}")
        print(f"  Average Loss:       ${real_stats['avg_loss']:,.2f}")
        if real_stats['avg_loss'] != 0:
            print(f"  Win/Loss Ratio:     {abs(real_stats['avg_win'] / real_stats['avg_loss']):.1f}:1")

        # Market Structure Analysis
        print(f"\n{'='*80}")
        print("MARKET STRUCTURE ANALYSIS")
        print(f"{'='*80}")
        self.analyze_structure_performance()

        # Expected vs Actual (7-day scaling)
        print(f"\n{'='*80}")
        print("PERFORMANCE ANALYSIS (7-Day Sample)")
        print(f"{'='*80}")

        expected_trades_7d = int(110 * (7/57))  # Scale from 57-day period

        print(f"\nExpected (scaled from 57-day V4 baseline):")
        print(f"  Trades:             ~{expected_trades_7d} trades")
        print(f"  ROI:                ~+6% to +8% (scaled from +35-45%)")
        print(f"\nActual:")
        print(f"  Trades:             {demo_stats['total_trades']} trades {'✅' if demo_stats['total_trades'] >= expected_trades_7d * 0.5 else '⚠️'}")
        print(f"  ROI (Demo):         {(demo_stats['total_pnl'] / initial_demo * 100):+.2f}% {'✅' if (demo_stats['total_pnl'] / initial_demo * 100) > 0 else '❌'}")
        print(f"  ROI (Real):         {(real_stats['total_pnl'] / initial_real * 100):+.2f}% {'✅' if (real_stats['total_pnl'] / initial_real * 100) > 0 else '❌'}")

        print(f"\n{'='*80}")

        # Save detailed results
        self.save_detailed_report()

    def analyze_structure_performance(self):
        """Analyze if market structure matters"""
        demo_trades = self.demo_wallet.trades

        bullish_trades = [t for t in demo_trades if t['structure'] == 'BULLISH']
        bearish_trades = [t for t in demo_trades if t['structure'] == 'BEARISH']
        neutral_trades = [t for t in demo_trades if t['structure'] == 'NEUTRAL']

        for structure_name, trades in [('BULLISH', bullish_trades), ('BEARISH', bearish_trades), ('NEUTRAL', neutral_trades)]:
            if len(trades) == 0:
                continue

            wins = len([t for t in trades if t['outcome'] == 'WIN'])
            losses = len([t for t in trades if t['outcome'] == 'LOSS'])
            bes = len([t for t in trades if t['outcome'] == 'BREAKEVEN'])

            win_rate = (wins / len(trades) * 100) if len(trades) > 0 else 0
            be_rate = (bes / len(trades) * 100) if len(trades) > 0 else 0

            print(f"\n{structure_name} Structure:")
            print(f"  Total: {len(trades)} | Wins: {wins} ({win_rate:.1f}%) | Losses: {losses} | BE: {bes} ({be_rate:.1f}%)")

    def save_detailed_report(self):
        """Save JSON report for analysis"""
        end_date = datetime.now(pytz.utc)
        start_date = end_date - timedelta(days=7)

        report = {
            "strategy": "V4_LIQUIDITY_SNIPER",
            "test_period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} (7 days)",
            "demo": {
                "initial_balance": self.demo_wallet.balance - self.demo_wallet.get_stats()['total_pnl'],
                "final_balance": self.demo_wallet.balance,
                "stats": self.demo_wallet.get_stats(),
                "trades": self.demo_wallet.trades
            },
            "real": {
                "initial_balance": self.real_wallet.balance - self.real_wallet.get_stats()['total_pnl'],
                "final_balance": self.real_wallet.balance,
                "stats": self.real_wallet.get_stats(),
                "trades": self.real_wallet.trades
            },
            "generated_at": datetime.now(pytz.utc).isoformat()
        }

        filename = "V4_LAST_7D_RESULTS.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        print(f"\n💾 Detailed results saved to {filename}")


async def main():
    backtest = V4Last7DaysBacktest()
    await backtest.run_backtest()


if __name__ == "__main__":
    asyncio.run(main())
