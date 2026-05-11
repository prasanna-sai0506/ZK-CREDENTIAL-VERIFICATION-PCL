import { create } from "zustand";

declare global { interface Window { ethereum?: any } }

const API = (typeof import.meta !== "undefined" && (import.meta as any).env?.VITE_API_URL) || "";

interface WalletState {
  address: string | null;
  token: string | null;
  error: string | null;
  connect: () => Promise<void>;
  disconnect: () => void;
}

export const useWalletStore = create<WalletState>((set) => ({
  address: null,
  token: null,
  error: null,
  connect: async () => {
    if (!window.ethereum) {
      set({ error: "MetaMask is not installed in this browser." });
      return;
    }

    set({ error: null });

    let accounts: string[] = [];
    try {
      accounts = await window.ethereum.request({ method: "eth_requestAccounts" });
    } catch {
      set({ error: "Wallet connection was cancelled." });
      return;
    }

    const address = accounts?.[0];
    if (!address) {
      set({ error: "No wallet account was returned by the provider." });
      return;
    }

    // Mark wallet as connected first, then try backend auth token.
    set({ address, token: null, error: null });

    try {
      const resp = await fetch(`${API}/api/v1/auth/token?user_address=${address}`, {
        method: "POST",
        headers: { Accept: "application/json" },
      });

      if (!resp.ok) {
        throw new Error(`Auth API returned ${resp.status}`);
      }

      const raw = await resp.text();
      if (!raw) {
        throw new Error("Empty auth response");
      }

      const parsed = JSON.parse(raw) as { access_token?: string };
      if (!parsed.access_token) {
        throw new Error("Missing access_token");
      }

      set({ token: parsed.access_token, error: null });
    } catch {
      set({
        token: null,
        error: "Wallet connected, but backend auth is unavailable. Start backend services to enable uploads.",
      });
    }
  },
  disconnect: () => set({ address: null, token: null, error: null }),
}));
