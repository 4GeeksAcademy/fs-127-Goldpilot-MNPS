const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

const parseError = async (response) => {
    try {
        const json = await response.json();
        return json.description || json.msg || json.message || "Error inesperado";
    } catch {
        return "Error inesperado";
    }
};

export const authServices = {
    signup: async (data) => {
        const response = await fetch(`${BACKEND_URL}/api/auth/signup`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            const msg = await parseError(response);
            throw new Error(msg);
        }
        return response.json();
    },

    verifyEmail: async (token) => {
        const response = await fetch(`${BACKEND_URL}/api/auth/verify/${token}`, {
            method: "GET",
        });
        if (!response.ok) {
            const msg = await parseError(response);
            throw new Error(msg);
        }
        return response.json();
    },

    forgotPassword: async (data) => {
        const response = await fetch(`${BACKEND_URL}/api/auth/forgot-password`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            const msg = await parseError(response);
            throw new Error(msg);
        }
        return response.json();
    },

    resetPassword: async (data) => {
        const response = await fetch(`${BACKEND_URL}/api/auth/reset-password`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            const msg = await parseError(response);
            throw new Error(msg);
        }
        return response.json();
    },

    login: async (data) => {
        const response = await fetch(`${BACKEND_URL}/api/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            const msg = await parseError(response);
            throw new Error(msg);
        }
        return response.json();
    },
};
