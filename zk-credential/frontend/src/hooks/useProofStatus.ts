import { useEffect, useRef } from "react";
import { useJobStore } from "../store/jobStore";
import { useWalletStore } from "../store/walletStore";

const API = (typeof import.meta !== "undefined" && (import.meta as any).env?.VITE_API_URL) || "";
const POLL_INTERVAL = 3000;

export function useProofStatus(jobId: string | null) {
  const { token } = useWalletStore();
  const { updateJob } = useJobStore();
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (!jobId || !token) return;
    const poll = async () => {
      try {
        const r = await fetch(`${API}/api/v1/jobs/${jobId}/status`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!r.ok) return;
        const data = await r.json();
        updateJob(jobId, {
          status: data.status,
          claimSet: data.claim_set,
          proofTxHash: data.proof_tx_hash,
          errorMessage: data.error_message,
        });
        if (data.status === "done" || data.status === "failed") {
          if (timerRef.current) clearInterval(timerRef.current);
        }
      } catch (_) {}
    };
    poll();
    timerRef.current = setInterval(poll, POLL_INTERVAL);
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, [jobId, token]);
}
