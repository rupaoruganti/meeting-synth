"use client";
import { useState } from "react";

export default function RegisterPage() {
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("");
  const [domain, setDomain] = useState("");
  const [email, setEmail] = useState("");

  const handleRegister = async (e: React.FormEvent) => {
  e.preventDefault();
  const cleanName = name.toLowerCase().trim().replace(/\s+/g, "");
  const cleanRole = role.toLowerCase().trim().replace(/\s+/g, "");
  const cleanDomain = domain.toLowerCase().trim();

  let emailGenerated =
    role === "Vice President"
      ? `${cleanName}@${cleanRole}.com`
      : `${cleanName}@${cleanRole}.${cleanDomain}.com`;

  setEmail(emailGenerated);

  // Send data to backend
  const res = await fetch("/api/register", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    name,
    email: emailGenerated,
    phone,
    password,
    role,
    domain,
  }),
});


  const data = await res.json();
  console.log("Response:", data);
};


  return (
    <div className="flex items-center justify-center min-h-[80vh] bg-gray-900 p-4">
      <div className="bg-gray-800 rounded-3xl shadow-2xl p-10 w-full max-w-md relative overflow-hidden border border-gray-700">
        <h2 className="text-3xl font-bold text-center mb-6 text-indigo-400">Register ✨</h2>

        <form className="flex flex-col gap-4" onSubmit={handleRegister}>
          <input
            type="text"
            placeholder="Name"
            value={name}
            onChange={e => setName(e.target.value)}
            className="p-3 rounded-xl border border-gray-600 bg-gray-900 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-400 transition"
            required
          />
          <input
            type="tel"
            placeholder="Phone"
            value={phone}
            onChange={e => setPhone(e.target.value)}
            className="p-3 rounded-xl border border-gray-600 bg-gray-900 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-400 transition"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            className="p-3 rounded-xl border border-gray-600 bg-gray-900 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-400 transition"
            required
          />
          <select
            value={role}
            onChange={e => { setRole(e.target.value); if (e.target.value === "Vice President") setDomain(""); }}
            className="p-3 rounded-xl border border-gray-600 bg-gray-900 text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-400 transition"
            required
          >
            <option value="">Select Role</option>
            <option>Vice President</option>
            <option>Team Lead</option>
            <option>Teammate</option>
          </select>

          {role !== "Vice President" && (
            <select
              value={domain}
              onChange={e => setDomain(e.target.value)}
              className="p-3 rounded-xl border border-gray-600 bg-gray-900 text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-400 transition"
              required
            >
              <option value="">Select Domain</option>
              <option>Frontend</option>
              <option>Backend</option>
              <option>Database</option>
            </select>
          )}

          <button
            type="submit"
            className="bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-2xl font-semibold shadow-lg transform hover:scale-105 transition-all mt-3"
          >
            Register
          </button>
        </form>

        {email && (
          <p className="mt-5 text-center text-lg font-bold text-green-400">
            Generated Email: {email}
          </p>
        )}
      </div>
    </div>
  );
}