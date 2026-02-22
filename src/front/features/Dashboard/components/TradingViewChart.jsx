import React, { useEffect, useRef } from "react";
import { createChart, CandlestickSeries } from "lightweight-charts";

/**
 * Genera datos mock de velas (candlestick) para BTC/USD.
 * TODO: Reemplazar con llamada al endpoint real del backend o API de precios.
 * @param {number} count - Número de velas a generar
 * @returns {Array} Array de objetos { time, open, high, low, close }
 */
const generateMockCandles = (count = 80) => {
    const candles = [];
    let base = 42000;
    const now = Math.floor(Date.now() / 1000);

    for (let i = count; i >= 0; i--) {
        const open = base + (Math.random() - 0.5) * 800;
        const close = open + (Math.random() - 0.5) * 600;
        const high = Math.max(open, close) + Math.random() * 300;
        const low = Math.min(open, close) - Math.random() * 300;

        candles.push({
            time: now - i * 900, // Intervalo de 15 minutos
            open: parseFloat(open.toFixed(2)),
            high: parseFloat(high.toFixed(2)),
            low: parseFloat(low.toFixed(2)),
            close: parseFloat(close.toFixed(2)),
        });
        base = close;
    }

    return candles;
};

/**
 * Stub para conexión futura con el backend o API de TradingView.
 * TODO: Conectar con el endpoint real del compañero de backend (ej: GET /api/market/candles).
 */
const fetchChartData = async () => {
    // En producción, aquí irá: const response = await fetch('/api/market/candles?symbol=BTCUSD&interval=15m');
    return generateMockCandles(80);
};

/**
 * Componente principal del gráfico de TradingView (Lightweight Charts).
 * Muestra un gráfico de velas (candlestick) para el par BTC/USD.
 * El diseño está alineado con el sistema de diseño "Liquid Glass" del proyecto.
 */
export const TradingViewChart = () => {
    const chartContainerRef = useRef(null);
    const chartRef = useRef(null);

    useEffect(() => {
        if (!chartContainerRef.current) return;

        const container = chartContainerRef.current;

        const chart = createChart(container, {
            width: container.clientWidth,
            height: container.clientHeight,
            layout: {
                background: { color: "transparent" },
                textColor: "rgba(255, 255, 255, 0.6)",
                fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif",
            },
            grid: {
                vertLines: { color: "rgba(255, 255, 255, 0.04)" },
                horzLines: { color: "rgba(255, 255, 255, 0.04)" },
            },
            crosshair: {
                vertLine: { color: "rgba(195, 143, 55, 0.5)", width: 1, style: 1 },
                horzLine: { color: "rgba(195, 143, 55, 0.5)", width: 1, style: 1 },
            },
            rightPriceScale: {
                borderColor: "rgba(255, 255, 255, 0.08)",
            },
            timeScale: {
                borderColor: "rgba(255, 255, 255, 0.08)",
                timeVisible: true,
                secondsVisible: false,
            },
        });

        chartRef.current = chart;

        const candleSeries = chart.addSeries(CandlestickSeries, {
            upColor: "#c38f37",           // Gold del sistema de diseño
            downColor: "#564535",         // Brown Medium del sistema de diseño
            borderVisible: false,
            wickUpColor: "#c38f37",
            wickDownColor: "#7a6050",
        });

        // Carga inicial de datos
        fetchChartData().then((data) => {
            candleSeries.setData(data);
            chart.timeScale().fitContent();
        });

        // Responsivo: redimensiona el gráfico si cambia el contenedor
        const resizeObserver = new ResizeObserver((entries) => {
            const { width, height } = entries[0].contentRect;
            chart.applyOptions({ width, height });
        });

        resizeObserver.observe(container);

        // Cleanup al desmontar el componente
        return () => {
            resizeObserver.disconnect();
            chart.remove();
        };
    }, []);

    return (
        <div className="w-full flex flex-col gap-4">
            {/* Cabecera del gráfico */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                    <div className="flex items-center gap-2">
                        <span className="text-2xl font-bold text-white tracking-tight">
                            42,350.21
                        </span>
                        <span className="text-white/40 text-sm">USD</span>
                    </div>
                    <p className="text-red-400 text-sm font-medium mt-0.5">
                        −$234.45 (−0.55%)
                    </p>
                </div>
                <div className="flex gap-2">
                    {["1H", "4H", "1D", "1W"].map((interval) => (
                        <button
                            key={interval}
                            className={`px-3 py-1 rounded-lg text-xs font-medium transition-all ${interval === "1H"
                                    ? "bg-[var(--color-gold)] text-black"
                                    : "bg-white/5 text-white/50 hover:bg-white/10"
                                }`}
                        >
                            {interval}
                        </button>
                    ))}
                </div>
            </div>

            {/* Contenedor del gráfico */}
            <div
                ref={chartContainerRef}
                className="w-full h-[380px] rounded-xl overflow-hidden"
            />
        </div>
    );
};
