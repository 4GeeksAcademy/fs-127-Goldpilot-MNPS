"""
Generate detailed trade-by-trade report for Internal Flow Strategy
"""

import json
from datetime import datetime

# Load results
with open('INTERNAL_FLOW_RESULTS.json', 'r') as f:
    data = json.load(f)

print("="*100)
print("INTERNAL FLOW STRATEGY: DETAILED TRADE ANALYSIS")
print("="*100)
print(f"\nStrategy: {data['strategy']}")
print(f"Test Period: {data['test_period']}")
print(f"Generated: {data['generated_at']}")

print("\n" + "="*100)
print("DEMO WALLET ($5,000) - TRADE-BY-TRADE BREAKDOWN")
print("="*100)

demo_trades = data['demo']['trades']
for i, trade in enumerate(demo_trades, 1):
    print(f"\n{'='*100}")
    print(f"TRADE #{i}")
    print(f"{'='*100}")

    # Entry Details
    entry_time = datetime.fromisoformat(trade['timestamp'].replace('+00:00', ''))
    print(f"\n📍 ENTRY")
    print(f"  Timestamp:        {entry_time.strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"  Direction:        {trade['direction']}")
    print(f"  Entry Price:      ${trade['entry_price']:.2f}")
    print(f"  Lot Size:         {trade['lot_size']}")

    # Setup Details
    print(f"\n🎯 SETUP")
    print(f"  H4 Trend:         {trade['h4_trend']}")
    print(f"  Session:          {trade['session']}")
    print(f"  Target Type:      {trade['target_type']}")
    print(f"  CHoCH Level:      {trade['choch_level']}")
    print(f"  EMA20:            {trade['ema20']}")
    print(f"  Reason:           {trade['reason']}")

    # Risk Management
    print(f"\n⚖️ RISK MANAGEMENT")
    print(f"  Stop Loss:        ${trade['sl']:.2f}")
    print(f"  Take Profit:      ${trade['tp']:.2f}")
    print(f"  Risk (Points):    ${trade['risk']:.2f}")
    print(f"  Planned RRR:      {trade['rrr']:.2f}:1")

    # Calculate distances
    if trade['direction'] == 'BUY':
        sl_distance = trade['entry_price'] - trade['sl']
        tp_distance = trade['tp'] - trade['entry_price']
    else:
        sl_distance = trade['sl'] - trade['entry_price']
        tp_distance = trade['entry_price'] - trade['tp']

    print(f"  SL Distance:      ${sl_distance:.2f} ({sl_distance} points)")
    print(f"  TP Distance:      ${tp_distance:.2f} ({tp_distance} points)")

    # Exit Details
    print(f"\n🚪 EXIT")
    print(f"  Outcome:          {trade['outcome']}")
    print(f"  Exit Reason:      {trade.get('exit_reason', 'N/A')}")

    if trade['exit_time']:
        exit_time = datetime.fromisoformat(str(trade['exit_time']).replace('+00:00', ''))
        print(f"  Exit Time:        {exit_time.strftime('%Y-%m-%d %H:%M UTC')}")

        # Calculate hold time
        hold_duration = exit_time - entry_time
        hours = hold_duration.total_seconds() / 3600
        print(f"  Hold Duration:    {hours:.1f} hours")

    if trade['exit_price']:
        print(f"  Exit Price:       ${trade['exit_price']:.2f}")

        # Calculate actual move
        if trade['direction'] == 'BUY':
            actual_move = trade['exit_price'] - trade['entry_price']
        else:
            actual_move = trade['entry_price'] - trade['exit_price']

        print(f"  Actual Move:      ${actual_move:+.2f} ({actual_move:+.0f} points)")

    # P&L Analysis
    print(f"\n💰 P&L")
    print(f"  P&L Amount:       ${trade['pnl']:+.2f}")

    if trade['pnl'] != 0 and trade['risk'] != 0:
        actual_rrr = abs(trade['pnl'] / (trade['risk'] * trade['lot_size'] * 10))
        print(f"  Actual RRR:       {actual_rrr:.2f}:1")

        if trade['outcome'] == 'WIN':
            efficiency = (actual_rrr / trade['rrr']) * 100 if trade['rrr'] > 0 else 0
            print(f"  TP Efficiency:    {efficiency:.1f}% (Actual vs Planned RRR)")

# Summary Statistics
print("\n" + "="*100)
print("SUMMARY STATISTICS")
print("="*100)

stats = data['demo']['stats']
print(f"\n📊 PERFORMANCE")
print(f"  Initial Balance:  ${data['demo']['initial_balance']:,.2f}")
print(f"  Final Balance:    ${data['demo']['final_balance']:,.2f}")
print(f"  Total P&L:        ${stats['total_pnl']:+,.2f}")
print(f"  ROI:              {(stats['total_pnl'] / data['demo']['initial_balance'] * 100):+.2f}%")

print(f"\n📈 TRADE BREAKDOWN")
print(f"  Total Trades:     {stats['total_trades']}")
print(f"  Wins:             {stats['wins']} ({stats['win_rate']:.1f}%)")
print(f"  Losses:           {stats['losses']}")
print(f"  Time Stops:       {stats['time_stops']}")
print(f"  Open:             {stats['open']}")

print(f"\n💵 RISK METRICS")
print(f"  Average Win:      ${stats['avg_win']:,.2f}")
print(f"  Average Loss:     ${stats['avg_loss']:,.2f}")
print(f"  Average RRR:      {stats['avg_rrr']:.2f}:1")

if stats['avg_loss'] != 0:
    win_loss_ratio = abs(stats['avg_win'] / stats['avg_loss'])
    print(f"  Win/Loss Ratio:   {win_loss_ratio:.2f}:1")

# Trade Pattern Analysis
print(f"\n" + "="*100)
print("PATTERN ANALYSIS")
print("="*100)

# Group by outcome
wins = [t for t in demo_trades if t['outcome'] == 'WIN']
losses = [t for t in demo_trades if t['outcome'] == 'LOSS']
time_stops = [t for t in demo_trades if t['outcome'] == 'TIME_STOP']

print(f"\n✅ WINNING TRADES ({len(wins)})")
for i, trade in enumerate(wins, 1):
    entry_time = datetime.fromisoformat(trade['timestamp'].replace('+00:00', ''))
    print(f"  {i}. {entry_time.strftime('%Y-%m-%d %H:%M')} | {trade['direction']:4s} | "
          f"RRR: {trade['rrr']:.1f}:1 | P&L: ${trade['pnl']:+.2f} | {trade['target_type']}")

if losses:
    print(f"\n❌ LOSING TRADES ({len(losses)})")
    for i, trade in enumerate(losses, 1):
        entry_time = datetime.fromisoformat(trade['timestamp'].replace('+00:00', ''))
        print(f"  {i}. {entry_time.strftime('%Y-%m-%d %H:%M')} | {trade['direction']:4s} | "
              f"RRR: {trade['rrr']:.1f}:1 | P&L: ${trade['pnl']:+.2f} | {trade.get('exit_reason', 'N/A')}")

if time_stops:
    print(f"\n⏰ TIME STOP TRADES ({len(time_stops)})")
    for i, trade in enumerate(time_stops, 1):
        entry_time = datetime.fromisoformat(trade['timestamp'].replace('+00:00', ''))
        print(f"  {i}. {entry_time.strftime('%Y-%m-%d %H:%M')} | {trade['direction']:4s} | "
              f"RRR: {trade['rrr']:.1f}:1 | P&L: ${trade['pnl']:+.2f} | {trade['target_type']}")

# Target Type Analysis
print(f"\n" + "="*100)
print("TARGET TYPE BREAKDOWN")
print("="*100)

h1_level_trades = [t for t in demo_trades if 'H1 Level' in t.get('target_type', '')]
price_discovery_trades = [t for t in demo_trades if 'Price Discovery' in t.get('target_type', '')]

print(f"\n🎯 H1 LEVEL TARGETS ({len(h1_level_trades)})")
if h1_level_trades:
    h1_wins = [t for t in h1_level_trades if t['outcome'] == 'WIN']
    h1_avg_rrr = sum(t['rrr'] for t in h1_level_trades) / len(h1_level_trades)
    h1_total_pnl = sum(t['pnl'] for t in h1_level_trades)
    print(f"  Win Rate:         {len(h1_wins) / len(h1_level_trades) * 100:.1f}%")
    print(f"  Average RRR:      {h1_avg_rrr:.2f}:1")
    print(f"  Total P&L:        ${h1_total_pnl:+.2f}")

print(f"\n🚀 PRICE DISCOVERY (1:3 RR) TARGETS ({len(price_discovery_trades)})")
if price_discovery_trades:
    pd_wins = [t for t in price_discovery_trades if t['outcome'] == 'WIN']
    pd_avg_rrr = sum(t['rrr'] for t in price_discovery_trades) / len(price_discovery_trades)
    pd_total_pnl = sum(t['pnl'] for t in price_discovery_trades)
    print(f"  Win Rate:         {len(pd_wins) / len(price_discovery_trades) * 100:.1f}%")
    print(f"  Average RRR:      {pd_avg_rrr:.2f}:1")
    print(f"  Total P&L:        ${pd_total_pnl:+.2f}")

# Direction Analysis
print(f"\n" + "="*100)
print("DIRECTION ANALYSIS")
print("="*100)

buys = [t for t in demo_trades if t['direction'] == 'BUY']
sells = [t for t in demo_trades if t['direction'] == 'SELL']

print(f"\n📈 BUY TRADES ({len(buys)})")
if buys:
    buy_wins = [t for t in buys if t['outcome'] == 'WIN']
    buy_pnl = sum(t['pnl'] for t in buys)
    print(f"  Win Rate:         {len(buy_wins) / len(buys) * 100:.1f}%")
    print(f"  Total P&L:        ${buy_pnl:+.2f}")
    print(f"  Avg P&L:          ${buy_pnl / len(buys):+.2f}")

print(f"\n📉 SELL TRADES ({len(sells)})")
if sells:
    sell_wins = [t for t in sells if t['outcome'] == 'WIN']
    sell_pnl = sum(t['pnl'] for t in sells)
    print(f"  Win Rate:         {len(sell_wins) / len(sells) * 100:.1f}%")
    print(f"  Total P&L:        ${sell_pnl:+.2f}")
    print(f"  Avg P&L:          ${sell_pnl / len(sells):+.2f}")

print("\n" + "="*100)
print("END OF REPORT")
print("="*100)
