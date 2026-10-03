"use client";

import { useEffect, useState } from "react";
import { createPortal } from "react-dom";

export default function PdfViewerModal({ isOpen, title, fileUrl, onClose }) {
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
        className="glass-card w-full max-w-4xl h-[85vh] rounded-2xl flex flex-col border border-border shadow-2xl overflow-hidden animate-fade-in-up"
      >
        {/* Modal Header */}
        <div className="px-6 py-4 bg-surface/80 border-b border-border flex items-center justify-between">
          <h3 className="font-bold text-white text-sm sm:text-base truncate mr-4">
            Viewing PDF: {title}
          </h3>
          <button 
            onClick={onClose}
            className="text-xs font-semibold text-text-muted hover:text-white px-3 py-1.5 rounded-lg bg-surface hover:bg-surface-elevated border border-border transition-colors cursor-pointer"
          >
            Close
          </button>
        </div>
        {/* Modal Content - Native PDF rendering frame */}
        <div className="flex-1 bg-[#0f172a]">
          <iframe 
            src={fileUrl} 
            className="w-full h-full border-0"
            title={title}
          />
        </div>
      </div>
    </div>,
    document.body
  );
}
