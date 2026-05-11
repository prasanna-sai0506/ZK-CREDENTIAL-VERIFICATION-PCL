import React, { useState } from "react";
import axios from "axios";

const API = import.meta.env.VITE_API_URL || "";

const BITMAP_OPTIONS = [
  { label: "Age ≥ 18", bit: 1 },
  { label: "Nationality verified", bit: 2 },
  { label: "Degree verified", bit: 4 },
  { label: "Employment verified", bit: 8 },
];

export default function VerifyPage() {
  const [address, setAddress] = useState("");
  const [selectedBits, setSelectedBits] = useState<number[]>([]);
  const [result, setResult] = useState<boolean | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const bitmap = selectedBits.reduce((acc, b) => acc | b, 0);

  const toggle = (bit: number) => {
    setSelectedBits((prev) =>
      prev.includes(bit) ? prev.filter((b) => b !== bit) : [...prev, bit]
    );
  };

  const verify = async () => {
    if (!address || bitmap === 0) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await axios.post(`${API}/api/v1/verify`, {
        user_address: address,
        claim_bitmap: `0x${bitmap.toString(16)}`,
      });
      setResult(res.data.verified);
    } catch (e) {
      setError("Verification request failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="space-y-8">
      <section className="soft-card hero-gradient p-6 sm:p-8">
        <p className="section-title">Verification</p>
        <div className="mt-3 max-w-3xl space-y-3">
          <h1 className="font-display text-4xl font-bold tracking-tight text-white sm:text-5xl">
            Verify claims without exposing documents.
          </h1>
          <p className="max-w-2xl text-base leading-7 text-slate-300 sm:text-lg">
            Enter a wallet address and choose the claims you need. The interface makes the bitmap
            and verification result easy to read on desktop and mobile.
          </p>
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-[minmax(0,1.05fr)_minmax(300px,0.95fr)]">
        <div className="soft-card p-5 sm:p-6">
          <div className="mb-5 flex items-center justify-between gap-3">
            <div>
              <p className="section-title">Query</p>
              <h2 className="mt-2 text-2xl font-bold text-white">Claim request</h2>
            </div>
            <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs font-semibold text-slate-300">
              On-chain bitmap
            </span>
          </div>

          <div className="space-y-5">
            <div>
              <label className="mb-2 block text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
                Wallet Address
              </label>
              <input
                type="text"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                placeholder="0x..."
                className="w-full rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-sm text-slate-100 font-mono outline-none transition placeholder:text-slate-600 focus:border-cyan-400/60 focus:ring-2 focus:ring-cyan-400/20"
              />
            </div>

            <div>
              <label className="mb-2 block text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
                Required Claims
              </label>
              <div className="grid gap-3 md:grid-cols-2">
                {BITMAP_OPTIONS.map(({ label, bit }) => (
                  <label
                    key={bit}
                    className="flex cursor-pointer items-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 transition hover:border-cyan-400/30 hover:bg-cyan-400/5"
                  >
                    <input
                      type="checkbox"
                      checked={selectedBits.includes(bit)}
                      onChange={() => toggle(bit)}
                      className="h-4 w-4 rounded border-white/20 accent-cyan-400"
                    />
                    <span className="text-sm font-medium text-slate-200">{label}</span>
                  </label>
                ))}
              </div>
              {bitmap > 0 && (
                <div className="mt-3 rounded-2xl border border-cyan-400/15 bg-cyan-400/10 px-4 py-3 text-sm text-cyan-100">
                  Bitmap: <span className="font-mono text-cyan-200">0x{bitmap.toString(16)}</span>
                </div>
              )}
            </div>

            <button
              onClick={verify}
              disabled={loading || !address || bitmap === 0}
              className="w-full rounded-2xl bg-gradient-to-r from-cyan-400 to-emerald-400 px-4 py-3 font-semibold text-slate-950 shadow-lg shadow-cyan-500/20 transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {loading ? "Checking…" : "Verify On-Chain"}
            </button>
          </div>
        </div>

        <div className="space-y-6">
          <div className="soft-card p-5 sm:p-6">
            <p className="section-title">Preview</p>
            <h2 className="mt-2 text-2xl font-bold text-white">What this request means</h2>
            <div className="mt-4 space-y-3 text-sm leading-6 text-slate-300">
              <p>• The address is matched against an on-chain proof registry.</p>
              <p>• The selected bitmap defines the exact claim combination.</p>
              <p>• No raw document leaves the private pipeline.</p>
            </div>
          </div>

          {result !== null && (
            <div
              className={`soft-card p-5 sm:p-6 text-center ${
                result ? "border-emerald-400/20" : "border-rose-400/20"
              }`}
            >
              <div
                className={`mx-auto flex h-16 w-16 items-center justify-center rounded-2xl text-3xl ${
                  result ? "bg-emerald-400/10" : "bg-rose-400/10"
                }`}
              >
                {result ? "✅" : "❌"}
              </div>
              <p className="mt-4 text-xl font-bold text-white">
                {result ? "Claims Verified" : "Claims Not Found"}
              </p>
              <p className="mt-2 text-sm leading-6 text-slate-300">
                {result
                  ? "This address has a valid on-chain proof for the requested claims."
                  : "No matching proof was found for the selected claims."}
              </p>
            </div>
          )}

          {error && (
            <div className="soft-card border-rose-400/20 bg-rose-400/10 p-4 text-sm text-rose-100">
              {error}
            </div>
          )}
        </div>
      </section>
    </main>
  );
}
