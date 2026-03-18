import React, { useEffect } from "react";
import { Theme, Container, Text } from "@radix-ui/themes";
import "@radix-ui/themes/styles.css";
import { motion } from "framer-motion";
import { Navbar } from "../features/Landing/components/Navbar";
import { Footer } from "../features/Landing/components/Footer";

const Section = ({ title, children }) => (
    <div className="mb-14">
        <h2 className="text-2xl font-bold text-white mb-6 tracking-tight">{title}</h2>
        <div className="text-gray-400 text-lg leading-relaxed font-light space-y-4">{children}</div>
    </div>
);

export const CookiesPage = () => {
    
    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    return (
        <Theme appearance="dark" accentColor="amber" grayColor="slate" panelBackground="translucent" radius="large">
            <div className="min-h-screen bg-black text-white selection:bg-[#D4AF37] selection:text-black font-sans">
                <Navbar />

                <main>
                    <Container size="3" className="pt-48 pb-20 px-6">
                        
                        <motion.div 
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.8 }}
                            className="max-w-4xl mx-auto"
                        >
                            {/* Header Institucional */}
                            <div className="mb-16 border-b border-white/10 pb-12 text-center md:text-left">
                                <Text className="text-[var(--color-gold)] font-bold text-sm uppercase tracking-widest mb-4 block">
                                    Legal
                                </Text>
                                <h1 className="text-5xl md:text-6xl font-black tracking-tighter text-white mb-6">
                                    Cookie <br className="md:hidden" /> Policy
                                </h1>
                                <Text className="text-gray-500 text-sm font-mono">
                                    Last updated: March 2026
                                </Text>
                            </div>

                            <div className="prose prose-invert max-w-none">
                                <Section title="1. What Are Cookies?">
                                    <p>
                                        Cookies are small text files stored on your device when you visit a website. They help us provide a secure and functional experience, ensuring that the XSNIPER Engine operates correctly during your session.
                                    </p>
                                </Section>

                                <Section title="2. How We Use Cookies">
                                    <p>
                                        XSNIPER uses cookies strictly for technical and security purposes. We do not use them for behavioral advertising or cross-site tracking. The cookies we use fall into the following categories:
                                    </p>
                                    <ul className="list-none pl-0 space-y-3">
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Essential Cookies: Required for secure login, session maintenance, and protecting against CSRF attacks.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Preference Cookies: Used to remember your dashboard settings, such as theme selection or chart configurations.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Analytics: Minimal, anonymous data to understand platform performance and latency issues.</li>
                                    </ul>
                                </Section>

                                <Section title="3. Third-Party Cookies">
                                    <p>
                                        In some cases, we use trusted third-party services like Cloudflare for DDoS protection and MetaAPI for trading connectivity. These providers may set their own cookies to ensure the security and reliability of their integrated services.
                                    </p>
                                </Section>

                                <Section title="4. Managing Cookies">
                                    <p>
                                        You can choose to disable cookies through your browser settings. However, please note that disabling essential cookies will prevent you from logging into the XSNIPER Dashboard and will break the connection to our trading algorithms.
                                    </p>
                                </Section>

                                <Section title="5. Consent">
                                    <p>
                                        By using our platform, you consent to the use of essential cookies necessary for the operation and security of the XSNIPER Engine.
                                    </p>
                                </Section>

                                <Section title="6. Contact">
                                    <p>
                                        For further information regarding our use of cookies, please contact us at: <a href="mailto:legal@xsniper.com" className="text-[var(--color-gold)] hover:text-white transition-colors">legal@xsniper.com</a>
                                    </p>
                                </Section>
                            </div>
                        </motion.div>
                    </Container>
                </main>

                <Footer />
            </div>
        </Theme>
    );
};

export default CookiesPage;