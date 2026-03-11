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

const TermsAndConditions = () => {
    
    // Forzar scroll al inicio al cargar la página
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
                                    Terms & <br className="md:hidden" /> Conditions
                                </h1>
                                <Text className="text-gray-500 text-sm font-mono">
                                    Last updated: March 2026
                                </Text>
                            </div>

                            {/* Banner Importante */}
                            <div className="mb-16 p-8 rounded-[24px] border border-[var(--color-gold)]/30 bg-[var(--color-gold)]/5">
                                <Text className="text-[var(--color-gold)] text-lg leading-relaxed font-medium">
                                    Important: XSNIPER is an automated trading algorithm provider. We are not a financial institution, broker, or investment advisor. We do not hold, manage, or have any access to your funds, and we do not have access to withdrawal functions on your trading account.
                                </Text>
                            </div>

                            {/* Secciones de Texto en Inglés */}
                            <div className="prose prose-invert max-w-none">
                                <Section title="1. Nature of Service">
                                    <p>
                                        XSNIPER provides automated trading algorithm software that connects to your MetaTrader 4 (MT4) or MetaTrader 5 (MT5) account via the MetaAPI service. Our platform allows you to run pre-configured algorithmic trading strategies on your existing brokerage account.
                                    </p>
                                    <p>
                                        We are a software and technology provider only. We do not provide financial advice, investment recommendations, or brokerage services of any kind. Nothing on this platform constitutes financial advice.
                                    </p>
                                </Section>

                                <Section title="2. No Access to Funds or Withdrawals">
                                    <p>
                                        XSNIPER does not have access to your funds at any time. Specifically:
                                    </p>
                                    <ul className="list-none pl-0 space-y-3">
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> We cannot initiate deposits or withdrawals from your trading account.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> We cannot transfer funds between accounts.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> We do not hold your money, act as a custodian, or operate as a payment service provider.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> All funds remain in your trading account at your broker at all times.</li>
                                    </ul>
                                    <p className="mt-4">
                                        Your capital is entirely under your control and your broker's custody. XSNIPER only places and manages trades within your account according to the algorithm you select.
                                    </p>
                                </Section>

                                <Section title="3. Account Credentials & Security">
                                    <p>
                                        XSNIPER connects to your trading account via MetaAPI, a third-party intermediary service. During the connection process:
                                    </p>
                                    <ul className="list-none pl-0 space-y-3">
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> We do not store your MT4/MT5 account password at any point. Credentials are transmitted directly to MetaAPI and are not retained on our servers.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> We store only a MetaAPI-assigned account identifier to reference your connected account.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> You are solely responsible for maintaining the security of your broker login credentials.</li>
                                    </ul>
                                    <p className="mt-4">
                                        You should never share your broker account password with any party. If you believe your credentials have been compromised, contact your broker immediately.
                                    </p>
                                </Section>

                                <Section title="4. Trading Risk Disclaimer">
                                    <p>
                                        Trading foreign exchange (Forex), commodities (including gold/XAUUSD), and other financial instruments involves substantial risk of loss and is not suitable for all investors. You should carefully consider your financial situation and risk tolerance before using any automated trading strategy.
                                    </p>
                                    <ul className="list-none pl-0 space-y-3">
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Past performance of any algorithm or strategy does not guarantee future results.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> You may lose some or all of your invested capital.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Automated trading does not eliminate market risk.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Market conditions, slippage, and connectivity issues may affect algorithm performance.</li>
                                    </ul>
                                    <p className="mt-4">
                                        By using XSNIPER, you acknowledge that you understand and accept these risks.
                                    </p>
                                </Section>

                                <Section title="5. Eligibility">
                                    <p>To use XSNIPER you must:</p>
                                    <ul className="list-none pl-0 space-y-3">
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Be at least 18 years of age.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Have a valid trading account with a licensed broker.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Be legally permitted to trade financial instruments in your jurisdiction.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Not be located in a jurisdiction where use of this service is prohibited by law.</li>
                                    </ul>
                                </Section>

                                <Section title="6. Algorithm Performance & No Guarantees">
                                    <p>
                                        XSNIPER makes no guarantees of profit or specific performance from any trading strategy available on the platform. All strategies are provided "as is" based on historical backtesting and defined risk parameters.
                                    </p>
                                    <p>
                                        You select and activate strategies at your own discretion and risk. XSNIPER is not liable for any trading losses incurred as a result of using our algorithms.
                                    </p>
                                </Section>

                                <Section title="7. User Responsibilities">
                                    <p>By using this platform, you agree to:</p>
                                    <ul className="list-none pl-0 space-y-3">
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Only connect trading accounts that you own or are legally authorized to operate.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Comply with your broker's terms of service regarding the use of automated trading tools.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Monitor your account regularly and deactivate strategies if required.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Keep your XSNIPER account credentials confidential.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Provide accurate information during registration.</li>
                                    </ul>
                                </Section>

                                <Section title="8. Limitation of Liability">
                                    <p>
                                        To the fullest extent permitted by law, XSNIPER, its founders, employees, and affiliates shall not be liable for:
                                    </p>
                                    <ul className="list-none pl-0 space-y-3">
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Any trading losses arising from the use of our algorithms.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Interruptions or failures in algorithm execution due to connectivity, broker downtime, or platform outages.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Actions taken by your broker including account suspension, margin calls, or position closures.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Any indirect, incidental, or consequential damages arising from use of the platform.</li>
                                    </ul>
                                </Section>

                                <Section title="9. Modifications to Terms">
                                    <p>
                                        XSNIPER reserves the right to update these Terms & Conditions at any time. Continued use of the platform following notification of changes constitutes acceptance of the revised terms. We recommend reviewing this page periodically.
                                    </p>
                                </Section>

                                <Section title="10. Contact">
                                    <p>
                                        If you have any questions about these Terms & Conditions, please contact us at:{" "}
                                        <a href="mailto:legal@xsniper.com" className="text-[var(--color-gold)] hover:text-white transition-colors">
                                            legal@xsniper.com
                                        </a>
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

export default TermsAndConditions;