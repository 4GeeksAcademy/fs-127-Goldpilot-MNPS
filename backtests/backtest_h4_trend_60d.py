"""
H4 TREND FOLLOWER: 60-DAY BACKTEST
===================================
Test Period: Last 60 days
Strategy: H4 trend analysis → M15/M30 execution
Trading Hours: 07:00-10:00 + 15:00-18:00 UTC
"""

import asyncio
from datetime import datetime, timedelta
import pytz
from metaapi_cloud_sdk import MetaApi
import os
from dotenv import load_dotenv
from strategy_h4_trend_follower import H4TrendFollower
import json

load_dotenv()

META_API_TOKEN = os.getenv('METAAPI_TOKEN')
ACCOUNT_ID = os.getenv('METAAPI_ACCOUNT_ID', '436348e0-be6e-49cc-a991-8895903e5288')


class H4TrendBacktest:
    """60-Day backtest for H4 Trend Follower strategy"""

    def __init__(self):
        self.demo_wallet = H4TrendFollower("DEMO", 5000, risk_pct=0.01)
        self.real_wallet = H4TrendFollower("REAL", 200, risk_pct=0.01)
        self.api_requests = 0

    async def fetch_historical_data(self):
        """Fetch last 60 days of data"""
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

        print("📊 Fetching H4 candles (analysis timeframe)...")
        candles_h4 = await account.get_historical_candles('GOLD.pro', '4h', start_date, 400)
        self.api_requests += 1

        print("📊 Fetching M30 candles (execution timeframe)...")
        candles_m30 = await account.get_historical_candles('GOLD.pro', '30m', start_date, 3000)
        self.api_requests += 1

        print("📊 Fetching M15 candles (execution timeframe)...")
        candles_m15 = await account.get_historical_candles('GOLD.pro', '15m', start_date, 6000)
        self.api_requests += 1

        print(f"✅ Data fetched: {len(candles_h4)} H4, {len(candles_m30)} M30, {len(candles_m15)} M15 candles\n")

        await connection.close()

        return {
            'h4': candles_h4,
            'm30': candles_m30,
            'm15': candles_m15
        }

    async def run_backtest(self):
        """Execute backtest"""
        print("\n" + "="*80)
        print("🎯 H4 TREND FOLLOWER: 60-DAY BACKTEST")
        print("="*80)
        print("Analysis Timeframe: 4-Hour (H4)")
        print("Execution Timeframes: 15-Min (M15) + 30-Min (M30)")
        print("Trading Hours: 07:00-10:00 + 15:00-18:00 UTC")
        print("Risk: 1% per trade | TP: Before next key level")
        print(f"\nVAULT A (DEMO):  ${self.demo_wallet.balance:,.2f}")
        print(f"VAULT B (REAL):  ${self.real_wallet.balance:,.2f}")
        print("="*80 + "\n")

        # Fetch data
        data = await self.fetch_historical_data()

        print("🔍 Scanning for H4 trend setups...\n")

        candles_m15 = data['m15']
        trade_counter = 0

        # Walk through M15 candles (execution timeframe)
        for i, candle in enumerate(candles_m15):
            timestamp = candle['time'] if isinstance(candle['time'], datetime) else datetime.fromtimestamp(candle['time'], tz=pytz.utc)

            # Get data up to current candle
            current_h4 = [c for c in data['h4'] if c['time'] <= candle['time']]
            current_m30 = [c for c in data['m30'] if c['time'] <= candle['time']]
            current_m15 = candles_m15[:i+1]

            # Need enough history
            if len(current_h4) < 30 or len(current_m30) < 20 or len(current_m15) < 20:
                continue

            # Generate signal for DEMO
            demo_signal = self.demo_wallet.generate_signal(
                current_h4, current_m15, current_m30, timestamp
            )

            # Generate signal for REAL (same logic)
            real_signal = self.real_wallet.generate_signal(
                current_h4, current_m15, current_m30, timestamp
            )

            if demo_signal and real_signal:
                trade_counter += 1
                print(f"🎯 TRADE #{trade_counter}")
                print(f"   Time: {timestamp.strftime('%Y-%m-%d %H:%M UTC')}")
                print(f"   Signal: {demo_signal['direction']} @ ${demo_signal['entry']:.2f}")
                print(f"   SL: ${demo_signal['sl']:.2f} | TP: ${demo_signal['tp']:.2f}")
                print(f"   H4 Trend: {demo_signal['h4_trend']} | Session: {demo_signal['session']}")
                print(f"   Level: {demo_signal['level_used']}")
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
                    print(f"   DEMO P&L: ${demo_trade['pnl']:+,.2f} | Balance: ${self.demo_wallet.balance:,.2f}")
                    print(f"   REAL P&L: ${real_trade['pnl']:+,.2f} | Balance: ${self.real_wallet.balance:,.2f}")

                    if demo_trade['exit_time']:
                        exit_time = demo_trade['exit_time'] if isinstance(demo_trade['exit_time'], datetime) else datetime.fromtimestamp(demo_trade['exit_time'], tz=pytz.utc)
                        print(f"   Exit: ${demo_trade['exit_price']:.2f} @ {exit_time.strftime('%Y-%m-%d %H:%M UTC')}\n")

        # Generate report
        self.generate_report()

    def generate_report(self):
        """Generate detailed report"""
        print("\n" + "="*80)
        print("📊 H4 TREND FOLLOWER: 60-DAY BACKTEST RESULTS")
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
        print(f"  Open:               {demo_stats.get('open', 0)}")
        print(f"\nAverage Metrics:")
        print(f"  Average Win:        ${demo_stats.get('avg_win', 0):,.2f}")
        print(f"  Average Loss:       ${demo_stats.get('avg_loss', 0):,.2f}")
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
        print(f"  Open:               {real_stats.get('open', 0)}")
        print(f"\nAverage Metrics:")
        print(f"  Average Win:        ${real_stats.get('avg_win', 0):,.2f}")
        print(f"  Average Loss:       ${real_stats.get('avg_loss', 0):,.2f}")
        if real_stats.get('avg_loss', 0) != 0:
            ratio = abs(real_stats.get('avg_win', 0) / real_stats.get('avg_loss', 0))
            print(f"  Win/Loss Ratio:     {ratio:.2f}:1")

        # Strategy Analysis
        print(f"\n{'='*80}")
        print("STRATEGY ANALYSIS")
        print(f"{'='*80}")

        # Analyze by H4 trend
        self.analyze_by_trend()

        # Analyze by session
        self.analyze_by_session()

        # Deployment recommendation
        print(f"\n{'='*80}")
        print("DEPLOYMENT RECOMMENDATION")
        print(f"{'='*80}")

        if demo_roi > 10 and demo_stats.get('win_rate', 0) > 40:
            print("✅ STRATEGY VALIDATED - Profitable Performance")
            print(f"\nStrengths:")
            print(f"  - ROI: {demo_roi:.1f}% (Target: >10%)")
            print(f"  - Win Rate: {demo_stats.get('win_rate', 0):.1f}% (Target: >40%)")
            print(f"\nNext Steps:")
            print(f"  1. Deploy to paper trading for 30 days")
            print(f"  2. Monitor live market alignment")
            print(f"  3. If consistent, scale to $1K live account")
        elif demo_roi > 0:
            print("⚠️ MARGINAL PERFORMANCE - Proceed with Caution")
            print(f"\nObservations:")
            print(f"  - ROI: {demo_roi:.1f}% (Below 10% target)")
            print(f"  - Win Rate: {demo_stats.get('win_rate', 0):.1f}%")
            print(f"\nRecommendation:")
            print(f"  - Extend backtest period")
            print(f"  - Review losing trades")
            print(f"  - Test parameter adjustments on separate account")
        else:
            print("❌ STRATEGY FAILED - DO NOT DEPLOY")
            print(f"\nIssues:")
            print(f"  - Negative ROI: {demo_roi:.1f}%")
            print(f"  - Win Rate: {demo_stats.get('win_rate', 0):.1f}%")
            print(f"\nAction:")
            print(f"  - Review H4 trend detection logic")
            print(f"  - Analyze support/resistance level accuracy")
            print(f"  - Consider different timeframe combinations")

        print(f"\n{'='*80}")

        # Save results
        self.save_results()

    def analyze_by_trend(self):
        """Analyze performance by H4 trend"""
        demo_trades = self.demo_wallet.trades

        bullish_trades = [t for t in demo_trades if t.get('h4_trend') == 'BULLISH']
        bearish_trades = [t for t in demo_trades if t.get('h4_trend') == 'BEARISH']

        print(f"\nPerformance by H4 Trend:")
        for trend_name, trades in [('BULLISH', bullish_trades), ('BEARISH', bearish_trades)]:
            if len(trades) == 0:
                continue

            wins = len([t for t in trades if t['outcome'] == 'WIN'])
            losses = len([t for t in trades if t['outcome'] == 'LOSS'])
            win_rate = (wins / len(trades) * 100) if len(trades) > 0 else 0

            print(f"  {trend_name}: {len(trades)} trades | Wins: {wins} ({win_rate:.1f}%) | Losses: {losses}")

    def analyze_by_session(self):
        """Analyze performance by trading session"""
        demo_trades = self.demo_wallet.trades

        london_trades = [t for t in demo_trades if t.get('session') == 'LONDON_MORNING']
        ny_trades = [t for t in demo_trades if t.get('session') == 'NY_AFTERNOON']

        print(f"\nPerformance by Session:")
        for session_name, trades in [('LONDON_MORNING', london_trades), ('NY_AFTERNOON', ny_trades)]:
            if len(trades) == 0:
                continue

            wins = len([t for t in trades if t['outcome'] == 'WIN'])
            losses = len([t for t in trades if t['outcome'] == 'LOSS'])
            win_rate = (wins / len(trades) * 100) if len(trades) > 0 else 0

            print(f"  {session_name}: {len(trades)} trades | Wins: {wins} ({win_rate:.1f}%) | Losses: {losses}")

    def save_results(self):
        """Save JSON results"""
        report = {
            "strategy": "H4_TREND_FOLLOWER",
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

        filename = "H4_TREND_FOLLOWER_RESULTS.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        print(f"\n💾 Detailed results saved to {filename}")


async def main():
    backtest = H4TrendBacktest()
    await backtest.run_backtest()


if __name__ == "__main__":
    asyncio.run(main())
