import { useEffect, useRef, memo } from "react";

/**
 * @param {string} symbol - Par de trading (default: 'OANDA:XAUUSD')
 * @param {string} theme - Tema visual: 'dark' | 'light' (default: 'dark')
 */
const TradingViewWidget = ({ symbol = "OANDA:XAUUSD", theme = "dark" }) => {
    const containerRef = useRef(null);

    useEffect(() => {
        if (!containerRef.current) return;

        containerRef.current.innerHTML = "";

        const script = document.createElement("script");
        script.src = "https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js";
        script.type = "text/javascript";
        script.async = true;
        script.innerHTML = JSON.stringify({
            autosize: true,
            symbol,
            interval: "60",
            timezone: "Etc/UTC",
            theme,
            style: "1",
            locale: "es",
            enable_publishing: false,
            allow_symbol_change: true,
            calendar: false,
            support_host: "https://www.tradingview.com",
            hide_side_toolbar: false,
            details: true,
            hotlist: false,
            backgroundColor: "rgba(0, 0, 0, 0)",
        });

        containerRef.current.appendChild(script);

        return () => {
            if (containerRef.current) {
                containerRef.current.innerHTML = "";
            }
        };
    }, [symbol, theme]);

    return (
        <div className="tradingview-widget-container" style={{ height: "100%", width: "100%" }}>
            <div
                ref={containerRef}
                className="tradingview-widget-container__widget"
                style={{ height: "100%", width: "100%" }}
            />
        </div>
    );
};

export const TradingViewChart = memo(() => (
    <div className="w-full h-[500px]">
        <TradingViewWidget symbol="OANDA:XAUUSD" theme="dark" />
    </div>
));

TradingViewChart.displayName = "TradingViewChart";
