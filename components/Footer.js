export default function Footer() {
  return (
    <footer className="border-t border-border/80 bg-surface/20 py-12 mt-auto">
      <div className="max-w-6xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-6">
        {/* Brand */}
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-emerald-500 flex items-center justify-center font-bold text-white text-xs shadow-md shadow-indigo-500/10">
            Bf
          </div>
          <span className="text-base font-bold text-white">
            Bharat<span className="gradient-text">eFiling</span>
          </span>
        </div>

        {/* Text details */}
        <div className="text-center sm:text-right">
          <p className="text-xs text-text-muted">
            © {new Date().getFullYear()} BharateFiling. All rights reserved.
          </p>
          <p className="text-[10px] text-text-muted/60 mt-1">
            Compliant with the Income Tax Department of India guidelines.
          </p>
        </div>
      </div>
    </footer>
  );
}
