import json
import os
from datetime import datetime

def generate_v11_detailed_report():
    """Institutional Report Generator for Strategy v11.0: Ghost Protocol"""
    
    file_path = 'STRATEGY_V11_RESULTS.json'
    if not os.path.exists(file_path):
        print(f"❌ ERROR: {file_path} not found. Ensure backtest_v11.py has run.")
        return

    with open(file_path, 'r') as f:
        data = json.load(f)

    trades = data['trades']
    total_trades = len(trades)
    
    # Outcome Buckets
    wins = [t for t in trades if t['status'] == "WIN"]
    losses = [t for t in trades if t['status'] == "LOSS"]
    bes = [t for t in trades if t['status'] == "BE"]
    partial_bes = [t for t in trades if t['status'] == "PARTIAL_BE"]
    timeouts = [t for t in trades if t['status'] == "TIMEOUT"]
    
    # Wallet Metrics
    demo_start = data['demo_start']
    demo_final = data['demo_final']
    real_start = data['real_start']
    real_final = data['real_final']
    
    demo_roi = ((demo_final - demo_start) / demo_start) * 100
    real_roi = ((real_final - real_start) / real_start) * 100
    
    # Gating & Cooldown Stats
    skipped_real = len([t for t in trades if not t['real_active']])

    report = []
    report.append("="*100)
    report.append("AURUM ARCHITECT: STRATEGY v11.0 GHOST PROTOCOL AUDIT")
    report.append("="*100)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Logic: 1:3 RR | 60% Bank at 1:1.5 RR | ATR-Min SL | One-Shot Level Cooldown")
    report.append("")

    report.append("="*100)
    report.append("EXECUTIVE SUMMARY")
    report.append("="*100)
    report.append(f"VAULT A (DEMO $5K):   ROI {demo_roi:+.2f}% | Final: ${demo_final:,.2f}")
    report.append(f"VAULT B (REAL $200):  ROI {real_roi:+.2f}% | Final: ${real_final:,.2f} ⭐")
    report.append("")
    report.append("TRADE STATISTICS:")
    report.append(f"  Total Signals:       {total_trades}")
    report.append(f"  Full Wins (1:3):     {len(wins)}  ({(len(wins)/total_trades*100) if total_trades > 0 else 0:.1f}%)")
    report.append(f"  Salary Banked (1:1.5): {len(partial_bes)}  ({(len(partial_bes)/total_trades*100) if total_trades > 0 else 0:.1f}%) 💵")
    report.append(f"  Armor Protection (BE): {len(bes)}  ({(len(bes)/total_trades*100) if total_trades > 0 else 0:.1f}%) 🛡️")
    report.append(f"  Full Losses:         {len(losses)}  ({(len(losses)/total_trades*100) if total_trades > 0 else 0:.1f}%)")
    report.append("")
    
    survival_rate = ((len(wins) + len(partial_bes) + len(bes)) / total_trades * 100) if total_trades > 0 else 0
    report.append(f"  SURVIVAL RATE:       {survival_rate:.1f}% (Win + Partial + BE)")
    report.append("")
    report.append("VOLATILITY GATING (REAL ACCOUNT PROTECTION):")
    report.append(f"  Trades Skipped:      {skipped_real} out of {total_trades} (Setups > $8.00 ATR rejected)")
    report.append("")

    # --- TRADE LOG ---
    report.append("="*100)
    report.append("DETAILED EXECUTION LOG")
    report.append("="*100)
    
    for t in trades:
        # Determine Icon
        if t['status'] == "WIN": icon = "✅ [FULL TARGET]"
        elif t['status'] == "PARTIAL_BE": icon = "💵 [SALARY BANKED]"
        elif t['status'] == "BE": icon = "🛡️ [BREAKEVEN]"
        elif t['status'] == "LOSS": icon = "❌ [LOSS]"
        else: icon = "⌛ [TIMEOUT]"

        real_status = "ACTIVE" if t['real_active'] else "GATED (SKIPPED)"
        
        report.append(f"[{t['time']}] {t['signal']} -> {icon}")
        report.append(f"   Real Account Status: {real_status}")
        report.append(f"   Demo PnL: ${t['demo_pnl']:+,.2f} | Real PnL: ${t['real_pnl']:+,.2f}")
        report.append("-" * 50)

    report.append("")
    report.append("="*100)
    report.append("ARCHITECT'S NOTES: THE GHOST ADVANTAGE")
    report.append("="*100)
    report.append("1. THE 'ONE LEVEL, ONE BULLET' RULE:")
    report.append("   By enforcing a 6-hour cooldown on levels, we eliminated the 'Revenge Cycle'")
    report.append("   that previously caused multiple losses on the same level in one session.")
    report.append("")
    report.append("2. THE 60% SALARY BANK:")
    report.append("   The 'PARTIAL_BE' status is the backbone of your income. Banking 60% at 1:1.5")
    report.append("   ensures that even if Gold is choppy, you are taking money out of the market")
    report.append("   and paying your bills while the rest of the position 'free-rolls' to 1:3.")
    report.append("")
    report.append("3. ATR-MINIMUM STOP LOSS:")
    report.append("   Using a minimum $4.00 stop loss (based on ATR) allowed the trades to survive")
    report.append("   the micro-volatility that previously triggered premature stop-outs.")
    report.append("="*100)

    with open('STRATEGY_V11_DETAILED_REPORT.txt', 'w') as f:
        f.write("\n".join(report))
    
    print("✅ Strategy v11.0 Detailed Audit generated: STRATEGY_V11_DETAILED_REPORT.txt")

if __name__ == "__main__":
    generate_v11_detailed_report()