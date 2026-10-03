"use client";

import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import dynamic from "next/dynamic";

// dynamically import react-json-view to prevent SSR issues in Next.js
const JsonViewer = dynamic(() => import("@uiw/react-json-view"), { ssr: false });

export default function JsonViewerModal({ isOpen, title, data, onClose }) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    return () => setMounted(false);
  }, []);

  if (!isOpen) return null;
  if (!mounted) return null;

  return createPortal(
    <div 
      onClick={onClose}
      className="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
    >
      <div 
        onClick={(e) => e.stopPropagation()}
        className="glass-card w-full max-w-2xl rounded-2xl flex flex-col max-h-[85vh] border border-border shadow-2xl overflow-hidden animate-fade-in-up"
      >
        {/* Modal Header */}
        <div className="px-6 py-4 bg-surface/80 border-b border-border flex items-center justify-between">
          <h3 className="font-bold text-white text-sm sm:text-base truncate mr-4">
            Viewing: {title}
          </h3>
          <button 
            onClick={onClose}
            className="text-xs font-semibold text-text-muted hover:text-white px-3 py-1.5 rounded-lg bg-surface hover:bg-surface-elevated border border-border transition-colors cursor-pointer"
          >
            Close
          </button>
        </div>
        {/* Modal Content */}
        <div className="flex-1 p-6 overflow-auto bg-[#030712]/60 select-text max-h-[60vh]">
          <JsonViewer 
            value={data} 
            displayDataTypes={false}
            displayObjectSize={false}
            enableClipboard={false}
            style={{
              "--w-rjv-color": "#a5b4fc", // indigo-300
              "--w-rjv-key-number": "#34d399", // emerald-400
              "--w-rjv-key-string": "#34d399", // emerald-400
              "--w-rjv-background-color": "transparent",
              fontFamily: "monospace",
              fontSize: "12px",
            }}
          />
        </div>
      </div>
    </div>,
    document.body
  );
}
