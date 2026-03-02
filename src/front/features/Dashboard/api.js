const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

const parseError = async (response) => {
    try {
        const json = await response.json();
        return json.description || json.msg || json.message || "Error inesperado";
    } catch {
        return "Error inesperado";
    }
};

export const getBotStatus = async () => {
    const token = localStorage.getItem("token");
    const response = await fetch(`${BACKEND_URL}/api/bot/status`, {
        headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) {
        const msg = await parseError(response);
        throw new Error(msg);
    }
    return response.json();
};

export const startBot = async () => {
    const token = localStorage.getItem("token");
    const response = await fetch(`${BACKEND_URL}/api/bot/start`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) {
        const msg = await parseError(response);
        throw new Error(msg);
    }
    return response.json();
};

export const stopBot = async () => {
    const token = localStorage.getItem("token");
    const response = await fetch(`${BACKEND_URL}/api/bot/stop`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) {
        const msg = await parseError(response);
        throw new Error(msg);
    }
    return response.json();
};

export const connectAccount = async (data) => {
    const token = localStorage.getItem("token");
    const response = await fetch(`${BACKEND_URL}/api/bot/connect`, {
        method: "POST",
        headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        const msg = await parseError(response);
        throw new Error(msg);
    }
    return response.json();
};

export const updateBotStrategy = async (strategyId) => {
    const token = localStorage.getItem("token");
    const response = await fetch(`${BACKEND_URL}/api/bot/strategy`, {
        method: "POST",
        headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ strategy: strategyId }),
    });
    if (!response.ok) {
        const msg = await parseError(response);
        throw new Error(msg);
    }
    return response.json();
};