"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowLeftIcon } from "./Icons";
import { formRegistry, componentMap } from "@/components/forms";

export default function FilingDashboard() {
  // active return type tab selector (defaults to first form in registry)
  const [activeTab, setActiveTab] = useState(formRegistry[0]?.id || "itr1");

  // resolve current active form metadata and component reference
  const activeForm = formRegistry.find((f) => f.id === activeTab);
  const ActiveFormComponent = componentMap[activeForm?.componentName] || (() => null);

  return (
    <div className="max-w-6xl mx-auto px-6 pt-32 pb-24">
      {/* Header section */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 mb-8">
        <div>
          <Link href="/" className="inline-flex items-center gap-2 text-sm text-text-muted hover:text-white mb-4 transition-colors">
            <ArrowLeftIcon className="w-4 h-4" /> Back to Home
          </Link>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Tax Document <span className="gradient-text">Bookkeeper</span>
          </h1>
          <p className="mt-2 text-text-muted text-sm sm:text-base max-w-xl">
            Choose your tax return type, upload required reports, and compile the final draft JSON payload.
          </p>
        </div>
      </div>

      {/* Dynamic Horizontal Tab Bar from Registry */}
      <div className="flex border-b border-border/80 gap-6 mb-8 overflow-x-auto select-none no-scrollbar">
        {formRegistry.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`pb-4 text-left border-b-2 transition-all duration-200 cursor-pointer min-w-[125px] flex-shrink-0 ${
              activeTab === tab.id
                ? "border-emerald-500 text-white font-bold"
                : "border-transparent text-text-muted hover:text-white"
            }`}
          >
            <div className="text-sm font-semibold">{tab.label}</div>
            <div className="text-[10px] text-text-muted mt-0.5 font-normal">{tab.desc}</div>
          </button>
        ))}
      </div>

      {/* Dynamic Tab Panel Content switcher */}
      <ActiveFormComponent onBackToItr1={() => setActiveTab("itr1")} />
    </div>
  );
}
