import { Outlet } from "react-router-dom/dist"
import ScrollToTop from "../components/ui/ScrollToTop"
import { Navbar } from "../components/layout/Navbar"
import { Footer } from "../components/layout/Footer"

export const Layout = () => {
    return (
        <ScrollToTop>
            <Navbar />
                <Outlet />
            <Footer />
        </ScrollToTop>
    )
}