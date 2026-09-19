import React from 'react';
import { AlertCircle, AlertTriangle, CheckCircle2, RotateCcw, FileText } from 'lucide-react';
import { RiskSummary } from '@/types/schema';

interface SummaryBarProps {
  documentName: string;
  totalClauses: number;
  summary: RiskSummary;
  onReset: () => void;
}

export default function SummaryBar({
  documentName,
  totalClauses,
  summary,
  onReset,
}: SummaryBarProps) {
  return (
    <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-200 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
      <div className="flex items-center gap-3">
        <div className="p-2.5 bg-blue-50 border border-blue-100 rounded-xl text-blue-600 shrink-0">
          <FileText className="w-6 h-6" />
        </div>
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">{documentName}</h2>
          <p className="text-sm text-slate-500">
            Analysis complete &bull; <strong className="text-slate-700">{totalClauses} clauses</strong> analyzed
          </p>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-3 w-full md:w-auto justify-between md:justify-end">
        {/* Risk Badges */}
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-red-50 border border-red-200 text-red-700 text-xs font-semibold rounded-full">
            <AlertCircle className="w-3.5 h-3.5 text-red-600" />
            {summary.high} High Risk
          </span>

          <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-amber-50 border border-amber-200 text-amber-700 text-xs font-semibold rounded-full">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
            {summary.medium} Medium Risk
          </span>

          <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-semibold rounded-full">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
            {summary.low} Low Risk
          </span>
        </div>

        {/* Upload New Document Button */}
        <button
          onClick={onReset}
          className="inline-flex items-center gap-1.5 px-3.5 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 border border-slate-200 rounded-xl transition-all"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          Upload New
        </button>
      </div>
    </div>
  );
}
