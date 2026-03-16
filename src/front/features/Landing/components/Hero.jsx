import React, { useRef } from "react";
import sovereignVideo from "../../../assets/img/K_Video_for_Website_Login.mp4";

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
                    loop
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
        </section>
    );
};
