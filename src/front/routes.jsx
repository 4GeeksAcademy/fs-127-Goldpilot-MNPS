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
import { StrategiesPage } from "./features/Dashboard/pages/StrategiesPage";

export const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route path="/" element={<LandingPage />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/login" element={<SignupSignin />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/signup" element={<SignupSignin />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/verify" element={<VerifyEmail />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/forgot-password" element={<ForgotPassword />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/reset-password" element={<ResetPassword />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/terms" element={<TermsAndConditions />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/dashboard" element={<DashboardLayout />} errorElement={<h1>No encontrado!</h1>}>
        <Route index element={<DashboardHome />} />
        {/* Ruta: Historial de operaciones — HistorialPage (tabla: trades) */}
        <Route path="strategies" element={<StrategiesPage />} />
        <Route path="historial" element={<HistorialPage />} />
        <Route path="wallets" element={<WalletsPage />} />
        <Route path="bot-control" element={<BotControlPage />} />
        <Route path="ajustes" element={<SettingsPage />} />
      </Route>
      <Route element={<Layout />} errorElement={<h1>No encontrado!</h1>} >
        <Route path="/home" element={<Home />} />
        <Route path="/strategies" element={<Home />} />
        <Route path="/single/:theId" element={<Single />} />
        <Route path="/demo" element={<Demo />} />
      </Route>
    </>
  )
);
