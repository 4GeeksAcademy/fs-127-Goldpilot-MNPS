"""
STRATEGY V12: DUAL-WALLET BACKTEST
===================================
Test Period: Nov 1 - Dec 27, 2025 (57 days - matching V4)
Wallets:
  - DEMO: $5,000 (1% risk per trade)
  - REAL: $200 (1% risk per trade)

Purpose: Validate V12 (V4 revival) against V4 baseline
Expected: +35-45% ROI, 35-45% BE rate, 5-7% win rate
"""

import asyncio
from datetime import datetime, timedelta
import pytz
from metaapi_cloud_sdk import MetaApi
import os
from dotenv import load_dotenv
from strategy_v12_renaissance import StrategyV12
import json

load_dotenv()

META_API_TOKEN = os.getenv('METAAPI_TOKEN')
ACCOUNT_ID = os.getenv('METAAPI_ACCOUNT_ID', '436348e0-be6e-49cc-a991-8895903e5288')


class V12DualWalletBacktest:
    """Run V12 strategy on two wallets simultaneously"""

    def __init__(self):
        self.demo_wallet = StrategyV12("DEMO", 5000, risk_pct=0.01)
        self.real_wallet = StrategyV12("REAL", 200, risk_pct=0.01)
        self.api_requests = 0

    async def fetch_historical_data(self):
        """Fetch Nov 1 - Dec 27, 2025 (matching V4 test period)"""
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

        print("✅ Connected! Fetching 57-day data (Nov 1 - Dec 27)...")

        # Nov 1 - Dec 27, 2025 (57 days - SAME as V4)
        start_date = datetime(2025, 11, 1, 0, 0, 0, tzinfo=pytz.utc)

        print("📊 Fetching 15-minute candles...")
        candles_15m = await account.get_historical_candles('GOLD.pro', '15m', start_date, 5800)
        self.api_requests += 1

        print("📊 Fetching 1-hour candles...")
        candles_1h = await account.get_historical_candles('GOLD.pro', '1h', start_date, 1450)
        self.api_requests += 1

        print("📊 Fetching 4-hour candles...")
        candles_4h = await account.get_historical_candles('GOLD.pro', '4h', start_date, 400)
        self.api_requests += 1

        print(f"✅ Data fetched: {len(candles_15m)} 15m, {len(candles_1h)} 1h, {len(candles_4h)} 4h candles")

        await connection.close()

        return {
            '15m': candles_15m,
            '1h': candles_1h,
            '4h': candles_4h
        }

    async def run_backtest(self):
        """Execute dual-wallet backtest"""
        print("\n" + "="*80)
        print("🎯 STRATEGY V12: DUAL-WALLET BACKTEST")
        print("="*80)
        print("Period: Nov 1 - Dec 27, 2025 (57 days - MATCHING V4)")
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
        """Generate V12 validation report"""
        print("\n" + "="*80)
        print("📊 STRATEGY V12: DUAL-WALLET BACKTEST RESULTS")
        print("="*80)

        demo_stats = self.demo_wallet.get_stats()
        real_stats = self.real_wallet.get_stats()

        # VAULT A (DEMO) Results
        print(f"\n{'='*80}")
        print("VAULT A (DEMO $5K)")
        print(f"{'='*80}")
        print(f"Initial Balance:      ${self.demo_wallet.balance - demo_stats['total_pnl']:,.2f}")
        print(f"Final Balance:        ${self.demo_wallet.balance:,.2f}")
        print(f"Total P&L:            ${demo_stats['total_pnl']:+,.2f}")
        print(f"ROI:                  {(demo_stats['total_pnl'] / (self.demo_wallet.balance - demo_stats['total_pnl']) * 100):+.2f}%")
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
        print(f"Initial Balance:      ${self.real_wallet.balance - real_stats['total_pnl']:,.2f}")
        print(f"Final Balance:        ${self.real_wallet.balance:,.2f}")
        print(f"Total P&L:            ${real_stats['total_pnl']:+,.2f}")
        print(f"ROI:                  {(real_stats['total_pnl'] / (self.real_wallet.balance - real_stats['total_pnl']) * 100):+.2f}%")
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

        # V12 vs V4 Comparison
        print(f"\n{'='*80}")
        print("V12 VALIDATION AGAINST V4 BASELINE")
        print(f"{'='*80}")
        print(f"\nMetric                  | V4 Target    | V12 Demo     | V12 Real     | Status")
        print(f"{'-'*80}")
        print(f"ROI                     | +35% to +45% | {(demo_stats['total_pnl'] / (self.demo_wallet.balance - demo_stats['total_pnl']) * 100):+.2f}%      | {(real_stats['total_pnl'] / (self.real_wallet.balance - real_stats['total_pnl']) * 100):+.2f}%      | {'✅' if (demo_stats['total_pnl'] / (self.demo_wallet.balance - demo_stats['total_pnl']) * 100) > 30 else '⚠️'}")
        print(f"Win Rate                | 5-7%         | {demo_stats['win_rate']:.1f}%        | {real_stats['win_rate']:.1f}%        | {'✅' if 4 <= demo_stats['win_rate'] <= 10 else '⚠️'}")
        print(f"BE Rate                 | 35-45%       | {demo_stats['be_rate']:.1f}%       | {real_stats['be_rate']:.1f}%       | {'✅' if demo_stats['be_rate'] >= 30 else '⚠️'}")
        print(f"Survival Rate           | >45%         | {demo_stats['survival_rate']:.1f}%       | {real_stats['survival_rate']:.1f}%       | {'✅' if demo_stats['survival_rate'] >= 40 else '⚠️'}")
        print(f"Total Trades            | 100-120      | {demo_stats['total_trades']}         | {real_stats['total_trades']}         | {'✅' if demo_stats['total_trades'] >= 80 else '⚠️'}")

        # Market Structure Analysis (V12 Enhancement)
        print(f"\n{'='*80}")
        print("V12 ENHANCEMENT: MARKET STRUCTURE ANALYSIS")
        print(f"{'='*80}")
        self.analyze_structure_performance()

        # Deployment Recommendation
        print(f"\n{'='*80}")
        print("DEPLOYMENT RECOMMENDATION")
        print(f"{'='*80}")

        demo_roi = (demo_stats['total_pnl'] / (self.demo_wallet.balance - demo_stats['total_pnl']) * 100)
        real_roi = (real_stats['total_pnl'] / (self.real_wallet.balance - real_stats['total_pnl']) * 100)

        if demo_roi > 30 and demo_stats['be_rate'] > 30 and demo_stats['survival_rate'] > 40:
            print("✅ V12 VALIDATED - Ready for Phase 2 (Paper Trading)")
            print(f"\nNext Steps:")
            print(f"  1. Deploy to MetaAPI demo account ($10K)")
            print(f"  2. Run for 60 days (expect 100+ trades)")
            print(f"  3. If ROI >+30% and BE rate >30%, proceed to Phase 3 (Micro-Live)")
        elif demo_roi > 15 and demo_stats['be_rate'] > 25:
            print("⚠️ V12 PARTIAL VALIDATION - Acceptable but below target")
            print(f"\nRecommendation:")
            print(f"  - Review losing trades for patterns")
            print(f"  - Extend backtest period for more data")
            print(f"  - Proceed with caution to paper trading")
        else:
            print("❌ V12 FAILED VALIDATION - DO NOT DEPLOY")
            print(f"\nIssues:")
            if demo_roi < 15:
                print(f"  - ROI too low ({demo_roi:.1f}% vs 35% target)")
            if demo_stats['be_rate'] < 25:
                print(f"  - BE rate too low ({demo_stats['be_rate']:.1f}% vs 35% target)")
            if demo_stats['survival_rate'] < 40:
                print(f"  - Survival rate too low ({demo_stats['survival_rate']:.1f}% vs 45% target)")
            print(f"\nAction: Debug code, verify data source, check for bugs")

        print(f"\n{'='*80}")

        # Save detailed results
        self.save_detailed_report()

    def analyze_structure_performance(self):
        """V12 Enhancement: Analyze if market structure matters"""
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
        report = {
            "strategy": "V12_RENAISSANCE",
            "test_period": "2025-11-01 to 2025-12-27 (57 days - matching V4)",
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

        filename = "STRATEGY_V12_RESULTS.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        print(f"\n💾 Detailed results saved to {filename}")


async def main():
    backtest = V12DualWalletBacktest()
    await backtest.run_backtest()


if __name__ == "__main__":
    asyncio.run(main())
