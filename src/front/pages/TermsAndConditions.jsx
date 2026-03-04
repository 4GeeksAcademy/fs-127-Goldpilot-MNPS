import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

const Section = ({ title, children }) => (
    <div className="mb-10">
        <h2 className="text-lg font-semibold text-[var(--color-gold)] mb-3 uppercase tracking-wide">{title}</h2>
        <div className="text-white/60 text-sm leading-relaxed space-y-3">{children}</div>
    </div>
);

const TermsAndConditions = () => {
    return (
        <div className="min-h-screen bg-[var(--color-brown-dark)] text-white px-6 py-16">

            <div className="max-w-3xl mx-auto">

                {/* Back */}
                <Link to="/"
                    className="inline-flex items-center gap-2 text-white/40 hover:text-[var(--color-gold)] transition-colors text-sm mb-12">
                    <ArrowLeft size={14} /> Back to Home
                </Link>

                {/* Header */}
                <div className="mb-12 border-b border-white/10 pb-10">
                    <div className="flex items-center gap-2 mb-6">
                        <div className="w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold text-black"
                            style={{ background: "var(--gradient-gold)" }}>XS</div>
                        <span className="font-bold tracking-tight text-white text-lg">XSNIPER</span>
                    </div>
                    <h1 className="text-4xl font-bold tracking-tight mb-3">Terms &amp; Conditions</h1>
                    <p className="text-white/40 text-sm">Last updated: March 2025</p>
                </div>

                {/* Important disclaimer banner */}
                <div className="mb-10 p-5 rounded-2xl border border-[var(--color-gold)]/30 bg-[var(--color-gold)]/5 text-sm text-[var(--color-gold)]/80 leading-relaxed">
                    <strong className="text-[var(--color-gold)]">Important:</strong> Xsniper is an automated trading algorithm provider. We are <strong>not</strong> a financial institution, broker, or investment advisor. We do <strong>not</strong> hold, manage, or have any access to your funds, and we do <strong>not</strong> have access to withdrawal functions on your trading account.
                </div>

                <Section title="1. Nature of Service">
                    <p>
                        Xsniper provides automated trading algorithm software that connects to your MetaTrader 4 (MT4) or MetaTrader 5 (MT5) account via the MetaAPI service. Our platform allows you to run pre-configured algorithmic trading strategies on your existing brokerage account.
                    </p>
                    <p>
                        We are a <strong className="text-white/80">software and technology provider only</strong>. We do not provide financial advice, investment recommendations, or brokerage services of any kind. Nothing on this platform constitutes financial advice.
                    </p>
                </Section>

                <Section title="2. No Access to Funds or Withdrawals">
                    <p>
                        Xsniper does <strong className="text-white/80">not</strong> have access to your funds at any time. Specifically:
                    </p>
                    <ul className="list-disc pl-5 space-y-2">
                        <li>We cannot initiate deposits or withdrawals from your trading account.</li>
                        <li>We cannot transfer funds between accounts.</li>
                        <li>We do not hold your money, act as a custodian, or operate as a payment service provider.</li>
                        <li>All funds remain in your trading account at your broker at all times.</li>
                    </ul>
                    <p>
                        Your capital is entirely under your control and your broker's custody. Xsniper only places and manages trades within your account according to the algorithm you select.
                    </p>
                </Section>

                <Section title="3. Account Credentials &amp; Security">
                    <p>
                        Xsniper connects to your trading account via <strong className="text-white/80">MetaAPI</strong>, a third-party intermediary service. During the connection process:
                    </p>
                    <ul className="list-disc pl-5 space-y-2">
                        <li>We do <strong className="text-white/80">not</strong> store your MT4/MT5 account password at any point. Credentials are transmitted directly to MetaAPI and are not retained on our servers.</li>
                        <li>We store only a MetaAPI-assigned account identifier to reference your connected account.</li>
                        <li>You are solely responsible for maintaining the security of your broker login credentials.</li>
                    </ul>
                    <p>
                        You should never share your broker account password with any party. If you believe your credentials have been compromised, contact your broker immediately.
                    </p>
                </Section>

                <Section title="4. Trading Risk Disclaimer">
                    <p>
                        Trading foreign exchange (Forex), commodities (including gold/XAUUSD), and other financial instruments involves <strong className="text-white/80">substantial risk of loss</strong> and is not suitable for all investors. You should carefully consider your financial situation and risk tolerance before using any automated trading strategy.
                    </p>
                    <ul className="list-disc pl-5 space-y-2">
                        <li>Past performance of any algorithm or strategy does not guarantee future results.</li>
                        <li>You may lose some or all of your invested capital.</li>
                        <li>Automated trading does not eliminate market risk.</li>
                        <li>Market conditions, slippage, and connectivity issues may affect algorithm performance.</li>
                    </ul>
                    <p>
                        By using Xsniper, you acknowledge that you understand and accept these risks.
                    </p>
                </Section>

                <Section title="5. Eligibility">
                    <p>
                        To use Xsniper you must:
                    </p>
                    <ul className="list-disc pl-5 space-y-2">
                        <li>Be at least <strong className="text-white/80">18 years of age</strong>.</li>
                        <li>Have a valid trading account with a licensed broker.</li>
                        <li>Be legally permitted to trade financial instruments in your jurisdiction.</li>
                        <li>Not be located in a jurisdiction where use of this service is prohibited by law.</li>
                    </ul>
                </Section>

                <Section title="6. Algorithm Performance &amp; No Guarantees">
                    <p>
                        Xsniper makes <strong className="text-white/80">no guarantees</strong> of profit or specific performance from any trading strategy available on the platform. All strategies are provided "as is" based on historical backtesting and defined risk parameters.
                    </p>
                    <p>
                        You select and activate strategies at your own discretion and risk. Xsniper is not liable for any trading losses incurred as a result of using our algorithms.
                    </p>
                </Section>

                <Section title="7. User Responsibilities">
                    <p>By using this platform, you agree to:</p>
                    <ul className="list-disc pl-5 space-y-2">
                        <li>Only connect trading accounts that you own or are legally authorised to operate.</li>
                        <li>Comply with your broker's terms of service regarding the use of automated trading tools.</li>
                        <li>Monitor your account regularly and deactivate strategies if required.</li>
                        <li>Keep your Xsniper account credentials confidential.</li>
                        <li>Provide accurate information during registration.</li>
                    </ul>
                </Section>

                <Section title="8. Limitation of Liability">
                    <p>
                        To the fullest extent permitted by law, Xsniper, its founders, employees, and affiliates shall not be liable for:
                    </p>
                    <ul className="list-disc pl-5 space-y-2">
                        <li>Any trading losses arising from the use of our algorithms.</li>
                        <li>Interruptions or failures in algorithm execution due to connectivity, broker downtime, or platform outages.</li>
                        <li>Actions taken by your broker including account suspension, margin calls, or position closures.</li>
                        <li>Any indirect, incidental, or consequential damages arising from use of the platform.</li>
                    </ul>
                </Section>

                <Section title="9. Modifications to Terms">
                    <p>
                        Xsniper reserves the right to update these Terms &amp; Conditions at any time. Continued use of the platform following notification of changes constitutes acceptance of the revised terms. We recommend reviewing this page periodically.
                    </p>
                </Section>

                <Section title="10. Contact">
                    <p>
                        If you have any questions about these Terms &amp; Conditions, please contact us at: <span className="text-[var(--color-gold)]">legal@xsniper.io</span>
                    </p>
                </Section>

                {/* Bottom */}
                <div className="mt-12 pt-8 border-t border-white/10 text-center text-white/25 text-xs">
                    © 2025 Xsniper Inc. All rights reserved.
                </div>

            </div>
        </div>
    );
};

export default TermsAndConditions;
