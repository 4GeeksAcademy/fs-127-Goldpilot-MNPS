import React, { useState } from "react";
import { Theme, Container, Text } from "@radix-ui/themes";
import { Navbar } from "../features/Landing/components/Navbar";

export const MetaApiTestPage = () => {
    const [loading, setLoading] = useState(false);
    const [log, setLog] = useState("");

    const handleTestOrder = async () => {
        setLoading(true);
        setLog("Iniciando conexión con el backend...");
        
        try {
            // 👇 AHORA USA LA VARIABLE DE ENTORNO CORRECTA (Webpack) 👇
            const backendUrl = import.meta.env.VITE_BACKEND_URL;            
            // Verificación por si la variable no está definida en el .env
            if (!backendUrl) {
                throw new Error("La variable BACKEND_URL no está definida en el archivo .env");
            }
            
            const response = await fetch(`${backendUrl}/api/test-trade`, {
                method: "POST",
                headers: { "Content-Type": "application/json" }
            });
            
            const data = await response.json();
            
            if (response.ok && data.status === "success") {
                setLog(`✅ ¡ÉXITO! Operación ejecutada en MetaTrader.\nOrder ID: ${data.orderId}`);
            } else {
                setLog(`❌ ERROR: ${data.message || "Fallo en la conexión"}`);
            }
        } catch (error) {
            console.error("Error en la petición:", error);
            setLog(`❌ ERROR CRÍTICO: No se pudo contactar con el backend. Detalle: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Theme appearance="dark" accentColor="amber" grayColor="slate" panelBackground="translucent">
            <div className="min-h-screen bg-black text-white selection:bg-[#D4AF37] selection:text-black">
                <Navbar />
                
                <main className="pt-52 pb-20 px-6 flex flex-col items-center">
                    <Container size="2" className="text-center mt-10">
                        <h1 className="text-4xl font-black mb-6">LABORATORIO METAAPI</h1>
                        <Text className="text-gray-400 mb-10 block">
                            Usa este botón para enviar una orden de prueba (0.01 lotes) a través de tu backend hacia la cuenta de MetaTrader configurada.
                        </Text>

                        <button 
                            onClick={handleTestOrder}
                            disabled={loading}
                            className="bg-[var(--color-gold)] text-black px-8 py-4 rounded-full font-bold tracking-widest uppercase hover:scale-105 transition-all disabled:opacity-50 disabled:scale-100 mb-8"
                        >
                            {loading ? "ENVIANDO COMANDOS..." : "EJECUTAR OPERACIÓN (PING)"}
                        </button>

                        {/* Consola de logs en pantalla */}
                        <div className="bg-[#0A0A0A] border border-white/10 p-6 rounded-2xl w-full text-left font-mono text-sm h-48 overflow-y-auto">
                            <span className="text-[var(--color-gold)]">x-sniper-terminal:~$</span>
                            <p className="mt-2 text-gray-300 whitespace-pre-wrap">{log || "Esperando instrucciones..."}</p>
                        </div>
                    </Container>
                </main>
            </div>
        </Theme>
    );
};