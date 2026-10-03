"use client";

import dynamic from "next/dynamic";
import { 
  FileTextIcon, 
  DocumentIcon, 
  DownloadIcon 
} from "./Icons";

import { printTaxComputation } from "@/utils/pdfGenerator";

// dynamically import react-json-view to prevent SSR issues in Next.js
const JsonViewer = dynamic(() => import("@uiw/react-json-view"), { ssr: false });

export default function OutputJsonViewer({ data, onDownload, uploadedFiles }) {
  return (
    <div className="glass-card rounded-2xl p-6 sm:p-8 flex flex-col h-full min-h-[500px]">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <DocumentIcon className="w-5 h-5 text-emerald-400" /> Compiled Draft JSON
        </h2>

        {data && (
          <div className="flex items-center gap-3">
            <button
              onClick={() => printTaxComputation(data, uploadedFiles)}
              className="px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-surface hover:bg-surface-elevated text-text-muted hover:text-white border border-border transition-colors flex items-center gap-1.5 cursor-pointer"
            >
              <svg className="w-3.5 h-3.5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
              </svg>
              Print Computation PDF
            </button>
            <button
              onClick={onDownload}
              className="px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-surface hover:bg-surface-elevated text-text-muted hover:text-white border border-border transition-colors flex items-center gap-1.5 cursor-pointer"
            >
              <DownloadIcon className="w-3.5 h-3.5 text-emerald-400" /> Download JSON
            </button>
          </div>
        )}
      </div>

      {/* Body Content */}
      {data ? (
        <div className="flex-1 bg-[#030712]/45 border border-border/80 rounded-xl overflow-hidden flex flex-col">
          {/* Top Panel Info */}
          <div className="bg-surface/85 px-4 py-2.5 border-b border-border/80 flex items-center justify-between text-xs text-text-muted select-none">
            <span>Draft payload preview</span>
            <span className="font-mono text-[10px] bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 px-2 py-0.5 rounded-full">
              schema v1.0
            </span>
          </div>
          
          {/* Interactive Collapsible Tree View */}
          <div className="flex-1 p-4 overflow-auto max-h-[460px] select-text">
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
      ) : (
        /* Empty State */
        <div className="flex-1 flex flex-col items-center justify-center text-center p-8 border border-dashed border-border rounded-xl bg-surface/10 select-none">
          <FileTextIcon className="w-12 h-12 text-text-muted/40 mb-4" />
          <h3 className="font-bold text-white text-base">No Draft Generated</h3>
          <p className="text-xs text-text-muted max-w-sm mt-2">
            Select and upload at least one document source, then click the generate button on the left to compile your draft payload.
          </p>
        </div>
      )}
    </div>
  );
}
