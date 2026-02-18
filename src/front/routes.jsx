// Importar componentes y funciones necesarios de react-router-dom.

import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
} from "react-router-dom";
import { Layout } from "./pages/Layout";
import { Single } from "./pages/Single";
import { Demo } from "./pages/Demo";
import LandingPage from "./features/Landing/LandingPage";

export const router = createBrowserRouter(
  createRoutesFromElements(
    // Ruta Raíz: Toda la navegación comenzará desde aquí.
    <>
      <Route path="/" element={<LandingPage />} errorElement={<h1>No encontrado!</h1>} />
      <Route element={<Layout />} errorElement={<h1>No encontrado!</h1>} >
        <Route path="/single/:theId" element={<Single />} />
        <Route path="/demo" element={<Demo />} />
      </Route>
    </>
  )
);