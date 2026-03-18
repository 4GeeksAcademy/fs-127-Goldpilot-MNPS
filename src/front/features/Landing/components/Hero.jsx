import { useRef } from "react";
import sovereignVideo from "../../../assets/img/Sovereign_Vault_Luxury_Industrial_Reveal.mp4";

export const Hero = () => {
    const videoRef = useRef(null);

    const handleEnded = () => {
        const v = videoRef.current;
        if (v) {
            v.currentTime = v.duration - 0.001;
            v.pause();
        }
    };

    return (
        <section className="relative w-full flex items-center justify-center overflow-hidden bg-[var(--color-brown-dark)]"
            style={{ height: "100svh" }}>
            <div className="absolute inset-0 z-0">
                <video
                    ref={videoRef}
                    autoPlay
                    muted
                    playsInline
                    webkit-playsinline="true"
                    onEnded={handleEnded}
                    className="absolute inset-0 w-full h-full object-cover opacity-90 mix-blend-luminosity"
                >
                    <source src={sovereignVideo} type="video/mp4" />
                </video>

                <div className="absolute inset-0 bg-[var(--color-brown-dark)] mix-blend-color z-10 opacity-60" />

                <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_20%,var(--color-brown-dark)_100%)] z-20 opacity-90" />

                <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,var(--color-gold)_0%,transparent_40%)] z-20 mix-blend-overlay opacity-20" />

                <div className="absolute bottom-0 left-0 right-0 h-64 bg-gradient-to-t from-[var(--color-brown-dark)] to-transparent z-30" />
            </div>

            {/* Scroll arrow */}
            <div className="absolute bottom-10 left-1/2 -translate-x-1/2 z-40 flex flex-col items-center"
                style={{ animation: "scrollBounce 1.8s ease-in-out infinite" }}>
                <div
                    className="flex items-center justify-center"
                    style={{
                        width: 56,
                        height: 56,
                        borderRadius: "50%",
                        background: "rgba(255,255,255,0.06)",
                        backdropFilter: "blur(16px)",
                        WebkitBackdropFilter: "blur(16px)",
                        border: "1px solid rgba(255,255,255,0.15)",
                        boxShadow: "0 4px 24px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.12)",
                    }}
                >
                    <svg
                        width="22" height="14" viewBox="0 0 32 18" fill="none"
                        style={{ color: "var(--color-gold)" }}
                    >
                        <path d="M1 1L16 16L31 1" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                </div>
            </div>

            <style>{`
                @keyframes scrollBounce {
                    0%, 100% { transform: translateX(-50%) translateY(0); opacity: 0.8; }
                    50% { transform: translateX(-50%) translateY(7px); opacity: 1; }
                }
            `}</style>
        </section>
    );
};
