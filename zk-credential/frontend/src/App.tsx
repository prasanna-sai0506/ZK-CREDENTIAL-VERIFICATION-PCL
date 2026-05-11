import { useState } from "react";
import Upload from "./pages/Upload";
import Dashboard from "./pages/Dashboard";
import Verify from "./pages/Verify";
import { useWalletStore } from "./store/walletStore";

type Page = "upload" | "dashboard" | "verify";

export default function App() {
  const [page, setPage] = useState<Page>("upload");
  return (
    <div className="relative min-h-screen overflow-hidden text-slate-100">
      <div className="pointer-events-none absolute inset-0 opacity-60">
        <div className="absolute -left-24 top-8 h-64 w-64 rounded-full bg-cyan-500/20 blur-3xl" />
        <div className="absolute right-0 top-40 h-72 w-72 rounded-full bg-emerald-400/10 blur-3xl" />
        <div className="absolute bottom-0 left-1/3 h-80 w-80 rounded-full bg-sky-500/10 blur-3xl" />
      </div>

      <div className="relative mx-auto flex min-h-screen w-full max-w-7xl flex-col px-4 pb-24 pt-4 sm:px-6 lg:px-8 lg:pb-10">
        <Nav page={page} setPage={setPage} />

        <main className="mt-6 grid flex-1 gap-6 lg:grid-cols-[minmax(0,1.55fr)_minmax(320px,0.9fr)]">
          <section className="soft-card overflow-hidden p-4 sm:p-6 lg:p-8">
            {page === "upload" && <Upload />}
            {page === "dashboard" && <Dashboard />}
            {page === "verify" && <Verify />}
          </section>

          <aside className="hidden lg:flex lg:flex-col lg:gap-6">
            <div className="soft-card p-6">
              <p className="section-title">Why it stands out</p>
              <h2 className="mt-3 text-2xl font-bold text-white">Private, polished, and easy to scan.</h2>
              <p className="mt-3 text-sm leading-6 text-slate-300">
                The interface now uses layered glass panels, clear hierarchy, and responsive spacing
                so the app feels like a product instead of a prototype.
              </p>
            </div>

            <div className="soft-card p-6">
              <p className="section-title">Workflow</p>
              <div className="mt-4 space-y-3 text-sm text-slate-300">
                <InfoRow title="1. Upload" text="Encrypt a document and send it securely." />
                <InfoRow title="2. Prove" text="Claims move through the backend proof pipeline." />
                <InfoRow title="3. Verify" text="Check on-chain claims without exposing the source file." />
              </div>
            </div>
          </aside>
        </main>
      </div>

      <MobileNav page={page} setPage={setPage} />
    </div>
  );
}

function Nav({ page, setPage }: { page: Page; setPage: (p: Page) => void }) {
  const { address, connect, disconnect, error } = useWalletStore();
  const btn = (p: Page, label: string) => (
    <button
      onClick={() => setPage(p)}
      className={`nav-pill ${page === p ? "nav-pill-active" : "hover:border-white/20 hover:bg-white/10 hover:text-white"}`}
    >
      {label}
    </button>
  );
  return (
    <nav className="glass-panel flex flex-col gap-4 rounded-3xl px-4 py-4 shadow-2xl shadow-slate-950/30 sm:px-6 lg:flex-row lg:items-center lg:justify-between">
      <div className="flex items-center gap-3 sm:gap-4">
        <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-400 to-emerald-400 text-lg font-black text-slate-950 shadow-lg shadow-cyan-500/25">
          ZK
        </div>
        <div>
          <p className="text-[0.7rem] font-semibold uppercase tracking-[0.28em] text-slate-400">
            ZK Credential
          </p>
          <h1 className="font-display text-base font-bold text-white sm:text-xl">
            Privacy-preserving identity workflow
          </h1>
        </div>
      </div>

      <div className="flex flex-wrap gap-2 sm:justify-center">
        {btn("upload", "Upload")}
        {btn("dashboard", "Dashboard")}
        {btn("verify", "Verify")}
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between lg:justify-end">
        <div className="hidden text-right sm:block">
          <p className="text-[0.7rem] uppercase tracking-[0.24em] text-slate-500">Wallet</p>
          <p className="text-xs text-slate-400">
            {address ? "Connected" : "Not connected"}
          </p>
        </div>
        <div className="flex flex-col items-stretch gap-2 sm:items-end">
          {address ? (
            <div className="flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-2">
              <span className="h-2.5 w-2.5 rounded-full bg-emerald-400 shadow-[0_0_0_6px_rgba(16,185,129,0.12)]" />
              <span className="max-w-[10rem] truncate font-mono text-xs text-emerald-200 sm:max-w-none">
                {address.slice(0, 6)}...{address.slice(-4)}
              </span>
              <button
                onClick={disconnect}
                className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs font-medium text-slate-200 transition hover:bg-white/10"
              >
                Disconnect
              </button>
            </div>
          ) : (
            <button
              onClick={connect}
              className="rounded-full bg-gradient-to-r from-cyan-400 to-emerald-400 px-4 py-2 text-sm font-semibold text-slate-950 shadow-lg shadow-cyan-500/25 transition hover:brightness-110"
            >
              Connect Wallet
            </button>
          )}

          {error && (
            <p className="max-w-[18rem] text-right text-xs leading-5 text-rose-200">
              {error}
            </p>
          )}
        </div>
      </div>
    </nav>
  );
}

function MobileNav({ page, setPage }: { page: Page; setPage: (p: Page) => void }) {
  const mobileBtn = (p: Page, label: string, icon: string) => (
    <button
      onClick={() => setPage(p)}
      className={`flex flex-1 flex-col items-center justify-center gap-1 rounded-2xl px-3 py-3 text-xs font-semibold transition ${
        page === p
          ? "bg-cyan-400 text-slate-950 shadow-lg shadow-cyan-500/20"
          : "text-slate-300 hover:bg-white/8"
      }`}
    >
      <span className="text-base">{icon}</span>
      {label}
    </button>
  );

  return (
    <nav className="fixed inset-x-4 bottom-4 z-50 rounded-3xl border border-white/10 bg-slate-950/80 p-2 shadow-[0_20px_60px_rgba(2,6,23,0.45)] backdrop-blur-xl lg:hidden">
      <div className="flex gap-2">
        {mobileBtn("upload", "Upload", "⬆️")}
        {mobileBtn("dashboard", "Dashboard", "📊")}
        {mobileBtn("verify", "Verify", "🛡️")}
      </div>
    </nav>
  );
}

function InfoRow({ title, text }: { title: string; text: string }) {
  return (
    <div className="rounded-2xl border border-white/8 bg-white/5 p-4">
      <p className="text-sm font-semibold text-white">{title}</p>
      <p className="mt-1 text-sm leading-6 text-slate-300">{text}</p>
    </div>
  );
}
