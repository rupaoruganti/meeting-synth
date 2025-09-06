// app/layout.tsx
import "./globals.css";
import Link from "next/link";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col bg-gray-900 text-gray-100">
        {/* Navbar */}
        <nav className="bg-gray-800/80 backdrop-blur-md fixed w-full z-50 shadow-lg">
          <div className="max-w-7xl mx-auto flex justify-between items-center p-4">
            <h1 className="text-2xl font-bold tracking-widest text-indigo-400">🌌 Meeting Synth</h1>
            <div className="flex gap-6">
              <Link href="/" className="hover:text-indigo-300 transition-colors">Home</Link>
              <Link href="/login" className="hover:text-indigo-300 transition-colors">Login</Link>
              <Link href="/register" className="hover:text-indigo-300 transition-colors">Register</Link>
            </div>
          </div>
        </nav>

        {/* Page content */}
        <main className="flex-grow pt-24">{children}</main>

        {/* Footer */}
        <footer className="bg-gray-800 text-gray-400 text-center p-4 mt-auto">
          © 2025 My Dark App. All rights reserved.
        </footer>
      </body>
    </html>
  );
}