import React from "react";
import { JobEntry } from "../store/jobStore";

const STATUS_CONFIG = {
  queued:     { icon: "⏳", color: "text-gray-400",  label: "Queued" },
  processing: { icon: "⚙️", color: "text-sky-400",   label: "Processing" },
  done:       { icon: "✅", color: "text-green-400", label: "Proof Generated" },
  failed:     { icon: "❌", color: "text-red-400",   label: "Failed" },
};

const CLAIM_LABELS: Record<string, string> = {
  over_18: "Age ≥ 18",
  nationality: "Nationality",
  has_degree: "Degree",
  degree_institution: "Institution",
  employment_verified: "Employed",
};

function ClaimBadge({ label, value }: { label: string; value: unknown }) {
  const display = typeof value === "boolean" ? (value ? "✓" : "✗") : String(value);
  const positive = value === true || (typeof value === "string" && value.length > 0);
  return (
    <span
      className={`inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full border
        ${positive ? "bg-green-900/30 border-green-700 text-green-300" : "bg-gray-900/30 border-gray-700 text-gray-500"}`}
    >
      {label}: <strong>{display}</strong>
    </span>
  );
}

export default function ProofCard({ job }: { job: JobEntry }) {
  const cfg = STATUS_CONFIG[job.status];
  const parserFields = (job.claimSet as Record<string, unknown> | undefined)?.custom_claims as
    | { extracted_fields?: Record<string, unknown> }
    | undefined;
  const ageUnknown =
    parserFields?.extracted_fields &&
    (parserFields.extracted_fields.dob == null || parserFields.extracted_fields.dob === "") &&
    (parserFields.extracted_fields.year_of_birth == null || parserFields.extracted_fields.year_of_birth === "");

  return (
    <div className="soft-card p-5 sm:p-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="space-y-1">
          <p className="text-base font-semibold text-white">{job.filename}</p>
          <p className="text-xs text-slate-400">{job.uploadedAt.toLocaleString()}</p>
        </div>
        <span className={`inline-flex items-center gap-2 self-start rounded-full border border-white/10 px-3 py-1 text-xs font-semibold ${cfg.color}`}>
          {cfg.icon} {cfg.label}
        </span>
      </div>

      {job.status === "processing" && (
        <div className="h-2 overflow-hidden rounded-full bg-white/5">
          <div className="h-full w-1/2 rounded-full bg-gradient-to-r from-cyan-400 to-emerald-400 animate-pulse" />
        </div>
      )}

      {job.claimSet && (
        <div className="flex flex-wrap gap-2">
          {ageUnknown && <ClaimBadge label="Age ≥ 18" value="Unknown" />}
          {Object.entries(job.claimSet)
            .filter(
              ([k]) =>
                k !== "custom_claims" &&
                k !== "age" &&
                k !== "age_years" &&
                !(k === "over_18" && ageUnknown),
            )
            .map(([k, v]) => (
              <ClaimBadge key={k} label={CLAIM_LABELS[k] ?? k} value={v} />
            ))}
        </div>
      )}

      {job.proofTxHash && (
        <div className="rounded-2xl border border-white/8 bg-slate-950/60 px-3 py-2 text-xs font-mono text-slate-400 truncate">
          Tx: <span className="text-cyan-300">{job.proofTxHash}</span>
        </div>
      )}

      {job.errorMessage && (
        <p className="rounded-2xl border border-rose-400/15 bg-rose-400/10 px-3 py-2 text-xs text-rose-100">{job.errorMessage}</p>
      )}
    </div>
  );
}
