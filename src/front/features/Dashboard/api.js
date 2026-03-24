const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

// ── Simple in-memory cache (stale-while-revalidate) ─────────────────────────
const _cache = {};

const cached = (key, ttlMs, fetcher) => {
  const hit = _cache[key];
  const fresh = hit && Date.now() - hit.ts < ttlMs;
  if (fresh) return Promise.resolve(hit.data);
  const promise = fetcher().then((data) => {
    _cache[key] = { data, ts: Date.now() };
    return data;
  });
  if (hit) {
    // stale: return old data immediately, refresh in background
    promise.catch(() => {});
    return Promise.resolve(hit.data);
  }
  return promise;
};

export const invalidateCache = (key) => { delete _cache[key]; };
// ─────────────────────────────────────────────────────────────────────────────

const parseError = async (response) => {
  try {
    const json = await response.json();
    return json.description || json.msg || json.message || "Error inesperado";
  } catch {
    return "Error inesperado";
  }
};

/** Si el token expiró o es inválido (401), limpia sesión y redirige al login */
const checkAuth = (response) => {
  if (response.status === 401) {
    localStorage.removeItem("token");
    window.location.href = "/login";
  }
  return response;
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

export const startBot = async (walletId = null) => {
  const token = localStorage.getItem("token");
  const body  = walletId ? JSON.stringify({ wallet_id: walletId }) : null;
  const response = await fetch(`${BACKEND_URL}/api/bot/start`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, ...(body ? { "Content-Type": "application/json" } : {}) },
    ...(body ? { body } : {}),
  });
  if (!response.ok) {
    const msg = await parseError(response);
    throw new Error(msg);
  }
  return response.json();
};

export const stopBot = async (walletId = null) => {
  const token = localStorage.getItem("token");
  const body  = walletId ? JSON.stringify({ wallet_id: walletId }) : null;
  const response = await fetch(`${BACKEND_URL}/api/bot/stop`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, ...(body ? { "Content-Type": "application/json" } : {}) },
    ...(body ? { body } : {}),
  });
  if (!response.ok) {
    const msg = await parseError(response);
    throw new Error(msg);
  }
  return response.json();
};

export const getWallets = () =>
  cached("wallets", 60_000, async () => {
    const token = localStorage.getItem("token");
    const response = await fetch(`${BACKEND_URL}/api/wallets`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) { const msg = await parseError(response); throw new Error(msg); }
    return response.json();
  });

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

export const updateBotStrategy = async (strategyId, walletId = null) => {
  const token = localStorage.getItem("token");
  const body = { strategy: strategyId };
  if (walletId) body.wallet_id = walletId;
  const response = await fetch(`${BACKEND_URL}/api/bot/strategy`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    const msg = await parseError(response);
    throw new Error(msg);
  }
  return response.json();
};

export const setWalletPropFirm = async (walletId, phase) => {
  const token = localStorage.getItem("token");
  const response = await fetch(`${BACKEND_URL}/api/wallets/${walletId}/set-prop-firm`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ phase }),
  });
  if (!response.ok) {
    const msg = await parseError(response);
    throw new Error(msg);
  }
  return response.json();
};

export const getProfile = async () => {
  const token = localStorage.getItem("token");
  const response = await fetch(`${BACKEND_URL}/api/users/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (response.status === 401) {
    localStorage.removeItem("token");
    window.location.href = "/login";
  }
  if (!response.ok) {
    const msg = await parseError(response);
    throw new Error(msg);
  }
  return response.json();
};

export const updateProfile = async (data) => {
  const token = localStorage.getItem("token");
  const response = await fetch(`${BACKEND_URL}/api/users/me`, {
    method: "PATCH",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  if (response.status === 401) {
    localStorage.removeItem("token");
    window.location.href = "/login";
  }
  if (!response.ok) {
    const msg = await parseError(response);
    throw new Error(msg);
  }
  return response.json();
};

export const getOpenTrades = () =>
  cached("open_trades", 20_000, async () => {
    const token = localStorage.getItem("token");
    const response = checkAuth(await fetch(`${BACKEND_URL}/api/dashboard/trades/open`, {
      headers: { Authorization: `Bearer ${token}` },
    }));
    if (!response.ok) { const msg = await parseError(response); throw new Error(msg); }
    return response.json();
  });

export const syncTrades = async () => {
  const token = localStorage.getItem("token");
  const response = checkAuth(await fetch(`${BACKEND_URL}/api/dashboard/sync`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  }));
  if (!response.ok) {
    const msg = await parseError(response);
    throw new Error(msg);
  }
  return response.json();
};

export const getBotSignal = async () => {
  const token = localStorage.getItem("token");
  const response = checkAuth(await fetch(`${BACKEND_URL}/api/bot/signal`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  }));
  if (!response.ok) {
    const msg = await parseError(response);
    throw new Error(msg);
  }
  return response.json();
};

export const getDashboardSummary = () =>
  cached("dashboard_summary", 30_000, async () => {
    const token = localStorage.getItem("token");
    const response = checkAuth(await fetch(`${BACKEND_URL}/api/dashboard/summary`, {
      headers: { Authorization: `Bearer ${token}` },
    }));
    if (!response.ok) { const msg = await parseError(response); throw new Error(msg); }
    return response.json();
  });

export const getTradeHistory = () =>
  cached("trade_history", 60_000, async () => {
    const token = localStorage.getItem("token");
    const response = checkAuth(await fetch(`${BACKEND_URL}/api/dashboard/trades/history`, {
      headers: { Authorization: `Bearer ${token}` },
    }));
    if (!response.ok) { const msg = await parseError(response); throw new Error(msg); }
    return response.json();
  });

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
