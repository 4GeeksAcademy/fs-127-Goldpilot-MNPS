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
import ChangePassword from "./pages/ChangePassword";
import ConfirmPasswordChange from "./pages/ConfirmPasswordChange";

export const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route path="/" element={<LandingPage />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/login" element={<SignupSignin />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/signup" element={<SignupSignin />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/verify" element={<VerifyEmail />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/change-password" element={<ChangePassword />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/confirm-password-change" element={<ConfirmPasswordChange />} errorElement={<h1>No encontrado!</h1>} />
      <Route path="/dashboard" element={<DashboardLayout />} errorElement={<h1>No encontrado!</h1>}>
        <Route index element={<DashboardHome />} />
      </Route>
      <Route element={<Layout />} errorElement={<h1>No encontrado!</h1>} >
        <Route path="/home" element={<Home />} />
        <Route path="/single/:theId" element={<Single />} />
        <Route path="/demo" element={<Demo />} />
      </Route>
    </>
  )
);
