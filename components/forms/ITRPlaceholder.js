"use client";

import { SparklesIcon } from "../Icons";

export default function ITRPlaceholder({ formName, onBackToItr1 }) {
  return (
    <div className="glass-card rounded-2xl p-8 sm:p-12 text-center max-w-xl mx-auto flex flex-col items-center border border-border/60 animate-fade-in-up">
      <div className="w-14 h-14 rounded-full bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-6 animate-pulse">
        <SparklesIcon className="w-6 h-6" />
      </div>
      <h2 className="text-xl font-bold text-white mb-2">
        {formName.toUpperCase()} Payload Builder Coming Soon
      </h2>
      <p className="text-xs text-text-muted max-w-sm mb-8 leading-relaxed">
        Aggregation and draft JSON generation logic for {formName.toUpperCase()} returns is currently under active development and compliance mapping.
      </p>
      <button
        onClick={onBackToItr1}
        className="px-6 py-2.5 rounded-full bg-surface-elevated hover:bg-surface border border-border text-xs font-semibold text-white transition-colors cursor-pointer"
      >
        Back to ITR-1 Filing
      </button>
    </div>
  );
}
