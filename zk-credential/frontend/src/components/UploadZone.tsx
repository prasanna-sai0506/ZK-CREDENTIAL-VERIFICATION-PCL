import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";
import { useJobStore } from "../store/jobStore";
import { useWalletStore } from "../store/walletStore";

const API = import.meta.env.VITE_API_URL || "";
const ACCEPTED = { "application/pdf": [".pdf"], "image/*": [".png", ".jpg", ".jpeg"] };

async function encryptFile(file: File, rawKey: Uint8Array): Promise<{ bytes: Uint8Array; iv: Uint8Array }> {
  // AES-256-GCM client-side encryption
  const keyBytes = rawKey.buffer.slice(0) as ArrayBuffer;
  const key = await crypto.subtle.importKey("raw", keyBytes, "AES-GCM", false, ["encrypt"]);
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const plaintext = await file.arrayBuffer();
  const ciphertext = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, plaintext);
  return { bytes: new Uint8Array(ciphertext), iv };
}

function toHex(bytes: Uint8Array): string {
  return Array.from(bytes, (byte) => byte.toString(16).padStart(2, "0")).join("");
}

export default function UploadZone({ onJobCreated }: { onJobCreated: (jobId: string) => void }) {
  const addJob = useJobStore((s) => s.addJob);
  const token = useWalletStore((s) => s.token);
  const [uploading, setUploading] = useState(false);
  const [statusMsg, setStatusMsg] = useState<string | null>(null);
  const [errMsg, setErrMsg] = useState<string | null>(null);

  const onDrop = useCallback(
    async (accepted: File[]) => {
      if (!accepted.length) return;
      if (!token) {
        setErrMsg("Please connect your wallet first.");
        return;
      }
      const file = accepted[0];
      setUploading(true);
      setErrMsg(null);
      setStatusMsg("Encrypting document…");

      try {
        const rawKey = crypto.getRandomValues(new Uint8Array(32));
        const { bytes, iv } = await encryptFile(file, rawKey);
        setStatusMsg("Uploading encrypted document…");

        const view = bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength) as ArrayBuffer;
        const blob = new Blob([view], { type: "application/octet-stream" });
        const formData = new FormData();
        formData.append("file", blob, file.name);
        formData.append("encryption_key", toHex(rawKey));
        formData.append("encryption_iv", toHex(iv));

        const res = await axios.post(`${API}/api/v1/documents/upload`, formData, {
          headers: { Authorization: `Bearer ${token}`, "Content-Type": "multipart/form-data" },
        });

        const { doc_id, job_id } = res.data;
        addJob({
          jobId: job_id,
          docId: doc_id,
          status: "queued",
          filename: file.name,
          uploadedAt: new Date(),
        });
        onJobCreated(job_id);
        setStatusMsg("Uploaded! Generating ZK proof in background…");
      } catch (e: unknown) {
        setErrMsg(e instanceof Error ? e.message : "Upload failed");
        setStatusMsg(null);
      } finally {
        setUploading(false);
      }
    },
    [token, addJob, onJobCreated]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ACCEPTED,
    maxFiles: 1,
    disabled: uploading,
  });

  return (
    <div>
      <div
        {...getRootProps()}
        className={`group cursor-pointer rounded-3xl border-2 border-dashed p-6 text-center transition duration-200 sm:p-10
          ${isDragActive ? "border-cyan-400 bg-cyan-400/10 shadow-[0_0_0_1px_rgba(34,211,238,0.15)]" : "border-white/10 bg-white/5 hover:border-cyan-400/30 hover:bg-cyan-400/5"}`}
      >
        <input {...getInputProps()} />
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-slate-950/70 text-3xl shadow-lg shadow-slate-950/20">
          📄
        </div>
        {isDragActive ? (
          <p className="mt-4 text-base font-semibold text-cyan-200">Drop your document here…</p>
        ) : (
          <div className="mt-4 space-y-2">
            <p className="text-base font-semibold text-white">Drag & drop a document</p>
            <p className="text-sm text-slate-400">or click to browse</p>
            <p className="text-xs uppercase tracking-[0.22em] text-slate-500">PDF, PNG, JPG - up to 20 MB</p>
          </div>
        )}
      </div>
      {uploading && (
        <div className="mt-3 flex items-center gap-2 rounded-2xl border border-cyan-400/15 bg-cyan-400/10 px-4 py-3 text-sm text-cyan-100">
          <span className="animate-spin">⟳</span> {statusMsg}
        </div>
      )}
      {!uploading && statusMsg && (
        <p className="mt-3 rounded-2xl border border-emerald-400/15 bg-emerald-400/10 px-4 py-3 text-sm text-emerald-100">✓ {statusMsg}</p>
      )}
      {errMsg && <p className="mt-3 rounded-2xl border border-rose-400/15 bg-rose-400/10 px-4 py-3 text-sm text-rose-100">✗ {errMsg}</p>}
    </div>
  );
}
