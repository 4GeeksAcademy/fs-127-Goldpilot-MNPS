import pandas as pd
from src.api.strategies import LowRiskStrategy, MediumRiskStrategy, HighRiskStrategy

def ejecutar_test():
    print("🚀 INICIANDO TEST GENERAL DE ESTRATEGIAS...\n")

    # 1. Crear datos simulados
    print("📊 Generando datos simulados (Oro, Dólar y Nasdaq)...")
    fechas = pd.date_range(start="2026-01-01", periods=50, freq="h")
    
    gold_fake = pd.DataFrame({
        "close": [1900 + i for i in range(50)],
        "high": [1905 + i for i in range(50)],
        "low": [1895 + i for i in range(50)]
    }, index=fechas)

    dxy_fake = pd.DataFrame({
        "close": [105 - (i*0.1) for i in range(50)]
    }, index=fechas)

    nasdaq_fake = pd.DataFrame({
        "close": [15000 + (i*10) for i in range(50)]
    }, index=fechas)

    # 2. Instanciar los bots
    print("🤖 Cargando los 3 cerebros de trading...\n")
    bot_low = LowRiskStrategy()
    bot_medium = MediumRiskStrategy()
    bot_high = HighRiskStrategy()

    # 3. Ejecutar análisis
    print("--- 🟢 LOW RISK STRATEGY (Macro: Oro + Nasdaq + DXY) ---")
    try:
        # Le pasamos los 3 DataFrames que necesita
        resultado_low = bot_low.analyze(gold_fake, nasdaq_fake, dxy_fake)
        print(f"Decisión: {resultado_low.get('action')}")
        print(f"Detalles: {resultado_low}")
    except Exception as e:
        print(f"❌ Error en Low Risk: {e}")

    print("\n--- 🟡 MEDIUM RISK STRATEGY (Técnico: Fibo + RSI) ---")
    try:
        resultado_medium = bot_medium.analyze(gold_fake, dxy_fake)
        print(f"Decisión: {resultado_medium.get('action')}")
        print(f"Detalles: {resultado_medium}")
    except Exception as e:
        print(f"❌ Error en Medium Risk: {e}")

    print("\n--- 🔴 HIGH RISK STRATEGY (Acción del Precio: Breakout) ---")
    try:
        resultado_high = bot_high.analyze(gold_fake)
        print(f"Decisión: {resultado_high.get('action')}")
        print(f"Detalles: {resultado_high}")
    except Exception as e:
        print(f"❌ Error en High Risk: {e}")

    print("\n✅ TEST FINALIZADO.")

if __name__ == "__main__":
    ejecutar_test()