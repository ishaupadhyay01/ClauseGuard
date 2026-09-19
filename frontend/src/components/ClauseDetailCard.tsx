import React from 'react';
import { ClauseResult } from '@/types/schema';
import { ShieldAlert, AlertTriangle, CheckCircle2, Tag, Info, Cpu, FileText } from 'lucide-react';

interface ClauseDetailCardProps {
  clause: ClauseResult | null;
}

export default function ClauseDetailCard({ clause }: ClauseDetailCardProps) {
  if (!clause) {
    return (
      <div className="bg-white rounded-2xl p-8 shadow-sm border border-slate-200 text-center flex flex-col items-center justify-center min-h-[400px]">
        <div className="p-4 bg-slate-50 border border-slate-200 rounded-2xl mb-4 text-slate-400">
          <Info className="w-8 h-8" />
        </div>
        <h4 className="font-semibold text-slate-700 text-base">No Clause Selected</h4>
        <p className="text-xs text-slate-500 max-w-xs mt-1">
          Click any highlighted clause in the document viewer to inspect its risk analysis, matched pattern, and plain-English explanation.
        </p>
      </div>
    );
  }

  const isHigh = clause.risk_level === 'high';
  const isMedium = clause.risk_level === 'medium';
  const isLow = clause.risk_level === 'low';

  return (
    <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-200 space-y-6 sticky top-24">
      {/* Header Badge */}
      <div className="flex items-center justify-between border-b border-slate-100 pb-4">
        <div className="flex items-center gap-2">
          <span className="font-mono text-xs font-bold px-2.5 py-1 bg-slate-100 border border-slate-200 rounded-lg text-slate-700">
            {clause.clause_id}
          </span>
          {clause.position.page && (
            <span className="text-xs text-slate-400 font-medium">Page {clause.position.page}</span>
          )}
        </div>

        {/* Engine Used */}
        <span className="text-xs font-mono text-slate-500 bg-slate-50 border border-slate-200 px-2.5 py-1 rounded-full flex items-center gap-1.5">
          <Cpu className="w-3.5 h-3.5 text-slate-600" />
          {clause.engine_used === 'fallback' ? 'Rule-Based Fallback' : 'Gemini AI RAG'}
        </span>
      </div>

      {/* Risk Level Badge */}
      <div className="space-y-1">
        <label className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
          Risk Assessment
        </label>
        {isHigh && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-xl flex items-center gap-2.5 text-red-800 font-semibold text-sm">
            <ShieldAlert className="w-5 h-5 text-red-600 shrink-0" />
            <span>High Risk Flagged</span>
          </div>
        )}
        {isMedium && (
          <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl flex items-center gap-2.5 text-amber-800 font-semibold text-sm">
            <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0" />
            <span>Medium Risk Flagged</span>
          </div>
        )}
        {isLow && (
          <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center gap-2.5 text-emerald-800 font-semibold text-sm">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
            <span>Low Risk / Standard Clause</span>
          </div>
        )}
      </div>

      {/* Matched Pattern Details */}
      {clause.matched_pattern.pattern_name ? (
        <div className="space-y-2">
          <label className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
            Matched Risk Pattern
          </label>
          <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
            <h5 className="font-bold text-slate-900 text-sm">{clause.matched_pattern.pattern_name}</h5>
            {clause.matched_pattern.category && (
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold rounded-md">
                <Tag className="w-3 h-3" />
                {clause.matched_pattern.category}
              </span>
            )}
          </div>
        </div>
      ) : (
        <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-500">
          No matching high-risk pattern found in seed knowledge base.
        </div>
      )}

      {/* Plain-English Explanation */}
      <div className="space-y-1.5">
        <label className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
          Plain-English Explanation
        </label>
        <div className="p-4 bg-slate-900 text-slate-100 rounded-xl text-sm leading-relaxed font-sans shadow-inner">
          {clause.explanation}
        </div>
      </div>

      {/* Clause Original Text Snippet */}
      <div className="space-y-1.5">
        <label className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
          Original Clause Text
        </label>
        <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-700 font-serif italic max-h-40 overflow-y-auto">
          "{clause.clause_text}"
        </div>
      </div>
    </div>
  );
}
