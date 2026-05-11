import React from "react";
import { useWalletStore } from "../store/walletStore";

export default function WalletButton() {
  const address = useWalletStore((s) => s.address);
  const connectWallet = useWalletStore((s) => s.connect);
  const storeError = useWalletStore((s) => s.error);
  const [connecting, setConnecting] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const connect = async () => {
    setConnecting(true);
    setError(null);
    try {
      await connectWallet();
    } catch (e) {
      const message = e instanceof Error ? e.message : "Failed to connect wallet";
      setError(message);
    } finally {
      setConnecting(false);
    }
  };

  if (address) {
    return (
      <div className="inline-flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-2 text-sm text-emerald-100">
        <span className="h-2.5 w-2.5 rounded-full bg-emerald-400 shadow-[0_0_0_6px_rgba(16,185,129,0.12)] animate-pulse" />
        <span className="max-w-[10rem] truncate font-mono text-xs sm:max-w-none">
          {address.slice(0, 6)}...{address.slice(-4)}
        </span>
      </div>
    );
  }

  return (
    <div>
      <button
        onClick={connect}
        disabled={connecting}
        className="w-full rounded-full bg-gradient-to-r from-cyan-400 to-emerald-400 px-4 py-2.5 text-sm font-semibold text-slate-950 shadow-lg shadow-cyan-500/20 transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto"
      >
        {connecting ? "Connecting…" : "Connect Wallet"}
      </button>
      {(error || storeError) && (
        <p className="mt-2 text-xs leading-5 text-rose-200">
          {error || storeError}
        </p>
      )}
    </div>
  );
}
