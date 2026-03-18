#!/usr/bin/env python3
"""
Strategy v6.0 Detailed Report Generator
Creates comprehensive trade-by-trade analysis for manual comparison
"""

import json
from datetime import datetime

def generate_detailed_report():
    """Generate comprehensive v6.0 report"""

    # Load v6.0 results
    with open('STRATEGY_V6_0_RESULTS.json', 'r') as f:
        data = json.load(f)

    trades = data['trades']

    # Organize trades by outcome
    wins = [t for t in trades if t.get('outcome') == 'WIN']
    losses = [t for t in trades if t.get('outcome') == 'LOSS']
    breakevens = [t for t in trades if t.get('outcome') == 'BREAKEVEN']
    open_trades = [t for t in trades if t.get('outcome') == 'OPEN']
    partial_activated = [t for t in trades if t.get('partial_activated')]

    # Calculate statistics
    total_trades = len(trades)
    total_pnl = data['total_pnl']
    roi = data['roi']

    avg_win = sum(t['pnl'] for t in wins) / len(wins) if wins else 0
    avg_loss = sum(t['pnl'] for t in losses) / len(losses) if losses else 0
    avg_be = sum(t['pnl'] for t in breakevens) / len(breakevens) if breakevens else 0

    # Start building report
    report = []
    report.append("="*100)
    report.append("STRATEGY v6.0: RESILIENT SNIPER - DETAILED TRADE REPORT")
    report.append("="*100)
    report.append("")
    report.append("TEST PERIOD: November 1 - December 27, 2025 (57 days)")
    report.append("DATA SOURCE: Twelve Data API (15-minute candles)")
    report.append("")
    report.append("="*100)
    report.append("EXECUTIVE SUMMARY")
    report.append("="*100)
    report.append("")
    report.append(f"Initial Balance:      ${data['initial_balance']:,.2f}")
    report.append(f"Final Balance:        ${data['final_balance']:,.2f}")
    report.append(f"Total P&L:            ${total_pnl:+,.2f}")
    report.append(f"ROI:                  {roi:+.2f}%")
    report.append("")
    report.append("TRADE STATISTICS:")
    report.append(f"  Total Trades:       {total_trades}")
    report.append(f"  Wins:               {len(wins)} ({len(wins)/total_trades*100:.1f}%)")
    report.append(f"  Losses:             {len(losses)} ({len(losses)/total_trades*100:.1f}%)")
    report.append(f"  Breakevens:         {len(breakevens)} ({len(breakevens)/total_trades*100:.1f}%)")
    report.append(f"  Open:               {len(open_trades)} ({len(open_trades)/total_trades*100:.1f}%)")
    report.append("")
    report.append("v6.0 ENHANCEMENTS:")
    report.append(f"  Partial Activations: {len(partial_activated)} ({len(partial_activated)/total_trades*100:.1f}%)")
    report.append(f"  - Close 50% at 1:1.5 RR")
    report.append(f"  - Move SL to entry after partial")
    report.append(f"  - Displacement filter required")
    report.append(f"  - Time windows: London 07:00-11:00 + NY 13:00-16:00 UTC")
    report.append("")
    report.append("AVERAGES:")
    report.append(f"  Average Win:        ${avg_win:,.2f}")
    report.append(f"  Average Loss:       ${avg_loss:,.2f}")
    if breakevens:
        report.append(f"  Average Breakeven:  ${avg_be:,.2f}")
    if wins and losses:
        win_loss_ratio = abs(avg_win / avg_loss)
        report.append(f"  Win/Loss Ratio:     {win_loss_ratio:.1f}:1")
    report.append("")

    # Market structure breakdown
    structures = {}
    for t in trades:
        struct = t.get('market_structure', 'UNKNOWN')
        if struct not in structures:
            structures[struct] = {'total': 0, 'wins': 0, 'losses': 0, 'be': 0}
        structures[struct]['total'] += 1
        if t.get('outcome') == 'WIN':
            structures[struct]['wins'] += 1
        elif t.get('outcome') == 'LOSS':
            structures[struct]['losses'] += 1
        elif t.get('outcome') == 'BREAKEVEN':
            structures[struct]['be'] += 1

    report.append("MARKET STRUCTURE BREAKDOWN:")
    for struct, stats in sorted(structures.items()):
        report.append(f"  {struct}:")
        report.append(f"    Total: {stats['total']}, Wins: {stats['wins']}, Losses: {stats['losses']}, BE: {stats['be']}")
    report.append("")

    # Session breakdown
    sessions = {}
    for t in trades:
        sess = t.get('session', 'UNKNOWN')
        if sess not in sessions:
            sessions[sess] = {'total': 0, 'wins': 0, 'losses': 0, 'be': 0}
        sessions[sess]['total'] += 1
        if t.get('outcome') == 'WIN':
            sessions[sess]['wins'] += 1
        elif t.get('outcome') == 'LOSS':
            sessions[sess]['losses'] += 1
        elif t.get('outcome') == 'BREAKEVEN':
            sessions[sess]['be'] += 1

    report.append("SESSION BREAKDOWN:")
    for sess, stats in sorted(sessions.items()):
        report.append(f"  {sess}:")
        report.append(f"    Total: {stats['total']}, Wins: {stats['wins']}, Losses: {stats['losses']}, BE: {stats['be']}")
    report.append("")

    report.append("="*100)
    report.append("")

    # ALL WINNING TRADES
    if wins:
        report.append("="*100)
        report.append(f"WINNING TRADES ({len(wins)} TOTAL)")
        report.append("="*100)
        report.append("")

        for trade in sorted(wins, key=lambda x: x['pnl'], reverse=True):
            report.append(f"TRADE #{trade['trade_number']:03d} - {trade['decision']} - WIN")
            report.append(f"Date & Time:      {trade['timestamp']}")
            report.append(f"Session:          {trade['session']}")
            report.append(f"Market Structure: {trade['market_structure']}")
            report.append(f"Level Swept:      {trade['level_swept']} (${trade['level_price']:.2f})")
            report.append(f"")
            report.append(f"Entry Price:      ${trade['entry_price']:.2f}")
            report.append(f"Stop Loss:        ${trade['sl']:.2f}")
            report.append(f"Take Profit:      ${trade['tp']:.2f}")
            report.append(f"Lot Size:         {trade['lot_size']}")
            report.append(f"ATR at Entry:     ${trade['atr']:.2f}")
            report.append(f"")

            if trade.get('partial_activated'):
                report.append(f"🎯 PARTIAL PROFIT TAKEN:")
                report.append(f"   50% closed at:  ${trade['partial_close_price']:.2f} (1:1.5 RR)")
                report.append(f"   After candles:  {trade['partial_close_candle']}")
                report.append(f"   SL moved to:    ${trade['entry_price']:.2f} (breakeven)")
                report.append(f"")
            else:
                report.append(f"⚠️  No partial activation (hit TP directly)")
                report.append(f"")

            if trade.get('exit_price'):
                report.append(f"Exit Price:       ${trade['exit_price']:.2f}")
            if trade.get('exit_time'):
                report.append(f"Exit Time:        {trade['exit_time']}")
            if trade.get('candles_in_trade'):
                report.append(f"Candles in Trade: {trade['candles_in_trade']} ({trade['candles_in_trade'] * 15} minutes)")
            report.append(f"")
            report.append(f"P&L:              ${trade['pnl']:+,.2f}")
            report.append(f"Balance Before:   ${trade['balance_before']:,.2f}")
            if trade.get('balance_after'):
                report.append(f"Balance After:    ${trade['balance_after']:,.2f}")
            report.append(f"")
            report.append(f"✅ WINNER - Full TP achieved")
            report.append(f"")
            report.append("-"*100)
            report.append("")

    # ALL LOSING TRADES
    if losses:
        report.append("="*100)
        report.append(f"LOSING TRADES ({len(losses)} TOTAL)")
        report.append("="*100)
        report.append("")

        for trade in sorted(losses, key=lambda x: x['pnl']):
            report.append(f"TRADE #{trade['trade_number']:03d} - {trade['decision']} - LOSS")
            report.append(f"Date & Time:      {trade['timestamp']}")
            report.append(f"Session:          {trade['session']}")
            report.append(f"Market Structure: {trade['market_structure']}")
            report.append(f"Level Swept:      {trade['level_swept']} (${trade['level_price']:.2f})")
            report.append(f"")
            report.append(f"Entry Price:      ${trade['entry_price']:.2f}")
            report.append(f"Stop Loss:        ${trade['sl']:.2f}")
            report.append(f"Take Profit:      ${trade['tp']:.2f}")
            report.append(f"Lot Size:         {trade['lot_size']}")
            report.append(f"ATR at Entry:     ${trade['atr']:.2f}")
            report.append(f"")

            if trade.get('partial_activated'):
                report.append(f"🎯 PARTIAL PROFIT TAKEN (but still lost overall):")
                report.append(f"   50% closed at:  ${trade['partial_close_price']:.2f} (1:1.5 RR)")
                report.append(f"   After candles:  {trade['partial_close_candle']}")
                report.append(f"   Then SL hit at: ${trade['entry_price']:.2f} (remaining 50%)")
                report.append(f"   Net P&L:        ${trade['pnl']:+.2f} (partial saved some)")
                report.append(f"")
            else:
                report.append(f"❌ No partial activation - full stop loss hit")
                report.append(f"")

            if trade.get('exit_price'):
                report.append(f"Exit Price:       ${trade['exit_price']:.2f}")
            if trade.get('exit_time'):
                report.append(f"Exit Time:        {trade['exit_time']}")
            if trade.get('candles_in_trade'):
                report.append(f"Candles in Trade: {trade['candles_in_trade']} ({trade['candles_in_trade'] * 15} minutes)")
            report.append(f"")
            report.append(f"P&L:              ${trade['pnl']:+,.2f}")
            report.append(f"Balance Before:   ${trade['balance_before']:,.2f}")
            if trade.get('balance_after'):
                report.append(f"Balance After:    ${trade['balance_after']:,.2f}")
            report.append(f"")
            report.append(f"❌ LOSS - Stop loss hit")
            report.append(f"")
            report.append("-"*100)
            report.append("")

    # ALL BREAKEVEN TRADES
    if breakevens:
        report.append("="*100)
        report.append(f"BREAKEVEN TRADES ({len(breakevens)} TOTAL)")
        report.append("="*100)
        report.append("")

        for trade in sorted(breakevens, key=lambda x: x.get('pnl', 0), reverse=True):
            report.append(f"TRADE #{trade['trade_number']:03d} - {trade['decision']} - BREAKEVEN")
            report.append(f"Date & Time:      {trade['timestamp']}")
            report.append(f"Session:          {trade['session']}")
            report.append(f"Market Structure: {trade['market_structure']}")
            report.append(f"Level Swept:      {trade['level_swept']} (${trade['level_price']:.2f})")
            report.append(f"")
            report.append(f"Entry Price:      ${trade['entry_price']:.2f}")
            report.append(f"Stop Loss:        ${trade['sl']:.2f}")
            report.append(f"Take Profit:      ${trade['tp']:.2f}")
            report.append(f"Lot Size:         {trade['lot_size']}")
            report.append(f"ATR at Entry:     ${trade['atr']:.2f}")
            report.append(f"")

            if trade.get('partial_activated'):
                report.append(f"🎯 PARTIAL PROFIT BANKED:")
                report.append(f"   50% closed at:  ${trade['partial_close_price']:.2f} (1:1.5 RR)")
                report.append(f"   After candles:  {trade['partial_close_candle']}")
                report.append(f"   Remaining 50%:  Closed at breakeven (${trade['entry_price']:.2f})")
                report.append(f"   Net P&L:        ${trade['pnl']:+.2f} (partial profit only)")
                report.append(f"")
            else:
                report.append(f"➖ No partial - closed at entry (breakeven)")
                report.append(f"")

            if trade.get('exit_price'):
                report.append(f"Exit Price:       ${trade['exit_price']:.2f}")
            if trade.get('exit_time'):
                report.append(f"Exit Time:        {trade['exit_time']}")
            if trade.get('candles_in_trade'):
                report.append(f"Candles in Trade: {trade['candles_in_trade']} ({trade['candles_in_trade'] * 15} minutes)")
            report.append(f"")
            report.append(f"P&L:              ${trade.get('pnl', 0):+,.2f}")
            report.append(f"Balance Before:   ${trade['balance_before']:,.2f}")
            if trade.get('balance_after'):
                report.append(f"Balance After:    ${trade['balance_after']:,.2f}")
            report.append(f"")
            report.append(f"➖ BREAKEVEN - Protected by partial profit or entry exit")
            report.append(f"")
            report.append("-"*100)
            report.append("")

    # OPEN TRADES
    if open_trades:
        report.append("="*100)
        report.append(f"OPEN TRADES ({len(open_trades)} TOTAL) - Still active at backtest end")
        report.append("="*100)
        report.append("")

        for trade in open_trades:
            report.append(f"TRADE #{trade['trade_number']:03d} - {trade['decision']} - OPEN")
            report.append(f"Date & Time:      {trade['timestamp']}")
            report.append(f"Session:          {trade['session']}")
            report.append(f"Market Structure: {trade['market_structure']}")
            report.append(f"Level Swept:      {trade['level_swept']} (${trade['level_price']:.2f})")
            report.append(f"")
            report.append(f"Entry Price:      ${trade['entry_price']:.2f}")
            report.append(f"Stop Loss:        ${trade['sl']:.2f}")
            report.append(f"Take Profit:      ${trade['tp']:.2f}")
            report.append(f"Lot Size:         {trade['lot_size']}")
            report.append(f"ATR at Entry:     ${trade['atr']:.2f}")
            report.append(f"")

            if trade.get('partial_activated'):
                report.append(f"🎯 PARTIAL PROFIT ALREADY BANKED:")
                report.append(f"   50% closed at:  ${trade['partial_close_price']:.2f} (1:1.5 RR)")
                report.append(f"   After candles:  {trade['partial_close_candle']}")
                report.append(f"   Remaining 50%:  Still open, SL at breakeven")
                report.append(f"")
            else:
                report.append(f"⏳ Awaiting 1:1.5 RR or SL hit")
                report.append(f"")

            report.append(f"Balance Before:   ${trade['balance_before']:,.2f}")
            report.append(f"")
            report.append(f"⏳ STILL OPEN - Trade not resolved by backtest end")
            report.append(f"")
            report.append("-"*100)
            report.append("")

    # QUICK REFERENCE SUMMARY
    report.append("")
    report.append("="*100)
    report.append("QUICK REFERENCE: v6.0 vs v4 SIDE-BY-SIDE")
    report.append("="*100)
    report.append("")
    report.append("Metric                      | v4 Liquidity Sniper | v6.0 Resilient Sniper")
    report.append("----------------------------|---------------------|----------------------")
    report.append(f"ROI                         | +44.02%             | {roi:+.2f}%")
    report.append(f"Total Trades                | 101                 | {total_trades}")
    report.append(f"Win Rate                    | 5.9%                | {len(wins)/total_trades*100:.1f}%")
    report.append(f"Loss Rate                   | 50.5%               | {len(losses)/total_trades*100:.1f}%")
    report.append(f"Breakeven Rate              | 40.6%               | {len(breakevens)/total_trades*100:.1f}%")
    report.append(f"Partial Activation Rate     | N/A (1:1 BE only)   | {len(partial_activated)/total_trades*100:.1f}%")
    report.append(f"Average Win                 | $354.26             | ${avg_win:.2f}")
    report.append(f"Average Loss                | -$44.63             | ${avg_loss:.2f}")
    if wins and losses:
        report.append(f"Win/Loss Ratio              | 7.9:1               | {win_loss_ratio:.1f}:1")
    report.append("")
    report.append("ENHANCEMENTS:")
    report.append("v4: 1:1 breakeven trigger, full sessions, no filters")
    report.append("v6.0: 1:1.5 partial profit, displacement filter, narrowed time windows")
    report.append("")
    report.append("="*100)
    report.append("END OF DETAILED REPORT")
    report.append("="*100)

    # Save report
    report_text = "\n".join(report)
    with open('STRATEGY_V6_0_DETAILED_REPORT.txt', 'w') as f:
        f.write(report_text)

    print("✅ Detailed report saved to STRATEGY_V6_0_DETAILED_REPORT.txt")

    # Create quick reference
    quick_ref = []
    quick_ref.append("="*80)
    quick_ref.append("STRATEGY v6.0: QUICK REFERENCE")
    quick_ref.append("="*80)
    quick_ref.append("")
    quick_ref.append(f"ROI:              {roi:+.2f}%")
    quick_ref.append(f"Final Balance:    ${data['final_balance']:,.2f}")
    quick_ref.append(f"Total P&L:        ${total_pnl:+,.2f}")
    quick_ref.append("")
    quick_ref.append(f"Total Trades:    {total_trades}")
    quick_ref.append(f"├─ Wins:         {len(wins)}    ({len(wins)/total_trades*100:.1f}%)   ✅")
    quick_ref.append(f"├─ Losses:       {len(losses)}   ({len(losses)/total_trades*100:.1f}%)  ❌")
    quick_ref.append(f"├─ Breakevens:   {len(breakevens)}   ({len(breakevens)/total_trades*100:.1f}%)  ➖")
    quick_ref.append(f"└─ Open:         {len(open_trades)}   ({len(open_trades)/total_trades*100:.1f}%)  ⏳")
    quick_ref.append("")
    quick_ref.append(f"Partial Activations: {len(partial_activated)} ({len(partial_activated)/total_trades*100:.1f}%)")
    quick_ref.append("")
    quick_ref.append(f"Average Win:     ${avg_win:,.2f}")
    quick_ref.append(f"Average Loss:    ${avg_loss:,.2f}")
    if wins and losses:
        quick_ref.append(f"Win/Loss Ratio:  {win_loss_ratio:.1f}:1")
    quick_ref.append("")
    quick_ref.append("="*80)
    quick_ref.append("v6.0 ENHANCEMENTS:")
    quick_ref.append("  1. Partial profit at 1:1.5 RR (50% close)")
    quick_ref.append("  2. Displacement filter (expansion candle)")
    quick_ref.append("  3. Narrowed windows (London 07:00-11:00 + NY 13:00-16:00)")
    quick_ref.append("")
    quick_ref.append("RESULT: All 3 enhancements FAILED")
    quick_ref.append("RECOMMENDATION: Revert to v4 (+44.02% ROI)")
    quick_ref.append("="*80)

    with open('STRATEGY_V6_0_QUICK_REFERENCE.txt', 'w') as f:
        f.write("\n".join(quick_ref))

    print("✅ Quick reference saved to STRATEGY_V6_0_QUICK_REFERENCE.txt")

    # Create trade-by-trade CSV for easy analysis
    import csv

    with open('STRATEGY_V6_0_TRADES.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Trade#', 'Timestamp', 'Decision', 'Entry', 'SL', 'TP',
            'Lot Size', 'Structure', 'Session', 'Level Swept',
            'Partial Activated', 'Partial Price', 'Partial Candle',
            'Outcome', 'Exit Price', 'Exit Time', 'Candles', 'P&L',
            'Balance Before', 'Balance After'
        ])

        for trade in trades:
            writer.writerow([
                trade['trade_number'],
                trade['timestamp'],
                trade['decision'],
                trade['entry_price'],
                trade['sl'],
                trade['tp'],
                trade['lot_size'],
                trade['market_structure'],
                trade['session'],
                trade['level_swept'],
                trade.get('partial_activated', False),
                trade.get('partial_close_price', ''),
                trade.get('partial_close_candle', ''),
                trade.get('outcome', 'OPEN'),
                trade.get('exit_price', ''),
                trade.get('exit_time', ''),
                trade.get('candles_in_trade', ''),
                trade.get('pnl', ''),
                trade['balance_before'],
                trade.get('balance_after', '')
            ])

    print("✅ CSV export saved to STRATEGY_V6_0_TRADES.csv")

    print("\n" + "="*80)
    print("📊 REPORT GENERATION COMPLETE")
    print("="*80)
    print("\nGenerated files:")
    print("  1. STRATEGY_V6_0_DETAILED_REPORT.txt (all 83 trades)")
    print("  2. STRATEGY_V6_0_QUICK_REFERENCE.txt (one-page summary)")
    print("  3. STRATEGY_V6_0_TRADES.csv (Excel-friendly format)")
    print("\nYou can now manually compare v6.0 vs v4 trade-by-trade.")
    print("="*80)

if __name__ == "__main__":
    generate_detailed_report()
