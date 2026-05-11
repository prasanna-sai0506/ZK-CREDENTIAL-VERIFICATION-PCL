import { create } from "zustand";

export interface JobEntry {
  jobId: string; docId: string; filename: string;
  uploadedAt: Date;
  status: "queued" | "processing" | "done" | "failed";
  claimSet?: Record<string, unknown>;
  proofTxHash?: string; errorMessage?: string;
}

interface JobStore {
  jobs: JobEntry[];
  addJob: (job: JobEntry) => void;
  updateJob: (jobId: string, patch: Partial<JobEntry>) => void;
}

export const useJobStore = create<JobStore>((set) => ({
  jobs: [],
  addJob: (job) => set((s) => ({ jobs: [job, ...s.jobs] })),
  updateJob: (jobId, patch) =>
    set((s) => ({ jobs: s.jobs.map((j) => (j.jobId === jobId ? { ...j, ...patch } : j)) })),
}));
