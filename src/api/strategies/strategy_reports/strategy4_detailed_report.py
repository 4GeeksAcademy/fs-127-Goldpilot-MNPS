#!/usr/bin/env python3
"""
Strategy #4: Aurum Liquidity Sniper - DETAILED TRADE ANALYSIS
Generates comprehensive report with every trade detail for manual review
"""

from datetime import datetime, timedelta
import pytz
import os
from dotenv import load_dotenv
from twelvedata import TDClient
import time
import json

load_dotenv()

TWELVEDATA_API_KEY = os.getenv('TWELVEDATA_API_KEY')
INITIAL_BALANCE = 10000
RISK_PER_TRADE = 0.01
RISK_REWARD_RATIO = 3.0
ATR_MULTIPLIER = 1.5
MAX_TRADES_PER_DAY = 4

class DetailedStrategy4Report:
    def __init__(self):
        self.balance = INITIAL_BALANCE
        self.trades = []
        self.trades_today = 0
        self.current_date = None

    def fetch_data_twelvedata(self):
        """Fetch 60 days of Gold data from Twelve Data"""
        print("="*80)
        print("📊 FETCHING HISTORICAL DATA FOR DETAILED ANALYSIS")
        print("="*80)

        if not TWELVEDATA_API_KEY:
            print("\n❌ ERROR: TWELVEDATA_API_KEY not found in .env")
            return None

        td = TDClient(apikey=TWELVEDATA_API_KEY)

        try:
            print("\n📈 Fetching 15-minute candles...")
            ts_15m = td.time_series(
                symbol="XAU/USD",
                interval="15min",
                outputsize=5000,
                timezone="UTC"
            )
            df_15m = ts_15m.as_pandas()
            candles_15m = self.convert_df_to_candles(df_15m)
            print(f"   ✅ Received {len(candles_15m)} candles")
            time.sleep(8)

            print("📈 Fetching 1-hour candles...")
            ts_1h = td.time_series(
                symbol="XAU/USD",
                interval="1h",
                outputsize=2000,
                timezone="UTC"
            )
            df_1h = ts_1h.as_pandas()
            candles_1h = self.convert_df_to_candles(df_1h)
            print(f"   ✅ Received {len(candles_1h)} candles")
            time.sleep(8)

            print("📈 Fetching 4-hour candles...")
            ts_4h = td.time_series(
                symbol="XAU/USD",
                interval="4h",
                outputsize=500,
                timezone="UTC"
            )
            df_4h = ts_4h.as_pandas()
            candles_4h = self.convert_df_to_candles(df_4h)
            print(f"   ✅ Received {len(candles_4h)} candles")

            # Filter to Nov 1 - Dec 27, 2025
            start_date = datetime(2025, 11, 1, tzinfo=pytz.utc)
            end_date = datetime(2025, 12, 27, 23, 59, 59, tzinfo=pytz.utc)

            candles_15m_filtered = [c for c in candles_15m if start_date <= c['time'] <= end_date]
            candles_1h_filtered = [c for c in candles_1h if start_date <= c['time'] <= end_date]
            candles_4h_filtered = [c for c in candles_4h if start_date <= c['time'] <= end_date]

            print(f"\n✅ DATA LOADED: {len(candles_15m_filtered)} 15m candles")
            print("="*80 + "\n")

            return {
                '15m': candles_15m_filtered,
                '1h': candles_1h_filtered,
                '4h': candles_4h_filtered
            }

        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return None

    def convert_df_to_candles(self, df):
        """Convert Twelve Data pandas dataframe to candle format"""
        candles = []
        df_sorted = df.sort_index()

        for index, row in df_sorted.iterrows():
            if isinstance(index, str):
                timestamp = datetime.strptime(index, '%Y-%m-%d %H:%M:%S')
                timestamp = pytz.utc.localize(timestamp)
            else:
                timestamp = index.to_pydatetime()
                if timestamp.tzinfo is None:
                    timestamp = pytz.utc.localize(timestamp)

            candle = {
                'time': timestamp,
                'open': float(row['open']),
                'high': float(row['high']),
                'low': float(row['low']),
                'close': float(row['close'])
            }
            candles.append(candle)

        return candles

    def calculate_atr(self, candles_4h, period=14):
        """Calculate Average True Range"""
        if len(candles_4h) < period + 1:
            return None

        recent = candles_4h[-(period + 1):]
        tr_list = []

        for i in range(1, len(recent)):
            high = recent[i]['high']
            low = recent[i]['low']
            prev_close = recent[i-1]['close']

            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            tr_list.append(tr)

        return sum(tr_list) / len(tr_list)

    def get_market_structure(self, candles_1h):
        """Get 1H market structure"""
        if len(candles_1h) < 15:
            return "NEUTRAL"

        recent = candles_1h[-15:]
        highs = [c['high'] for c in recent]
        lows = [c['low'] for c in recent]

        recent_high = max(highs[-5:])
        previous_high = max(highs[-15:-5])
        recent_low = min(lows[-5:])
        previous_low = min(lows[-15:-5])

        if recent_high > previous_high and recent_low >= previous_low:
            return "BULLISH"
        elif recent_low < previous_low and recent_high <= previous_high:
            return "BEARISH"

        return "NEUTRAL"

    def calculate_daily_levels(self, candles_15m, current_index):
        """Calculate PDH/PDL and Tokyo levels"""
        if current_index < 100:
            return None

        current_time = candles_15m[current_index]['time']
        current_date = current_time.date()

        # Previous day
        prev_day_start = datetime.combine(current_date - timedelta(days=1), datetime.min.time()).replace(tzinfo=pytz.utc)
        prev_day_end = datetime.combine(current_date, datetime.min.time()).replace(tzinfo=pytz.utc)

        prev_day_candles = [
            c for c in candles_15m[:current_index]
            if prev_day_start <= c['time'] < prev_day_end
        ]

        if not prev_day_candles:
            return None

        pdh = max(c['high'] for c in prev_day_candles)
        pdl = min(c['low'] for c in prev_day_candles)

        # Tokyo session
        tokyo_start = datetime.combine(current_date - timedelta(days=1), datetime.min.time()).replace(hour=23, tzinfo=pytz.utc)
        tokyo_end = datetime.combine(current_date, datetime.min.time()).replace(hour=8, tzinfo=pytz.utc)

        tokyo_candles = [
            c for c in candles_15m[:current_index]
            if tokyo_start <= c['time'] < tokyo_end
        ]

        if tokyo_candles:
            tokyo_high = max(c['high'] for c in tokyo_candles)
            tokyo_low = min(c['low'] for c in tokyo_candles)
        else:
            tokyo_high = pdh
            tokyo_low = pdl

        return {
            'PDH': pdh,
            'PDL': pdl,
            'TOKYO_HIGH': tokyo_high,
            'TOKYO_LOW': tokyo_low
        }

    def detect_liquidity_sweep(self, candles_15m, current_index, levels, structure):
        """Detect liquidity sweep at key levels"""
        if current_index < 3:
            return None

        current = candles_15m[current_index]
        prev = candles_15m[current_index - 1]
        prev2 = candles_15m[current_index - 2]

        # Bullish sweep
        if structure in ["BULLISH", "NEUTRAL"]:
            for level_name in ['PDL', 'TOKYO_LOW']:
                level = levels[level_name]

                swept = (prev['low'] < level or prev2['low'] < level)
                reversed = current['close'] > level

                if swept and reversed:
                    return ('BUY', level_name, current, level)

        # Bearish sweep
        if structure in ["BEARISH", "NEUTRAL"]:
            for level_name in ['PDH', 'TOKYO_HIGH']:
                level = levels[level_name]

                swept = (prev['high'] > level or prev2['high'] > level)
                reversed = current['close'] < level

                if swept and reversed:
                    return ('SELL', level_name, current, level)

        return None

    def is_trading_window(self, timestamp):
        """Check London/NY sessions"""
        hour = timestamp.hour

        if 7 <= hour < 16:
            return True, "LONDON"
        if 13 <= hour < 21:
            return True, "NY"

        return False, "CLOSED"

    def build_signal(self, direction, current_candle, rejection_candle, atr, balance):
        """Build liquidity sweep signal"""
        current_price = current_candle['close']
        risk_amount = balance * RISK_PER_TRADE

        if direction == 'BUY':
            atr_stop = current_price - (atr * ATR_MULTIPLIER)
            candle_stop = rejection_candle['low'] - 2.0
            sl = max(atr_stop, candle_stop)

            risk = current_price - sl
            tp = current_price + (risk * RISK_REWARD_RATIO)

            lot_size = risk_amount / (risk * 10)
            lot_size = max(0.01, round(lot_size, 2))

            if risk <= 0:
                return None

            return {
                "decision": "BUY",
                "price": current_price,
                "sl": round(sl, 2),
                "tp": round(tp, 2),
                "lot_size": lot_size,
                "risk": round(risk, 2),
                "atr": round(atr, 2)
            }

        else:  # SELL
            atr_stop = current_price + (atr * ATR_MULTIPLIER)
            candle_stop = rejection_candle['high'] + 2.0
            sl = min(atr_stop, candle_stop)

            risk = sl - current_price
            tp = current_price - (risk * RISK_REWARD_RATIO)

            lot_size = risk_amount / (risk * 10)
            lot_size = max(0.01, round(lot_size, 2))

            if risk <= 0:
                return None

            return {
                "decision": "SELL",
                "price": current_price,
                "sl": round(sl, 2),
                "tp": round(tp, 2),
                "lot_size": lot_size,
                "risk": round(risk, 2),
                "atr": round(atr, 2)
            }

    def simulate_trade_outcome(self, trade, future_candles):
        """Simulate with breakeven protection at 1:1"""
        entry = trade['entry_price']
        sl = trade['sl']
        tp = trade['tp']
        lot_size = trade['lot_size']

        candles_until_exit = 0
        max_favorable_excursion = 0
        max_adverse_excursion = 0

        for candle in future_candles[:200]:
            candles_until_exit += 1

            # Track MFE/MAE
            if trade['decision'] == 'BUY':
                mfe = candle['high'] - entry
                mae = entry - candle['low']
            else:
                mfe = entry - candle['low']
                mae = candle['high'] - entry

            max_favorable_excursion = max(max_favorable_excursion, mfe)
            max_adverse_excursion = max(max_adverse_excursion, mae)

            if trade['decision'] == 'BUY':
                # Breakeven at 1:1
                if not trade['breakeven_moved']:
                    risk = entry - sl
                    if candle['high'] >= entry + risk:
                        sl = entry
                        trade['breakeven_moved'] = True
                        trade['breakeven_candle'] = candles_until_exit

                # Check SL
                if candle['low'] <= sl:
                    trade['outcome'] = 'BREAKEVEN' if trade['breakeven_moved'] else 'LOSS'
                    trade['exit_price'] = sl
                    trade['exit_time'] = candle['time']
                    price_diff = (sl - entry) if not trade['breakeven_moved'] else 0
                    trade['pnl'] = price_diff * lot_size * 10
                    trade['candles_in_trade'] = candles_until_exit
                    trade['max_favorable_excursion'] = round(max_favorable_excursion, 2)
                    trade['max_adverse_excursion'] = round(max_adverse_excursion, 2)
                    self.balance += trade['pnl']
                    return

                # Check TP
                if candle['high'] >= tp:
                    trade['outcome'] = 'WIN'
                    trade['exit_price'] = tp
                    trade['exit_time'] = candle['time']
                    price_diff = tp - entry
                    trade['pnl'] = price_diff * lot_size * 10
                    trade['candles_in_trade'] = candles_until_exit
                    trade['max_favorable_excursion'] = round(max_favorable_excursion, 2)
                    trade['max_adverse_excursion'] = round(max_adverse_excursion, 2)
                    self.balance += trade['pnl']
                    return

            else:  # SELL
                # Breakeven at 1:1
                if not trade['breakeven_moved']:
                    risk = sl - entry
                    if candle['low'] <= entry - risk:
                        sl = entry
                        trade['breakeven_moved'] = True
                        trade['breakeven_candle'] = candles_until_exit

                # Check SL
                if candle['high'] >= sl:
                    trade['outcome'] = 'BREAKEVEN' if trade['breakeven_moved'] else 'LOSS'
                    trade['exit_price'] = sl
                    trade['exit_time'] = candle['time']
                    price_diff = (entry - sl) if not trade['breakeven_moved'] else 0
                    trade['pnl'] = price_diff * lot_size * 10 * -1
                    trade['candles_in_trade'] = candles_until_exit
                    trade['max_favorable_excursion'] = round(max_favorable_excursion, 2)
                    trade['max_adverse_excursion'] = round(max_adverse_excursion, 2)
                    self.balance += trade['pnl']
                    return

                # Check TP
                if candle['low'] <= tp:
                    trade['outcome'] = 'WIN'
                    trade['exit_price'] = tp
                    trade['exit_time'] = candle['time']
                    price_diff = entry - tp
                    trade['pnl'] = price_diff * lot_size * 10
                    trade['candles_in_trade'] = candles_until_exit
                    trade['max_favorable_excursion'] = round(max_favorable_excursion, 2)
                    trade['max_adverse_excursion'] = round(max_adverse_excursion, 2)
                    self.balance += trade['pnl']
                    return

        # Still open
        trade['outcome'] = 'OPEN'
        trade['candles_in_trade'] = candles_until_exit
        trade['max_favorable_excursion'] = round(max_favorable_excursion, 2)
        trade['max_adverse_excursion'] = round(max_adverse_excursion, 2)

    def run_backtest(self, data):
        """Main backtest simulation with detailed logging"""
        print("="*80)
        print("🎯 STRATEGY #4: AURUM LIQUIDITY SNIPER - DETAILED ANALYSIS")
        print("="*80)
        print("\nGenerating comprehensive trade-by-trade report...\n")

        candles_15m = data['15m']
        candles_1h = data['1h']
        candles_4h = data['4h']

        for i in range(100, len(candles_15m)):
            timestamp = candles_15m[i]['time']

            # Reset daily counter
            if self.current_date != timestamp.date():
                self.current_date = timestamp.date()
                self.trades_today = 0

            if self.trades_today >= MAX_TRADES_PER_DAY:
                continue

            # Check trading window
            in_window, session = self.is_trading_window(timestamp)
            if not in_window:
                continue

            # Calculate levels
            levels = self.calculate_daily_levels(candles_15m, i)
            if not levels:
                continue

            # Market structure
            structure = self.get_market_structure(candles_1h[:i//4+1])

            # ATR
            atr = self.calculate_atr(candles_4h[:i//16+1])
            if not atr:
                continue

            # Detect sweep
            sweep = self.detect_liquidity_sweep(candles_15m, i, levels, structure)
            if not sweep:
                continue

            direction, level_name, rejection_candle, level_price = sweep

            # Build signal
            signal = self.build_signal(direction, candles_15m[i], rejection_candle, atr, self.balance)
            if not signal:
                continue

            # Execute trade
            trade = {
                "trade_number": len(self.trades) + 1,
                "timestamp": timestamp,
                "date": timestamp.strftime('%Y-%m-%d'),
                "time": timestamp.strftime('%H:%M UTC'),
                "decision": signal['decision'],
                "entry_price": signal['price'],
                "sl": signal['sl'],
                "tp": signal['tp'],
                "lot_size": signal['lot_size'],
                "risk_dollars": round(signal['risk'] * signal['lot_size'] * 10, 2),
                "risk_percent": RISK_PER_TRADE * 100,
                "atr": signal['atr'],
                "level_swept": level_name,
                "level_price": round(level_price, 2),
                "market_structure": structure,
                "session": session,
                "outcome": None,
                "pnl": 0,
                "breakeven_moved": False,
                "breakeven_candle": None,
                "balance_before": round(self.balance, 2),
                "balance_after": None,
                "exit_price": None,
                "exit_time": None,
                "candles_in_trade": None,
                "max_favorable_excursion": None,
                "max_adverse_excursion": None
            }

            self.trades.append(trade)
            self.trades_today += 1

            # Simulate outcome
            self.simulate_trade_outcome(trade, candles_15m[i+1:])

            trade['balance_after'] = round(self.balance, 2)

            # Print progress
            if len(self.trades) % 10 == 0:
                print(f"   Processed {len(self.trades)} trades...")

        print(f"\n✅ Backtest complete! {len(self.trades)} trades analyzed\n")

    def generate_detailed_report(self):
        """Generate comprehensive HTML and text reports"""

        # Calculate statistics
        total_trades = len(self.trades)
        wins = [t for t in self.trades if t['outcome'] == 'WIN']
        losses = [t for t in self.trades if t['outcome'] == 'LOSS']
        breakevens = [t for t in self.trades if t['outcome'] == 'BREAKEVEN']
        open_trades = [t for t in self.trades if t['outcome'] == 'OPEN']

        win_rate = (len(wins) / total_trades * 100) if total_trades > 0 else 0
        total_pnl = sum(t['pnl'] for t in self.trades)
        roi = (total_pnl / INITIAL_BALANCE) * 100

        # Generate text report
        report = []
        report.append("="*100)
        report.append("STRATEGY #4: AURUM LIQUIDITY SNIPER - COMPREHENSIVE TRADE ANALYSIS")
        report.append("="*100)
        report.append(f"\nTest Period: November 1 - December 27, 2025 (57 days)")
        report.append(f"Data Source: Twelve Data API")
        report.append(f"Initial Balance: ${INITIAL_BALANCE:,.2f}")
        report.append(f"Final Balance: ${self.balance:,.2f}")
        report.append(f"Total P&L: ${total_pnl:+,.2f}")
        report.append(f"ROI: {roi:+.2f}%")
        report.append(f"\nTotal Trades: {total_trades}")
        report.append(f"Wins: {len(wins)} ({win_rate:.1f}%)")
        report.append(f"Losses: {len(losses)} ({len(losses)/total_trades*100:.1f}%)")
        report.append(f"Breakevens: {len(breakevens)} ({len(breakevens)/total_trades*100:.1f}%)")
        report.append(f"Open: {len(open_trades)} ({len(open_trades)/total_trades*100:.1f}%)")

        if wins:
            avg_win = sum(t['pnl'] for t in wins) / len(wins)
            report.append(f"\nAverage Win: ${avg_win:,.2f}")
        if losses:
            avg_loss = sum(t['pnl'] for t in losses) / len(losses)
            report.append(f"Average Loss: ${avg_loss:,.2f}")

        report.append(f"\n" + "="*100)
        report.append("INDIVIDUAL TRADE DETAILS")
        report.append("="*100)

        for trade in self.trades:
            report.append(f"\n{'='*100}")
            report.append(f"TRADE #{trade['trade_number']:03d} - {trade['decision']} - {trade['outcome'] or 'OPEN'}")
            report.append(f"{'='*100}")
            report.append(f"Date & Time:      {trade['date']} at {trade['time']}")
            report.append(f"Session:          {trade['session']}")
            report.append(f"Market Structure: {trade['market_structure']}")
            report.append(f"Level Swept:      {trade['level_swept']} (${trade['level_price']:.2f})")
            report.append(f"")
            report.append(f"Entry Price:      ${trade['entry_price']:.2f}")
            report.append(f"Stop Loss:        ${trade['sl']:.2f}")
            report.append(f"Take Profit:      ${trade['tp']:.2f}")
            report.append(f"Risk:Reward:      1:{RISK_REWARD_RATIO}")
            report.append(f"")
            report.append(f"Lot Size:         {trade['lot_size']}")
            report.append(f"Risk Amount:      ${trade['risk_dollars']:.2f} ({trade['risk_percent']:.0f}%)")
            report.append(f"ATR at Entry:     ${trade['atr']:.2f}")
            report.append(f"")

            if trade['outcome'] and trade['outcome'] != 'OPEN':
                if trade['exit_price'] is not None:
                    report.append(f"Exit Price:       ${trade['exit_price']:.2f}")
                if trade['exit_time']:
                    exit_time_str = trade['exit_time'].strftime('%Y-%m-%d %H:%M UTC')
                    report.append(f"Exit Time:        {exit_time_str}")
                if trade['candles_in_trade'] is not None:
                    report.append(f"Candles in Trade: {trade['candles_in_trade']} ({trade['candles_in_trade'] * 15} minutes)")
                report.append(f"")
                report.append(f"P&L:              ${trade['pnl']:+,.2f}")
                report.append(f"Balance Before:   ${trade['balance_before']:,.2f}")
                report.append(f"Balance After:    ${trade['balance_after']:,.2f}")
                report.append(f"")

                if trade['breakeven_moved']:
                    report.append(f"Breakeven:        ✅ Activated after {trade['breakeven_candle']} candles")
                else:
                    report.append(f"Breakeven:        ❌ Not triggered")

                report.append(f"")
                if trade['max_favorable_excursion'] is not None:
                    report.append(f"Max Favorable:    ${trade['max_favorable_excursion']:.2f}")
                if trade['max_adverse_excursion'] is not None:
                    report.append(f"Max Adverse:      ${trade['max_adverse_excursion']:.2f}")

                # Analysis
                if trade['outcome'] == 'WIN':
                    report.append(f"\n✅ WINNER - Full 1:3 RR achieved")
                elif trade['outcome'] == 'LOSS':
                    report.append(f"\n❌ LOSS - Stop loss hit")
                elif trade['outcome'] == 'BREAKEVEN':
                    report.append(f"\n➖ BREAKEVEN - Protected by 1:1 RR move")
            else:
                report.append(f"Status:           ⏳ STILL OPEN at backtest end")
                if trade['max_favorable_excursion'] is not None:
                    report.append(f"Max Favorable:    ${trade['max_favorable_excursion']:.2f}")
                if trade['max_adverse_excursion'] is not None:
                    report.append(f"Max Adverse:      ${trade['max_adverse_excursion']:.2f}")

        report.append(f"\n{'='*100}")
        report.append("END OF REPORT")
        report.append("="*100)

        # Save to file
        report_text = "\n".join(report)
        with open('STRATEGY_4_DETAILED_REPORT.txt', 'w') as f:
            f.write(report_text)

        # Also save JSON for programmatic access
        trades_json = []
        for trade in self.trades:
            trade_dict = trade.copy()
            # Convert datetime objects to strings
            trade_dict['timestamp'] = trade['timestamp'].isoformat()
            if trade_dict['exit_time']:
                trade_dict['exit_time'] = trade_dict['exit_time'].isoformat()
            trades_json.append(trade_dict)

        with open('STRATEGY_4_TRADES.json', 'w') as f:
            json.dump({
                'summary': {
                    'total_trades': total_trades,
                    'wins': len(wins),
                    'losses': len(losses),
                    'breakevens': len(breakevens),
                    'open': len(open_trades),
                    'win_rate': round(win_rate, 2),
                    'total_pnl': round(total_pnl, 2),
                    'roi': round(roi, 2),
                    'initial_balance': INITIAL_BALANCE,
                    'final_balance': round(self.balance, 2)
                },
                'trades': trades_json
            }, f, indent=2)

        print("="*80)
        print("📄 REPORTS GENERATED")
        print("="*80)
        print(f"\n✅ Text Report:  STRATEGY_4_DETAILED_REPORT.txt")
        print(f"✅ JSON Data:    STRATEGY_4_TRADES.json")
        print(f"\n{len(self.trades)} trades documented with full details\n")

        return report_text

def main():
    print("\n" + "="*80)
    print("🎯 STRATEGY #4: COMPREHENSIVE TRADE ANALYSIS")
    print("="*80)
    print("\nGenerating detailed report for manual review before deployment...\n")

    analyzer = DetailedStrategy4Report()

    # Fetch data
    data = analyzer.fetch_data_twelvedata()
    if data is None:
        print("❌ Failed to fetch data. Exiting.")
        return

    # Run backtest with detailed tracking
    analyzer.run_backtest(data)

    # Generate comprehensive reports
    report = analyzer.generate_detailed_report()

    # Print summary
    print("="*80)
    print("📊 QUICK SUMMARY")
    print("="*80)
    print(report.split("INDIVIDUAL TRADE DETAILS")[0])

if __name__ == "__main__":
    main()
