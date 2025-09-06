// app/page.tsx
import Link from "next/link";

export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] bg-gray-900 text-gray-100">
      <h1 className="text-5xl md:text-6xl font-extrabold text-indigo-400 mb-8 animate-pulse text-center">
        Welcome to Meeting Synth 🌌
      </h1>

      <p className="text-lg md:text-xl text-gray-300 text-center mb-12">
        Experience a sleek, modern dark UI for registration & login
      </p>

      <div className="flex gap-6 flex-col md:flex-row">
        <Link
          href="/login"
          className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-4 px-10 rounded-xl shadow-lg transform hover:scale-105 transition-all"
        >
          Login
        </Link>

        <Link
          href="/register"
          className="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-4 px-10 rounded-xl shadow-lg transform hover:scale-105 transition-all"
        >
          Register
        </Link>
      </div>
    </div>
  );
}
