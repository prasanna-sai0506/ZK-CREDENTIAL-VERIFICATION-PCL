import React, { useState } from "react";
import WalletButton from "../components/WalletButton";
import UploadZone from "../components/UploadZone";
import ProofCard from "../components/ProofCard";
import { useJobStore } from "../store/jobStore";
import { useProofStatus } from "../hooks/useProofStatus";

function ActiveJobPoller({ jobId }: { jobId: string }) {
  useProofStatus(jobId);
  const job = useJobStore((s) => s.jobs.find((j) => j.jobId === jobId));
  if (!job) return null;
  return <ProofCard job={job} />;
}

export default function UploadPage() {
  const [activeJobId, setActiveJobId] = useState<string | null>(null);

  return (
    <main className="space-y-8">
      <section className="grid gap-6 xl:grid-cols-[minmax(0,1.25fr)_minmax(280px,0.75fr)] xl:items-stretch">
        <div className="soft-card hero-gradient overflow-hidden p-6 sm:p-8 lg:p-10">
          <div className="inline-flex items-center gap-2 rounded-full border border-cyan-400/20 bg-cyan-400/10 px-3 py-1 text-[0.72rem] font-semibold uppercase tracking-[0.25em] text-cyan-200">
            <span className="h-2 w-2 rounded-full bg-cyan-300" />
            Zero-knowledge identity flow
          </div>

          <div className="mt-6 max-w-2xl space-y-4">
            <h1 className="font-display text-4xl font-bold tracking-tight text-white sm:text-5xl lg:text-6xl">
              Privacy-preserving identity verification with a premium interface.
            </h1>
            <p className="max-w-xl text-base leading-7 text-slate-300 sm:text-lg">
              Upload a document, extract claims, and mint a proof without revealing the source file.
              The redesigned layout focuses on clarity, trust, and fast scanning on every screen size.
            </p>
          </div>

          <div className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {[
              { icon: "🔒", label: "Encrypted upload", value: "Client-side" },
              { icon: "🧠", label: "LLM claim extraction", value: "Structured" },
              { icon: "⛓️", label: "ZK proof on-chain", value: "Verifiable" },
            ].map(({ icon, label, value }) => (
              <div key={label} className="rounded-2xl border border-white/10 bg-slate-950/40 p-4 backdrop-blur-sm">
                <div className="text-2xl">{icon}</div>
                <p className="mt-3 text-sm font-semibold text-white">{label}</p>
                <p className="mt-1 text-xs uppercase tracking-[0.24em] text-slate-400">{value}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="soft-card flex flex-col justify-between gap-6 p-6 sm:p-8">
          <div>
            <p className="section-title">Wallet</p>
            <h2 className="mt-2 text-2xl font-bold text-white">Authenticate before uploading.</h2>
            <p className="mt-3 text-sm leading-6 text-slate-300">
              Connect your wallet to encrypt and submit the document. The interface keeps the action
              obvious and the state readable.
            </p>
          </div>
          <div className="rounded-3xl border border-white/10 bg-slate-950/50 p-4">
            <WalletButton />
          </div>
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-[minmax(0,1.1fr)_minmax(320px,0.9fr)]">
        <div className="soft-card p-5 sm:p-6">
          <div className="mb-5 flex items-center justify-between gap-3">
            <div>
              <p className="section-title">Upload</p>
              <h2 className="mt-2 text-2xl font-bold text-white">Document intake</h2>
            </div>
            <span className="rounded-full border border-cyan-400/20 bg-cyan-400/10 px-3 py-1 text-xs font-semibold text-cyan-200">
              Secure
            </span>
          </div>
          <UploadZone onJobCreated={setActiveJobId} />
        </div>

        <div className="soft-card p-5 sm:p-6">
          <p className="section-title">Flow</p>
          <h2 className="mt-2 text-2xl font-bold text-white">What happens next</h2>
          <div className="mt-5 space-y-3">
            {[
              "The file is encrypted in your browser before upload.",
              "Backend workers extract claims and generate the witness.",
              "A proof is assembled and becomes visible in the dashboard.",
            ].map((item, index) => (
              <div key={item} className="flex gap-3 rounded-2xl border border-white/8 bg-white/5 p-4">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-cyan-400/15 text-sm font-bold text-cyan-200">
                  {index + 1}
                </div>
                <p className="text-sm leading-6 text-slate-300">{item}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {activeJobId && (
        <section className="soft-card p-5 sm:p-6">
          <div className="mb-4 flex items-center justify-between gap-3">
            <div>
              <p className="section-title">Proof status</p>
              <h2 className="mt-2 text-2xl font-bold text-white">Live processing update</h2>
            </div>
            <span className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs font-semibold text-emerald-200">
              Tracking
            </span>
          </div>
          <ActiveJobPoller jobId={activeJobId} />
        </section>
      )}
    </main>
  );
}
