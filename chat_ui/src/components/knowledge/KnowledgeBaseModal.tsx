import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Upload, FileText, CheckCircle2, Clock, AlertCircle } from "lucide-react";

interface DocumentItem {
  id: number;
  original_filename: string;
  file_size: number;
  status: string;
  created_at: string;
}

interface KnowledgeBaseModalProps {
  open: boolean;
  onClose: () => void;
  knowledgeBaseId?: number;
}

export function KnowledgeBaseModal({ open, onClose, knowledgeBaseId = 1 }: KnowledgeBaseModalProps) {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const baseUrl = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

  const fetchDocuments = async () => {
    try {
      const token = localStorage.getItem("access_token") || "";
      const res = await fetch(`${baseUrl}/api/knowledge-bases/${knowledgeBaseId}/documents`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (res.ok) {
        const data = await res.json();
        setDocuments(data.items || []);
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    if (open) {
      fetchDocuments();
    }
  }, [open, knowledgeBaseId]);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    const file = files[0];
    if (!file.name.endsWith(".pdf")) {
      setError("Only PDF files are supported");
      return;
    }

    setUploading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const token = localStorage.getItem("access_token") || "";
      const res = await fetch(`${baseUrl}/api/knowledge-bases/${knowledgeBaseId}/documents`, {
        method: "POST",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        body: formData,
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || "Upload failed");
      }

      await fetchDocuments();
    } catch (err: any) {
      setError(err.message || "Failed to upload document");
    } finally {
      setUploading(false);
    }
  };

  return (
    <AnimatePresence>
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.95, opacity: 0 }}
            className="w-full max-w-2xl rounded-2xl border border-border bg-background/95 p-6 shadow-2xl backdrop-blur-xl"
          >
            <div className="flex items-center justify-between pb-4 border-b border-border">
              <h2 className="text-lg font-semibold flex items-center gap-2">
                <FileText className="h-5 w-5 text-primary" />
                Knowledge Base Management
              </h2>
              <button onClick={onClose} className="rounded-lg p-1 text-muted-foreground hover:bg-muted">
                <X className="h-5 w-5" />
              </button>
            </div>

            {error && (
              <div className="mt-4 rounded-lg bg-destructive/15 border border-destructive/30 p-3 text-xs text-destructive">
                {error}
              </div>
            )}

            <div className="mt-4">
              <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-border rounded-xl cursor-pointer bg-muted/20 hover:bg-muted/40 transition">
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  <Upload className="w-8 h-8 mb-2 text-muted-foreground" />
                  <p className="mb-1 text-sm font-semibold">
                    {uploading ? "Uploading PDF & generating embeddings..." : "Click to upload PDF Document"}
                  </p>
                  <p className="text-xs text-muted-foreground">PDF files up to 50MB</p>
                </div>
                <input type="file" accept=".pdf" className="hidden" onChange={handleFileUpload} disabled={uploading} />
              </label>
            </div>

            <div className="mt-6">
              <h3 className="text-xs font-semibold uppercase text-muted-foreground tracking-wider mb-3">
                Uploaded Documents ({documents.length})
              </h3>
              <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
                {documents.length === 0 ? (
                  <p className="text-xs text-muted-foreground italic text-center py-4">No documents uploaded yet.</p>
                ) : (
                  documents.map((doc) => (
                    <div
                      key={doc.id}
                      className="flex items-center justify-between p-3 rounded-xl border border-border/80 bg-muted/30"
                    >
                      <div className="flex items-center gap-3">
                        <FileText className="h-5 w-5 text-primary" />
                        <div>
                          <p className="text-sm font-medium">{doc.original_filename}</p>
                          <p className="text-[11px] text-muted-foreground font-mono">
                            {(doc.file_size / 1024).toFixed(1)} KB
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-1 text-xs">
                        {doc.status === "ready" ? (
                          <span className="flex items-center gap-1 text-emerald-500 font-medium">
                            <CheckCircle2 className="h-4 w-4" /> Ready
                          </span>
                        ) : doc.status === "failed" ? (
                          <span className="flex items-center gap-1 text-destructive font-medium">
                            <AlertCircle className="h-4 w-4" /> Failed
                          </span>
                        ) : (
                          <span className="flex items-center gap-1 text-amber-500 font-medium">
                            <Clock className="h-4 w-4 animate-spin" /> Processing
                          </span>
                        )}
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
