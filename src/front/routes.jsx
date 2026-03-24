import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
} from "react-router-dom";
import { lazy, Suspense } from "react";

// Always-loaded (critical path)
import { Layout } from "./pages/Layout";
import { Single } from "./pages/Single";
import { Demo } from "./pages/Demo";
import { Home } from "./pages/Home";
import LandingPage from "./features/Landing/LandingPage";
import SignupSignin from "./components/auth/SignupSignin";
import VerifyEmail from "./pages/VerifyEmail";
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";
import { DashboardLayout } from "./features/Dashboard/DashboardLayout";

// Dashboard pages — lazy loaded (each becomes its own chunk)
const DashboardHome       = lazy(() => import("./features/Dashboard/pages/DashboardHome").then(m => ({ default: m.DashboardHome })));
const HistorialPage       = lazy(() => import("./features/Dashboard/pages/HistorialPage").then(m => ({ default: m.HistorialPage })));
const WalletsPage         = lazy(() => import("./features/Dashboard/pages/WalletsPage").then(m => ({ default: m.WalletsPage })));
const BotControlPage      = lazy(() => import("./features/Dashboard/pages/BotControlPage").then(m => ({ default: m.BotControlPage })));
const SettingsPage        = lazy(() => import("./features/Dashboard/pages/SettingsPage").then(m => ({ default: m.SettingsPage })));
const InvestorLevelPage   = lazy(() => import("./features/Dashboard/pages/InvestorLevelPage").then(m => ({ default: m.InvestorLevelPage })));
const DashboardStrategiesPage = lazy(() => import("./features/Dashboard/pages/StrategiesPage").then(m => ({ default: m.StrategiesPage })));

// Public pages — lazy loaded
const TermsAndConditions  = lazy(() => import("./pages/TermsAndConditions"));
const PublicStrategiesPage = lazy(() => import("./pages/PublicStrategiesPage").then(m => ({ default: m.StrategiesPage })));
const SecurityPage        = lazy(() => import("./pages/SecurityPage").then(m => ({ default: m.SecurityPage })));
const PrivacyPage         = lazy(() => import("./pages/PrivacyPage").then(m => ({ default: m.PrivacyPage })));
const ContactPage         = lazy(() => import("./pages/ContactPage").then(m => ({ default: m.ContactPage })));
const AboutUsPage         = lazy(() => import("./pages/AboutUsPage").then(m => ({ default: m.AboutUsPage })));
const PressPage           = lazy(() => import("./pages/PressPage").then(m => ({ default: m.PressPage })));
const CookiesPage         = lazy(() => import("./pages/CookiesPage").then(m => ({ default: m.CookiesPage })));

const PageLoader = () => (
  <div className="flex items-center justify-center min-h-screen">
    <div className="w-6 h-6 rounded-full border-2 border-t-transparent animate-spin" style={{ borderColor: "var(--color-gold)", borderTopColor: "transparent" }} />
  </div>
);

const S = ({ children }) => <Suspense fallback={<PageLoader />}>{children}</Suspense>;

export const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      {/* RUTAS PÚBLICAS / LANDING */}
      <Route path="/" element={<LandingPage />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/login" element={<SignupSignin />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/signup" element={<SignupSignin />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/verify" element={<VerifyEmail />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/forgot-password" element={<ForgotPassword />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/reset-password" element={<ResetPassword />} errorElement={<h1>No encontrado!</h1>} />

      {/* SECCIÓN INFORMATIVA PÚBLICA */}
      <Route path="/strategies" element={<S><PublicStrategiesPage /></S>} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/security"   element={<S><SecurityPage /></S>} />
      <Route path="/privacy"    element={<S><PrivacyPage /></S>} />
      <Route path="/terms"      element={<S><TermsAndConditions /></S>} />
      <Route path="/cookies"    element={<S><CookiesPage /></S>} />
      <Route path="/contact"    element={<S><ContactPage /></S>} />
      <Route path="/about"      element={<S><AboutUsPage /></S>} />
      <Route path="/press"      element={<S><PressPage /></S>} />

      {/* RUTAS DEL DASHBOARD (Privadas) */}
      <Route path="/dashboard" element={<DashboardLayout />} errorElement={<h1>No encontrado!</h1>}>
        <Route index element={<S><DashboardHome /></S>} />
        <Route path="strategies"    element={<S><DashboardStrategiesPage /></S>} />
        <Route path="historial"     element={<S><HistorialPage /></S>} />
        <Route path="wallets"       element={<S><WalletsPage /></S>} />
        <Route path="bot-control"   element={<S><BotControlPage /></S>} />
        <Route path="ajustes"       element={<S><SettingsPage /></S>} />
        <Route path="nivel-inversor" element={<S><InvestorLevelPage /></S>} />
      </Route>

      {/* OTRAS RUTAS CON EL LAYOUT GENERAL */}
      <Route element={<Layout />} errorElement={<h1>No encontrado!</h1>}>
        <Route path="/home" element={<Home />} />
        <Route path="/single/:theId" element={<Single />} />
        <Route path="/demo" element={<Demo />} />
      </Route>
    </>
  )
);