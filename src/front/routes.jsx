import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
} from "react-router-dom";
import { Layout } from "./pages/Layout";
import { Single } from "./pages/Single";
import { Demo } from "./pages/Demo";
import { Home } from "./pages/Home";
import LandingPage from "./features/Landing/LandingPage";
import SignupSignin from "./components/auth/SignupSignin";
import VerifyEmail from "./pages/VerifyEmail";
import { DashboardLayout } from "./features/Dashboard/DashboardLayout";
import { DashboardHome } from "./features/Dashboard/pages/DashboardHome";
import { HistorialPage } from "./features/Dashboard/pages/HistorialPage";
import { WalletsPage } from "./features/Dashboard/pages/WalletsPage";
import { BotControlPage } from "./features/Dashboard/pages/BotControlPage";
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";
import TermsAndConditions from "./pages/TermsAndConditions";
import { SettingsPage } from "./features/Dashboard/pages/SettingsPage";
import { InvestorLevelPage } from "./features/Dashboard/pages/InvestorLevelPage";

// --- IMPORTACIONES DE PÁGINAS DEL DASHBOARD (Usando el formato que funciona) ---
import { SimulationPage } from "./features/Dashboard/pages/SimulationPage";
import { BotTerminalPage } from "./features/Dashboard/pages/BotTerminalPage";

// --- IMPORTACIONES DE PÁGINAS PÚBLICAS ---
import { StrategiesPage as PublicStrategiesPage } from "./pages/PublicStrategiesPage"; 
import { SecurityPage } from "./pages/SecurityPage";
import { PrivacyPage } from "./pages/PrivacyPage";
import { ContactPage } from "./pages/ContactPage";
import { AboutUsPage } from "./pages/AboutUsPage";
import { PressPage } from "./pages/PressPage";
import { CookiesPage } from "./pages/CookiesPage";
import { MetaApiTestPage } from "./pages/MetaApiTestPage"; 

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
      <Route path="/strategies" element={<PublicStrategiesPage />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/security" element={<SecurityPage />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/privacy" element={<PrivacyPage />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/terms" element={<TermsAndConditions />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/cookies" element={<CookiesPage />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/contact" element={<ContactPage />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/about" element={<AboutUsPage />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/press" element={<PressPage />} errorElement={<h1>No encontrado!</h1>} />

      {/* LABORATORIO TÉCNICO */}
      <Route path="/test-metaapi" element={<MetaApiTestPage />} errorElement={<h1>No encontrado!</h1>} />

      {/* RUTAS DEL DASHBOARD (Privadas) */}
      <Route path="/dashboard" element={<DashboardLayout />} errorElement={<h1>No encontrado!</h1>}>
        <Route index element={<DashboardHome />} />
        
        {/* Simulación: Análisis y Backtesting */}
        <Route path="simulacion" element={<SimulationPage />} />
        
        {/* Terminal: Control Real del Bot */}
        <Route path="terminal" element={<BotTerminalPage />} />
        
        <Route path="historial" element={<HistorialPage />} />
        <Route path="wallets" element={<WalletsPage />} />
        <Route path="bot-control" element={<BotControlPage />} />
        <Route path="ajustes" element={<SettingsPage />} />
        <Route path="nivel-inversor" element={<InvestorLevelPage />} />
      </Route>

      {/* OTRAS RUTAS CON EL LAYOUT GENERAL */}
      <Route element={<Layout />} errorElement={<h1>No encontrado!</h1>} >
        <Route path="/home" element={<Home />} />
        <Route path="/single/:theId" element={<Single />} />
        <Route path="/demo" element={<Demo />} />
      </Route>
    </>
  )
);