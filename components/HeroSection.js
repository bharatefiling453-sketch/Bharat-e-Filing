import Link from "next/link";
import { 
  ShieldCheckIcon, 
  SparklesIcon, 
  CheckCircleIcon, 
  ArrowRightIcon 
} from "@/components/Icons";

export default function HeroSection() {
  return (
    <section
      id="hero"
      className="relative flex flex-col items-center justify-center overflow-hidden noise-overlay px-6 pt-36 pb-24 sm:pt-48 sm:pb-36"
    >
      {/* Background gradient orbs */}
      <div className="absolute top-1/4 -left-32 w-[350px] h-[350px] sm:w-[500px] sm:h-[500px] bg-indigo-600/15 rounded-full blur-[120px] animate-pulse-glow" />
      <div className="absolute bottom-1/4 -right-32 w-[350px] h-[350px] sm:w-[500px] sm:h-[500px] bg-emerald-600/15 rounded-full blur-[120px] animate-pulse-glow delay-700" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] sm:w-[700px] sm:h-[700px] bg-violet-600/10 rounded-full blur-[140px]" />

      <div className="relative z-10 max-w-4xl mx-auto text-center flex flex-col items-center">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-border bg-surface/60 backdrop-blur-md mb-8 animate-fade-in-up">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-xs font-semibold tracking-wide text-text-muted">
            AY 2026–27 FILING IS ACTIVE
          </span>
        </div>

        {/* Heading */}
        <h1 className="text-4xl sm:text-6xl md:text-7xl font-extrabold leading-[1.15] tracking-tight text-white px-2 sm:px-4 animate-fade-in-up delay-100">
          File Your Income Tax
          <span className="block mt-2 gradient-text">Effortlessly.</span>
        </h1>

        {/* Sub-heading */}
        <p className="mt-8 max-w-2xl mx-auto text-base sm:text-lg md:text-xl text-text-muted leading-relaxed px-4 animate-fade-in-up delay-200">
          Auto-import your AIS &amp; TIS, map transactions instantly with AI guidance, and e-verify in minutes. India&apos;s most secure, simple tax e-filing platform.
        </p>

        {/* CTA buttons */}
        <div className="mt-12 w-full flex flex-col sm:flex-row items-center justify-center gap-5 px-4 animate-fade-in-up delay-300">
          <Link
            href="/filing"
            id="hero-cta-primary"
            className="group w-full sm:w-auto px-8 py-4 rounded-full bg-gradient-to-r from-indigo-500 to-emerald-500 text-white font-bold text-base shadow-xl shadow-indigo-500/20 hover:shadow-indigo-500/40 transition-all duration-200 hover:-translate-y-0.5 flex items-center justify-center gap-2.5"
          >
            Start Filing Free
            <ArrowRightIcon className="w-5 h-5 transition-transform group-hover:translate-x-1" />
          </Link>
          <a
            href="#learn-more"
            id="hero-cta-secondary"
            className="w-full sm:w-auto px-8 py-4 rounded-full border border-border bg-surface/20 text-white font-bold text-base hover:bg-surface-elevated/40 transition-all duration-200 flex items-center justify-center"
          >
            Learn More
          </a>
        </div>

        {/* Trust badges */}
        <div className="mt-16 flex flex-col sm:flex-row flex-wrap items-center justify-center gap-y-4 gap-x-8 text-sm text-text-muted animate-fade-in delay-500 px-4">
          <div className="flex items-center gap-2">
            <ShieldCheckIcon className="w-5 h-5 text-emerald-400" />
            256-bit SSL Encrypted
          </div>
          <div className="flex items-center gap-2">
            <CheckCircleIcon className="w-5 h-5 text-emerald-400" />
            GSTIN Certified
          </div>
          <div className="flex items-center gap-2">
            <SparklesIcon className="w-5 h-5 text-emerald-400" />
            Income Tax Dept. Compliant
          </div>
        </div>
      </div>
    </section>
  );
}
