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
import { DashboardLayout } from "./features/Dashboard/DashboardLayout";
import { DashboardHome } from "./features/Dashboard/pages/DashboardHome";

export const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route path="/" element={<LandingPage />} errorElement={<h1>No encontrado!</h1>} />
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