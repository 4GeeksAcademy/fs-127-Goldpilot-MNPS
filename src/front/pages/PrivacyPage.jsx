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

export const PrivacyPage = () => {
    
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
                                    Privacy <br className="md:hidden" /> Policy
                                </h1>
                                <Text className="text-gray-500 text-sm font-mono">
                                    Last updated: March 2026
                                </Text>
                            </div>

                            {/* Banner de Compromiso */}
                            <div className="mb-16 p-8 rounded-[24px] border border-white/10 bg-white/[0.02]">
                                <Text className="text-gray-300 text-lg leading-relaxed font-light text-center md:text-left">
                                    At XSNIPER, we are committed to protecting your privacy. This policy explains how we handle your information, specifically regarding our non-custodial architecture and third-party integrations.
                                </Text>
                            </div>

                            <div className="prose prose-invert max-w-none">
                                <Section title="1. Information We Collect">
                                    <p>
                                        We collect only the minimum data necessary to provide our algorithmic execution services:
                                    </p>
                                    <ul className="list-none pl-0 space-y-3">
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Account information: Email address and basic profile data provided during registration.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Connection data: MetaAPI-assigned account identifiers used to sync your trading strategies.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Technical logs: IP addresses, browser types, and usage patterns for security monitoring.</li>
                                    </ul>
                                </Section>

                                <Section title="2. MetaAPI & Trading Credentials">
                                    <p>
                                        Our commitment to security is absolute regarding your trading credentials:
                                    </p>
                                    <ul className="list-none pl-0 space-y-3">
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> XSNIPER does not store your MT4/MT5 passwords on its own servers.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> All credentials provided during the connection process are transmitted via encrypted tunnels directly to MetaAPI.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> We only retain "tokens" or identifiers that allow our algorithms to send execution commands without ever seeing your primary passwords.</li>
                                    </ul>
                                </Section>

                                <Section title="3. How We Use Your Data">
                                    <p>Your data is used strictly for:</p>
                                    <ul className="list-none pl-0 space-y-3">
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Maintaining and optimizing the connection between our algorithms and your account.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Sending critical alerts regarding strategy performance or connectivity issues.</li>
                                        <li className="flex gap-3"><span className="text-[var(--color-gold)]">▸</span> Preventing fraudulent activity and ensuring the integrity of the XSNIPER Engine.</li>
                                    </ul>
                                </Section>

                                <Section title="4. Data Sharing & Third Parties">
                                    <p>
                                        We do not sell, rent, or trade your personal information. Data is only shared with third-party service providers (like MetaAPI or infrastructure hosts) as strictly necessary to operate the service. All partners are required to maintain the same level of encryption and security standards as XSNIPER.
                                    </p>
                                </Section>

                                <Section title="5. Data Retention">
                                    <p>
                                        We retain your information as long as your account is active. If you choose to delete your XSNIPER account, we will purge your personal data and disconnect all API bridges from our system within 30 days, except where legal obligations require longer retention.
                                    </p>
                                </Section>

                                <Section title="6. Your Rights">
                                    <p>
                                        You have the right to access, correct, or delete your personal data at any time. You can also request a copy of the data we hold about you by contacting our privacy team.
                                    </p>
                                </Section>

                                <Section title="7. Cookies & Tracking">
                                    <p>
                                        We use essential cookies to maintain your session and security. We do not use third-party advertising trackers that follow your activity across other websites.
                                    </p>
                                </Section>

                                <Section title="8. Policy Updates">
                                    <p>
                                        We may update this Privacy Policy to reflect changes in our technology or legal requirements. We will notify you of any significant changes via the email address associated with your account.
                                    </p>
                                </Section>

                                <Section title="9. Contact Us">
                                    <p>
                                        For questions regarding your privacy and data protection, please reach out to:{" "}
                                        <a href="mailto:privacy@xsniper.com" className="text-[var(--color-gold)] hover:text-white transition-colors">
                                            privacy@xsniper.com
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

export default PrivacyPage;