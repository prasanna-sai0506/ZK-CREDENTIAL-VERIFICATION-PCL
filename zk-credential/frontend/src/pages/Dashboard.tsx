import React from "react";
import ProofCard from "../components/ProofCard";
import { useJobStore } from "../store/jobStore";
import { useProofStatus } from "../hooks/useProofStatus";

function JobPoller({ jobId }: { jobId: string }) {
  useProofStatus(jobId);
  return null;
}

export default function DashboardPage() {
  const jobs = useJobStore((s) => s.jobs);

  const activeJobs = jobs.filter((j) => j.status === "queued" || j.status === "processing");
  const completedJobs = jobs.filter((j) => j.status === "done");

  return (
    <main className="space-y-8">
      <section className="soft-card hero-gradient p-6 sm:p-8">
        <p className="section-title">Dashboard</p>
        <div className="mt-3 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-2xl space-y-3">
            <h1 className="font-display text-4xl font-bold tracking-tight text-white sm:text-5xl">
              Track proofs at a glance.
            </h1>
            <p className="max-w-2xl text-base leading-7 text-slate-300 sm:text-lg">
              See recently processed documents, monitor active jobs, and review proof metadata in a
              cleaner, more readable layout.
            </p>
          </div>

          <div className="grid grid-cols-1 gap-3 sm:min-w-[20rem] sm:grid-cols-3">
            <StatChip label="Total" value={jobs.length} />
            <StatChip label="Active" value={activeJobs.length} />
            <StatChip label="Done" value={completedJobs.length} />
          </div>
        </div>
      </section>

      {activeJobs.map((j) => (
        <JobPoller key={j.jobId} jobId={j.jobId} />
      ))}

      {jobs.length === 0 ? (
        <div className="soft-card py-16 text-center text-slate-400">
          <div className="mb-3 text-5xl">📭</div>
          <p className="text-base">No credentials yet. Upload a document to get started.</p>
        </div>
      ) : (
        <div className="grid gap-4 lg:grid-cols-2">
          {jobs.map((job) => (
            <ProofCard key={job.jobId} job={job} />
          ))}
        </div>
      )}
    </main>
  );
}

function StatChip({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 px-3 py-3 text-center backdrop-blur-sm">
      <p className="text-[0.68rem] uppercase tracking-[0.24em] text-slate-400">{label}</p>
      <p className="mt-1 text-2xl font-bold text-white">{value}</p>
    </div>
  );
}
