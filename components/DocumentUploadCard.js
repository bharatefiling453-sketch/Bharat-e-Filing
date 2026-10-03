"use client";

import { useState, useRef, useEffect } from "react";
import { 
  CheckIcon, 
  RefreshIcon, 
  UploadIcon 
} from "./Icons";
import JsonViewerModal from "./JsonViewerModal";
import PdfViewerModal from "./PdfViewerModal";

export default function DocumentUploadCard({
  id,
  title,
  badgeText,
  description,
  selected,
  onToggle,
  onFileChange,
  onParseFile
}) {
  const fileInputRef = useRef(null);
  
  // self-contained states
  const [loaded, setLoaded] = useState(false);
  const [isSimulatingLoad, setIsSimulatingLoad] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  
  // modal views states
  const [activeJsonView, setActiveJsonView] = useState(null);
  const [activePdfView, setActivePdfView] = useState(null);

  // cleanup blob URL on unmount to prevent memory leaks
  useEffect(() => {
    return () => {
      if (uploadedFile?.fileUrl) {
        URL.revokeObjectURL(uploadedFile.fileUrl);
      }
    };
  }, [uploadedFile]);

  // handle local file uploads (PDF / JSON / Custom Parsed)
  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsSimulatingLoad(true);

    let parsedData = null;
    let isSuccess = true;
    let errorMsg = "";

    try {
      if (onParseFile) {
        // Delegate parsing to parent (e.g. for ZIP decryption)
        parsedData = await onParseFile(file);
      } else if (file.type === "application/json" || file.name.endsWith(".json")) {
        const text = await file.text();
        parsedData = JSON.parse(text);
      } else {
        // PDF format default parsing
        parsedData = {
          documentType: `${id.toUpperCase()} (Extracted PDF)`,
          fileName: file.name,
          fileSize: `${(file.size / 1024).toFixed(1)} KB`,
          extractedAt: new Date().toISOString(),
          notes: "File structure parsed successfully.",
          records: [],
          categories: [],
          taxDeductedAtSource: []
        };
      }
    } catch (err) {
      isSuccess = false;
      errorMsg = err.message || "Failed to process file.";
    }

    setTimeout(() => {
      setIsSimulatingLoad(false);
      if (isSuccess) {
        const fileUrl = URL.createObjectURL(file);
        const fileObj = {
          name: file.name,
          size: `${(file.size / 1024).toFixed(1)} KB`,
          type: file.type || (file.name.endsWith(".pdf") ? "application/pdf" : file.name.endsWith(".zip") ? "application/zip" : "application/octet-stream"),
          source: "upload",
          parsedData: parsedData,
          fileUrl: fileUrl,
        };

        setLoaded(true);
        setUploadedFile(fileObj);
        
        // bubble up parsedData to parent aggregator state
        if (onFileChange) {
          onFileChange(parsedData);
        }
      } else {
        alert(errorMsg);
      }
    }, 900);
  };

  // clear file selection
  const clearFile = () => {
    if (uploadedFile?.fileUrl) {
      URL.revokeObjectURL(uploadedFile.fileUrl);
    }
    setLoaded(false);
    setUploadedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
    
    // notify parent of clear state
    if (onFileChange) {
      onFileChange(null);
    }
  };

  // handle viewing file action
  const viewFile = () => {
    if (!uploadedFile) return;

    if (uploadedFile.type === "application/pdf" || uploadedFile.name.endsWith(".pdf")) {
      setActivePdfView({
        name: uploadedFile.name,
        fileUrl: uploadedFile.fileUrl
      });
    } else {
      setActiveJsonView({
        name: uploadedFile.name,
        data: uploadedFile.parsedData
      });
    }
  };

  return (
    <div 
      className={`p-5 rounded-xl border transition-all duration-200 ${
        selected 
          ? "bg-indigo-950/20 border-indigo-500/30" 
          : "bg-surface/40 border-border/80 opacity-60"
      }`}
    >
      {/* Document Header & Checkbox */}
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start gap-3 w-full">
          <input 
            type="checkbox" 
            id={`checkbox-${id}`}
            checked={selected}
            onChange={onToggle}
            autoComplete="off"
            className="mt-1 w-4.5 h-4.5 rounded border-border text-indigo-600 focus:ring-indigo-500 bg-surface cursor-pointer"
          />
          <label 
            htmlFor={`checkbox-${id}`} 
            className="cursor-pointer flex-1 select-none"
          >
            <div className="font-bold text-sm sm:text-base text-white flex items-center gap-2">
              {title}
              {badgeText && (
                <span className="text-[10px] font-normal px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
                  {badgeText}
                </span>
              )}
            </div>
            <div className="text-xs text-text-muted mt-1">{description}</div>
          </label>
        </div>
      </div>

      {/* Action Zone (Only visible when document is selected) */}
      {selected && (
        <div className="mt-4 pt-4 border-t border-border/60 flex flex-wrap items-center justify-between gap-3">
          {loaded ? (
            <div className="flex items-center justify-between w-full bg-emerald-500/5 border border-emerald-500/20 p-2.5 rounded-lg">
              <div className="flex items-center gap-2 text-xs text-emerald-400 font-semibold min-w-0">
                <CheckIcon className="w-4 h-4 flex-shrink-0" />
                <span className="truncate" title={uploadedFile?.name}>{uploadedFile?.name}</span>
                <span className="text-[10px] text-text-muted">({uploadedFile?.size})</span>
              </div>
              <div className="flex items-center gap-3 ml-2 flex-shrink-0">
                <button 
                  onClick={viewFile}
                  className="text-[10px] font-bold text-indigo-400 hover:text-indigo-300 cursor-pointer transition-colors"
                >
                  View
                </button>
                <button 
                  onClick={clearFile}
                  className="text-[10px] font-bold text-rose-400 hover:text-rose-300 cursor-pointer transition-colors"
                >
                  Clear
                </button>
              </div>
            </div>
          ) : (
            <div className="flex items-center gap-2 w-full justify-between sm:justify-start">
              <input 
                type="file" 
                ref={fileInputRef}
                onChange={handleFileUpload}
                accept=".json,.pdf,.zip,.txt"
                className="hidden"
              />
              <button
                onClick={() => fileInputRef.current?.click()}
                disabled={isSimulatingLoad}
                className="px-3.5 py-2 rounded-lg text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white flex items-center gap-1.5 transition-all cursor-pointer"
              >
                {isSimulatingLoad ? (
                  <>
                    <RefreshIcon className="w-3.5 h-3.5 animate-spin" /> Uploading...
                  </>
                ) : (
                  <>
                    <UploadIcon className="w-3.5 h-3.5" /> Upload PDF/JSON/ZIP
                  </>
                )}
              </button>
            </div>
          )}
        </div>
      )}

      {/* Internal JSON Viewer Modal */}
      <JsonViewerModal 
        isOpen={!!activeJsonView} 
        title={activeJsonView?.name} 
        data={activeJsonView?.data} 
        onClose={() => setActiveJsonView(null)} 
      />

      {/* Internal PDF Viewer Modal */}
      <PdfViewerModal 
        isOpen={!!activePdfView}
        title={activePdfView?.name}
        fileUrl={activePdfView?.fileUrl}
        onClose={() => setActivePdfView(null)}
      />
    </div>
  );
}
