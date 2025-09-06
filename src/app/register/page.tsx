"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function RegisterPage() {
  const [name, setName] = useState("");
  const [userEmail, setUserEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("");
  const [domain, setDomain] = useState("");
  const [email, setEmail] = useState("");

  const router = useRouter();

  const handleRegister = (e: React.FormEvent) => {
    e.preventDefault();

    let emailGenerated = "";
    const cleanName = name.toLowerCase().replace(/\s+/g, "");
    const cleanRole = role.toLowerCase().replace(/\s+/g, "");
    const cleanDomain = domain.toLowerCase();

    if (role === "Vice President") {
      emailGenerated = `${cleanName}@${cleanRole}.com`;
    } else {
      emailGenerated = `${cleanName}@${cleanRole}.${cleanDomain}.com`;
    }

    setEmail(emailGenerated);

    // ✅ Redirect to scheduler after register
    router.push("/scheduler");
  };

  return (
    <div className="flex items-center justify-center min-h-[80vh] bg-gray-900 p-4">
      <div className="bg-gray-800 rounded-3xl shadow-2xl p-10 w-full max-w-md relative overflow-hidden border border-gray-700">
        <h2 className="text-3xl font-bold text-center mb-6 text-indigo-400">
          Register ✨
        </h2>

        <form className="flex flex-col gap-4" onSubmit={handleRegister}>
          <input
            type="text"
            placeholder="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="p-3 rounded-xl border border-gray-600 bg-gray-900 text-gray-100 placeholder-gray-500 
                       focus:outline-none focus:ring-2 focus:ring-indigo-400 transition"
            required
          />

          <input
            type="email"
            placeholder="Email"
            value={userEmail}
            onChange={(e) => setUserEmail(e.target.value)}
            className="p-3 rounded-xl border border-gray-600 bg-gray-900 text-gray-100 placeholder-gray-500 
                       focus:outline-none focus:ring-2 focus:ring-indigo-400 transition"
            required
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="p-3 rounded-xl border border-gray-600 bg-gray-900 text-gray-100 placeholder-gray-500 
                       focus:outline-none focus:ring-2 focus:ring-indigo-400 transition"
            required
          />

          <select
            value={role}
            onChange={(e) => {
              setRole(e.target.value);
              if (e.target.value === "Vice President") setDomain("");
            }}
            required
            className="p-3 rounded-xl border border-gray-600 bg-gray-900 text-gray-100 
                       focus:outline-none focus:ring-2 focus:ring-indigo-400 transition"
          >
            <option value="">Select Role</option>
            <option>Vice President</option>
            <option>Team Lead</option>
            <option>Teammate</option>
          </select>

          {role !== "Vice President" && (
            <select
              value={domain}
              onChange={(e) => setDomain(e.target.value)}
              required
              className="p-3 rounded-xl border border-gray-600 bg-gray-900 text-gray-100 
                         focus:outline-none focus:ring-2 focus:ring-indigo-400 transition"
            >
              <option value="">Select Domain</option>
              <option>Frontend</option>
              <option>Backend</option>
              <option>Database</option>
            </select>
          )}

          <button
            type="submit"
            className="bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-2xl font-semibold shadow-lg 
                       transform hover:scale-105 transition-all mt-3"
          >
            Register
          </button>
        </form>

        {email && (
          <p className="mt-4 text-lg text-green-400 text-center">
            Generated Email: <span className="font-bold">{email}</span>
          </p>
        )}
      </div>
    </div>
  );
}
