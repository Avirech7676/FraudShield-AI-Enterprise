import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ShieldAlert, User, Mail, Lock, ArrowRight, ShieldCheck } from "lucide-react";

import { register } from "../services/auth";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import { Select } from "../components/ui/Select";
import { ThemeToggle } from "../components/ui/ThemeToggle";

export default function Register() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    role: "Analyst",
  });

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setMessage("");

    if (form.password !== form.confirmPassword) {
      setMessage("Passwords do not match");
      return;
    }

    setLoading(true);

    try {
      const result = await register({
        username: form.username,
        email: form.email,
        password: form.password,
        role: form.role,
      });

      setMessage(result.message || "Account created successfully!");
      setTimeout(() => {
        navigate("/login");
      }, 1200);
    } catch (err: any) {
      const serverDetail = err.response?.data?.detail;
      const errorMsg = serverDetail ? `${serverDetail}. Try signing in or use another username.` : (err.message || "Registration failed. Please try again.");
      setMessage(errorMsg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen w-full bg-slate-950 flex items-center justify-center p-4 md:p-8 selection:bg-indigo-500 selection:text-white relative overflow-hidden">
      {/* Background Glow */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-600/15 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-600/15 rounded-full blur-3xl pointer-events-none" />

      {/* Top Bar Theme Toggle */}
      <div className="absolute top-6 right-6 z-20">
        <ThemeToggle />
      </div>

      <div className="w-full max-w-5xl bg-slate-900/80 border border-slate-800/80 backdrop-blur-2xl rounded-3xl shadow-2xl shadow-black/80 grid grid-cols-1 lg:grid-cols-12 overflow-hidden z-10">
        {/* Left Hero Banner */}
        <div className="lg:col-span-5 p-8 lg:p-12 bg-gradient-to-br from-indigo-950/40 via-slate-900 to-slate-950 border-b lg:border-b-0 lg:border-r border-slate-800/80 flex flex-col justify-between relative">
          <div>
            <div className="flex items-center gap-3 mb-8">
              <div className="w-12 h-12 rounded-2xl bg-indigo-600 flex items-center justify-center text-white shadow-xl shadow-indigo-600/40 border border-indigo-400/30">
                <ShieldAlert className="w-7 h-7" />
              </div>
              <div className="flex flex-col">
                <span className="text-xl font-bold text-white tracking-tight leading-none">
                  FraudShield
                </span>
                <span className="text-xs font-semibold text-indigo-400 uppercase tracking-widest mt-1">
                  Enterprise AI
                </span>
              </div>
            </div>

            <h1 className="text-2xl lg:text-3xl font-bold text-slate-100 tracking-tight leading-tight mb-4">
              Join the Fraud Investigation Ops
            </h1>
            <p className="text-sm text-slate-400 leading-relaxed mb-8">
              Provision an analyst or administrator account to manage threat alerts, investigate cases, and trigger model retrains.
            </p>

            <div className="space-y-4">
              <div className="flex items-center gap-3 p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                <ShieldCheck className="w-5 h-5 text-indigo-400" />
                <span className="text-xs font-semibold text-slate-200">Role-Based Security Policy</span>
              </div>
              <div className="flex items-center gap-3 p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                <ShieldCheck className="w-5 h-5 text-indigo-400" />
                <span className="text-xs font-semibold text-slate-200">Immutable Security Audit Logs</span>
              </div>
              <div className="flex items-center gap-3 p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                <ShieldCheck className="w-5 h-5 text-indigo-400" />
                <span className="text-xs font-semibold text-slate-200">Real-Time Risk Webhooks</span>
              </div>
            </div>
          </div>

          <div className="mt-8 pt-6 border-t border-slate-800/80 text-xs text-slate-500">
            Enterprise Identity Protection
          </div>
        </div>

        {/* Right Form Panel */}
        <div className="lg:col-span-7 p-8 lg:p-12 flex flex-col justify-center">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-slate-100 tracking-tight">
              Create Analyst Account
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Complete the security clearance form to get access.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Username"
              id="reg-username"
              type="text"
              placeholder="Choose a operational handle"
              value={form.username}
              onChange={(e) => setForm({ ...form, username: e.target.value })}
              leftIcon={<User className="w-4 h-4" />}
              required
            />

            <Input
              label="Corporate Email"
              id="reg-email"
              type="email"
              placeholder="you@company.com"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              leftIcon={<Mail className="w-4 h-4" />}
              required
            />

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="Password"
                id="reg-password"
                type="password"
                placeholder="Strong password"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                leftIcon={<Lock className="w-4 h-4" />}
                required
              />

              <Input
                label="Confirm Password"
                id="reg-confirm"
                type="password"
                placeholder="Confirm password"
                value={form.confirmPassword}
                onChange={(e) => setForm({ ...form, confirmPassword: e.target.value })}
                leftIcon={<Lock className="w-4 h-4" />}
                required
              />
            </div>

            <Select
              label="Security Clearance Role"
              id="reg-role"
              value={form.role}
              onChange={(e) => setForm({ ...form, role: e.target.value })}
              options={[
                { value: "Analyst", label: "Analyst (Standard Threat Investigation)" },
                { value: "Admin", label: "Admin (Full System & Model Access)" },
              ]}
            />

            {message && (
              <div
                className={`p-3.5 rounded-xl text-xs font-medium border ${
                  message.includes("success")
                    ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-300"
                    : "bg-rose-500/10 border-rose-500/30 text-rose-300"
                }`}
              >
                {message}
              </div>
            )}

            <Button
              type="submit"
              size="lg"
              fullWidth
              isLoading={loading}
              rightIcon={<ArrowRight className="w-4 h-4" />}
            >
              Create Account
            </Button>
          </form>

          <div className="mt-6 text-center text-xs text-slate-400">
            Already registered?{" "}
            <Link
              to="/login"
              className="text-indigo-400 hover:text-indigo-300 font-semibold underline underline-offset-4 ml-1 transition-colors"
            >
              Sign In
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}