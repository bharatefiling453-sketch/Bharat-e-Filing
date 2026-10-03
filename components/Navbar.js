"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <nav
      id="main-nav"
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? "glass-card shadow-lg shadow-black/20 py-4"
          : "bg-transparent py-6"
      }`}
    >
      <div className="max-w-6xl mx-auto px-6 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2.5 group" id="logo-link">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-emerald-500 flex items-center justify-center font-bold text-white text-base transition-transform group-hover:scale-110 shadow-md shadow-indigo-500/10">
            Bf
          </div>
          <span className="text-xl font-bold tracking-tight text-white">
            Bharat<span className="gradient-text">eFiling</span>
          </span>
        </Link>

        {/* Action Button */}
        {pathname !== "/filing" && (
          <div>
            <Link
              href="/filing"
              id="nav-cta"
              className="px-6 py-2.5 rounded-full text-sm font-semibold bg-gradient-to-r from-indigo-500 to-emerald-500 text-white hover:shadow-lg hover:shadow-indigo-500/25 transition-all duration-200 hover:-translate-y-0.5"
            >
              Start Filing
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
}
