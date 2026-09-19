import React, { useState } from 'react';
import { ClauseResult } from '@/types/schema';
import { AlertCircle, AlertTriangle, CheckCircle2, Cpu, Filter } from 'lucide-react';

interface DocumentViewerProps {
  clauses: ClauseResult[];
  selectedClauseId: string | null;
  onSelectClause: (clause: ClauseResult) => void;
}

export default function DocumentViewer({
  clauses,
  selectedClauseId,
  onSelectClause,
}: DocumentViewerProps) {
  const [filter, setFilter] = useState<'all' | 'high' | 'medium' | 'low'>('all');

  const filteredClauses = clauses.filter((c) => {
    if (filter === 'all') return true;
    return c.risk_level === filter;
  });

  return (
    <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-200 space-y-4">
      {/* Header with Filter Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-4 gap-3">
        <div>
          <h3 className="font-bold text-slate-800 text-lg">Document Clauses Viewer</h3>
          <p className="text-xs text-slate-400 font-medium">Click any clause to inspect risk analysis</p>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-1.5 bg-slate-100 p-1 rounded-xl">
          <button
            onClick={() => setFilter('all')}
            className={`px-2.5 py-1 text-xs font-semibold rounded-lg transition-all ${
              filter === 'all'
                ? 'bg-white text-slate-800 shadow-sm'
                : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            All ({clauses.length})
          </button>
          <button
            onClick={() => setFilter('high')}
            className={`px-2.5 py-1 text-xs font-semibold rounded-lg transition-all ${
              filter === 'high'
                ? 'bg-red-600 text-white shadow-sm'
                : 'text-red-700 hover:bg-red-50'
            }`}
          >
            High ({clauses.filter((c) => c.risk_level === 'high').length})
          </button>
          <button
            onClick={() => setFilter('medium')}
            className={`px-2.5 py-1 text-xs font-semibold rounded-lg transition-all ${
              filter === 'medium'
                ? 'bg-amber-500 text-white shadow-sm'
                : 'text-amber-700 hover:bg-amber-50'
            }`}
          >
            Med ({clauses.filter((c) => c.risk_level === 'medium').length})
          </button>
          <button
            onClick={() => setFilter('low')}
            className={`px-2.5 py-1 text-xs font-semibold rounded-lg transition-all ${
              filter === 'low'
                ? 'bg-emerald-600 text-white shadow-sm'
                : 'text-emerald-700 hover:bg-emerald-50'
            }`}
          >
            Low ({clauses.filter((c) => c.risk_level === 'low').length})
          </button>
        </div>
      </div>

      {/* Clause List Container */}
      <div className="space-y-3 max-h-[720px] overflow-y-auto pr-1">
        {filteredClauses.length === 0 ? (
          <div className="text-center py-12 text-slate-400 text-sm">
            No clauses match the selected filter criteria.
          </div>
        ) : (
          filteredClauses.map((clause) => {
            const isSelected = selectedClauseId === clause.clause_id;
            const isHigh = clause.risk_level === 'high';
            const isMedium = clause.risk_level === 'medium';
            const isLow = clause.risk_level === 'low';

            return (
              <div
                key={clause.clause_id}
                onClick={() => onSelectClause(clause)}
                className={`p-4 rounded-xl cursor-pointer transition-all duration-150 border ${
                  isSelected
                    ? 'ring-2 ring-blue-500 border-transparent shadow-md'
                    : 'hover:shadow-sm'
                } ${
                  isHigh
                    ? 'border-l-4 border-l-red-500 bg-red-50/40 hover:bg-red-50/70 border-red-200/60'
                    : isMedium
                    ? 'border-l-4 border-l-amber-500 bg-amber-50/40 hover:bg-amber-50/70 border-amber-200/60'
                    : 'border-l-4 border-l-emerald-400 bg-slate-50/50 hover:bg-slate-100/70 border-slate-200/60'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-semibold px-2 py-0.5 bg-white border border-slate-200 rounded text-slate-600">
                      {clause.clause_id}
                    </span>
                    {clause.position.page && (
                      <span className="text-xs text-slate-400 font-medium">
                        Page {clause.position.page}
                      </span>
                    )}
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="text-[11px] font-mono text-slate-400 flex items-center gap-1 bg-slate-100 px-2 py-0.5 rounded">
                      <Cpu className="w-3 h-3 text-slate-500" />
                      {clause.engine_used}
                    </span>

                    {isHigh && (
                      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 text-xs font-semibold bg-red-100 text-red-800 rounded-full">
                        <AlertCircle className="w-3 h-3 text-red-600" /> High Risk
                      </span>
                    )}
                    {isMedium && (
                      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 text-xs font-semibold bg-amber-100 text-amber-800 rounded-full">
                        <AlertTriangle className="w-3 h-3 text-amber-600" /> Medium Risk
                      </span>
                    )}
                    {isLow && (
                      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 text-xs font-semibold bg-emerald-100 text-emerald-800 rounded-full">
                        <CheckCircle2 className="w-3 h-3 text-emerald-600" /> Low Risk
                      </span>
                    )}
                  </div>
                </div>

                {/* Clause Original Text */}
                <p className="text-sm font-serif text-slate-800 leading-relaxed mb-2">
                  "{clause.clause_text}"
                </p>

                {/* Flagged Pattern Banner */}
                {clause.matched_pattern.pattern_name && (
                  <div className="mt-2 text-xs font-medium text-red-700 bg-red-100/60 px-3 py-1.5 rounded-lg border border-red-200/50 flex items-center justify-between">
                    <span>
                      <strong>Matched Pattern:</strong> {clause.matched_pattern.pattern_name}
                    </span>
                    <span className="text-[10px] uppercase tracking-wider font-semibold bg-white/80 px-2 py-0.5 rounded text-red-800">
                      {clause.matched_pattern.category}
                    </span>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
