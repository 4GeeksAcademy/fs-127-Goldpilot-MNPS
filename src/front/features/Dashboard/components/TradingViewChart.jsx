import React, { useEffect, useRef, useState } from "react";
import { createChart, CandlestickSeries } from "lightweight-charts";

/** Intervalos disponibles y su equivalente en segundos para spacing de mock data */
const INTERVALS = ["1H", "4H", "1D", "1W"];

/**
 * Genera velas (candlestick) mock para XAUUSD en el rango de precio del oro (~2000-2100 USD).
 * @param {number} count - Número de velas
 * @param {number} intervalSecs - Espaciado temporal entre velas en segundos
 */
const generateXauusdCandles = (count = 80, intervalSecs = 3600) => {
    const candles = [];
    let base = 2050;
    const now = Math.floor(Date.now() / 1000);

    for (let i = count; i >= 0; i--) {
        const open = base + (Math.random() - 0.5) * 15;
        const close = open + (Math.random() - 0.5) * 12;
        const high = Math.max(open, close) + Math.random() * 6;
        const low = Math.min(open, close) - Math.random() * 6;

        candles.push({
            time: now - i * intervalSecs,
            open: parseFloat(open.toFixed(2)),
            high: parseFloat(high.toFixed(2)),
            low: parseFloat(low.toFixed(2)),
            close: parseFloat(close.toFixed(2)),
        });
        base = close;
    }

    return candles;
};

/** Mapeo de intervalo de UI → segundos para el mock de datos */
const INTERVAL_SECS = { "1H": 3600, "4H": 14400, "1D": 86400, "1W": 604800 };

/**
 * Gráfico de velas (candlestick) para el par XAUUSD (Oro / USD).
 * Usa Lightweight Charts con el sistema de diseño "Liquid Glass" del proyecto.
 * TODO: Conectar con endpoint real GET /api/market/candles?symbol=XAUUSD&interval=1H
 */
export const TradingViewChart = () => {
    const chartContainerRef = useRef(null);
    const chartRef = useRef(null);
    const seriesRef = useRef(null);
    const [activeInterval, setActiveInterval] = useState("1H");
    const [lastCandle, setLastCandle] = useState(null);

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
            rightPriceScale: { borderColor: "rgba(255, 255, 255, 0.08)" },
            timeScale: {
                borderColor: "rgba(255, 255, 255, 0.08)",
                timeVisible: true,
                secondsVisible: false,
            },
        });

        chartRef.current = chart;

        const candleSeries = chart.addSeries(CandlestickSeries, {
            upColor: "#c38f37",
            downColor: "#564535",
            borderVisible: false,
            wickUpColor: "#c38f37",
            wickDownColor: "#7a6050",
        });

        seriesRef.current = candleSeries;

        const data = generateXauusdCandles(80, INTERVAL_SECS["1H"]);
        candleSeries.setData(data);
        setLastCandle(data[data.length - 1]);
        chart.timeScale().fitContent();

        const resizeObserver = new ResizeObserver((entries) => {
            const { width, height } = entries[0].contentRect;
            chart.applyOptions({ width, height });
        });

        resizeObserver.observe(container);

        return () => {
            resizeObserver.disconnect();
            chart.remove();
        };
    }, []);

    /** Actualiza los datos al cambiar el intervalo seleccionado */
    const handleIntervalChange = (interval) => {
        setActiveInterval(interval);
        if (seriesRef.current) {
            const secs = INTERVAL_SECS[interval] ?? 3600;
            const data = generateXauusdCandles(80, secs);
            seriesRef.current.setData(data);
            setLastCandle(data[data.length - 1]);
            chartRef.current?.timeScale().fitContent();
        }
    };

    const priceChange = lastCandle ? (lastCandle.close - lastCandle.open) : 0;
    const priceChangePct = lastCandle ? ((priceChange / lastCandle.open) * 100) : 0;
    const isPositive = priceChange >= 0;

    return (
        <div className="w-full flex flex-col gap-4">
            {/* Cabecera del gráfico */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                    <div className="flex items-center gap-2">
                        <span className="text-xs font-bold px-2 py-0.5 rounded-full"
                            style={{ background: "rgba(195,143,55,0.15)", color: "var(--color-gold)" }}>
                            XAUUSD
                        </span>
                        <span className="text-2xl font-bold text-white tracking-tight">
                            {lastCandle ? lastCandle.close.toFixed(2) : "2,050.00"}
                        </span>
                        <span className="text-white/40 text-sm">USD</span>
                    </div>
                    <p className="text-sm font-medium mt-0.5"
                        style={{ color: isPositive ? "var(--color-olive)" : "#f87171" }}>
                        {isPositive ? "+" : ""}{priceChange.toFixed(2)} ({isPositive ? "+" : ""}{priceChangePct.toFixed(2)}%)
                    </p>
                </div>

                {/* Selector de intervalo */}
                <div className="flex gap-2">
                    {INTERVALS.map((interval) => (
                        <button
                            key={interval}
                            onClick={() => handleIntervalChange(interval)}
                            className="px-3 py-1 rounded-lg text-xs font-medium transition-all"
                            style={activeInterval === interval
                                ? { background: "var(--color-gold)", color: "#1a1005" }
                                : { background: "rgba(255,255,255,0.05)", color: "rgba(255,255,255,0.5)" }
                            }
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
