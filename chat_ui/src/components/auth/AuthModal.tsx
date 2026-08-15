import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Lock, Mail, User as UserIcon, LogIn, UserPlus } from "lucide-react";

interface AuthModalProps {
  open: boolean;
  onClose: () => void;
  onSuccess: (token: string, email: string) => void;
}

export function AuthModal({ open, onClose, onSuccess }: AuthModalProps) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const baseUrl = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

    try {
      if (isLogin) {
        const formData = new URLSearchParams();
        formData.append("username", email);
        formData.append("password", password);

        const res = await fetch(`${baseUrl}/api/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: formData,
        });

        if (!res.ok) {
          const errData = await res.json().catch(() => ({}));
          throw new Error(errData.detail || "Login failed");
        }

        const data = await res.json();
        localStorage.setItem("access_token", data.access_token);
        onSuccess(data.access_token, email);
        onClose();
      } else {
        const res = await fetch(`${baseUrl}/api/auth/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password, full_name: fullName }),
        });

        if (!res.ok) {
          const errData = await res.json().catch(() => ({}));
          throw new Error(errData.detail || "Registration failed");
        }

        setIsLogin(true);
        setError("Account created! Please log in.");
      }
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred");
    } finally {
      setLoading(false);
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
            className="w-full max-w-md rounded-2xl border border-border bg-background/95 p-6 shadow-2xl backdrop-blur-xl"
          >
            <div className="flex items-center justify-between pb-4 border-b border-border">
              <h2 className="text-lg font-semibold flex items-center gap-2">
                {isLogin ? <LogIn className="h-5 w-5 text-primary" /> : <UserPlus className="h-5 w-5 text-primary" />}
                {isLogin ? "Sign In to Vibrantic AI" : "Create an Account"}
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

            <form onSubmit={handleSubmit} className="mt-4 space-y-4">
              {!isLogin && (
                <div>
                  <label className="block text-xs font-medium text-muted-foreground mb-1">Full Name</label>
                  <div className="relative">
                    <UserIcon className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
                    <input
                      type="text"
                      required
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                      placeholder="Alex Rivera"
                      className="w-full rounded-xl border border-border bg-muted/40 pl-9 pr-3 py-2 text-sm focus:border-primary focus:outline-none"
                    />
                  </div>
                </div>
              )}

              <div>
                <label className="block text-xs font-medium text-muted-foreground mb-1">Email Address</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="user@vibrantic.ai"
                    className="w-full rounded-xl border border-border bg-muted/40 pl-9 pr-3 py-2 text-sm focus:border-primary focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-muted-foreground mb-1">Password</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full rounded-xl border border-border bg-muted/40 pl-9 pr-3 py-2 text-sm focus:border-primary focus:outline-none"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-xl bg-gradient-primary py-2.5 text-sm font-semibold text-primary-foreground shadow-glow hover:opacity-90 disabled:opacity-50"
              >
                {loading ? "Processing..." : isLogin ? "Sign In" : "Register"}
              </button>
            </form>

            <div className="mt-4 text-center text-xs text-muted-foreground">
              {isLogin ? "Don't have an account?" : "Already registered?"}{" "}
              <button onClick={() => setIsLogin(!isLogin)} className="font-semibold text-primary hover:underline">
                {isLogin ? "Create one" : "Sign in"}
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
