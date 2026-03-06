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

export const getWallets = async () => {
  const token = localStorage.getItem("token");
  const response = await fetch(`${BACKEND_URL}/api/wallets`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!response.ok) {
    const msg = await parseError(response);
    throw new Error(msg);
  }
  return response.json();
};

export const addWallet = async (data) => {
  const token = localStorage.getItem("token");
  const response = await fetch(`${BACKEND_URL}/api/wallets`, {
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

export const searchServers = async (query, platform = "mt4") => {
  const token = localStorage.getItem("token");
  const response = await fetch(
    `${BACKEND_URL}/api/wallets/servers?query=${encodeURIComponent(query)}&platform=${platform}`,
    { headers: { Authorization: `Bearer ${token}` } },
  );
  if (!response.ok) return { servers: {} };
  return response.json();
};

export const getWalletBalance = async (walletId) => {
  const token = localStorage.getItem("token");
  const response = await fetch(
    `${BACKEND_URL}/api/wallets/${walletId}/balance`,
    {
      headers: { Authorization: `Bearer ${token}` },
    },
  );
  if (!response.ok) return { balance: null, equity: null, currency: null };
  return response.json();
};

export const syncWallet = async (walletId) => {
  const token = localStorage.getItem("token");
  const response = await fetch(`${BACKEND_URL}/api/wallets/${walletId}/sync`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!response.ok) {
    const msg = await parseError(response);
    throw new Error(msg);
  }
  return response.json();
};

export const getWalletConfigLink = async (walletId) => {
  const token = localStorage.getItem("token");
  const response = await fetch(
    `${BACKEND_URL}/api/wallets/${walletId}/config-link`,
    {
      headers: { Authorization: `Bearer ${token}` },
    },
  );
  if (!response.ok) {
    const msg = await parseError(response);
    throw new Error(msg);
  }
  return response.json();
};

export const deleteWallet = async (walletId) => {
  const token = localStorage.getItem("token");
  const response = await fetch(`${BACKEND_URL}/api/wallets/${walletId}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
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

export const getDashboardSummary = async () => {
  const token = localStorage.getItem("token");
  const response = await fetch(`${BACKEND_URL}/api/dashboard/summary`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!response.ok) {
    const msg = await parseError(response);
    throw new Error(msg);
  }
  return response.json();
};

export const getTradeHistory = async () => {
  const token = localStorage.getItem("token");
  const response = await fetch(`${BACKEND_URL}/api/dashboard/trades/history`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!response.ok) {
    const msg = await parseError(response);
    throw new Error(msg);
  }
  return response.json();
};

/**
 * Obtiene candles históricas OHLCV para un símbolo de mercado vía MetaApi.
 * @param {string} symbol - Instrumento (default: 'XAUUSD')
 * @param {string} timeframe - Temporalidad: '1h','4h','1d','1w' (default: '1h')
 * @param {number} limit - Número de velas (default: 100)
 * @returns {{ candles: Array, symbol: string, timeframe: string }}
 */
export const getMarketCandles = async (
  symbol = "XAUUSD",
  timeframe = "1h",
  limit = 100,
) => {
  const token = localStorage.getItem("token");
  const params = new URLSearchParams({
    symbol,
    timeframe,
    limit: String(limit),
  });
  const response = await fetch(`${BACKEND_URL}/api/market/candles?${params}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!response.ok) return { candles: [], symbol, timeframe };
  return response.json();
};
