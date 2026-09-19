'use client';

import React, { useState } from 'react';
import UploadSection from '@/components/UploadSection';
import SummaryBar from '@/components/SummaryBar';
import DocumentViewer from '@/components/DocumentViewer';
import ClauseDetailCard from '@/components/ClauseDetailCard';
import { DocumentAnalysisResponse, ClauseResult } from '@/types/schema';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<DocumentAnalysisResponse | null>(null);
  const [selectedClause, setSelectedClause] = useState<ClauseResult | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0];
      const ext = selected.name.split('.').pop()?.toLowerCase();
      if (ext !== 'pdf' && ext !== 'docx') {
        setError('Unsupported file extension. Only PDF and DOCX documents are allowed.');
        setFile(null);
        return;
      }
      setError(null);
      setFile(selected);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    setAnalysisResult(null);
    setSelectedClause(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch(`${API_BASE_URL}/api/analyze`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({ detail: 'Upload failed' }));
        throw new Error(errData.detail || 'Failed to process document');
      }

      const data: DocumentAnalysisResponse = await res.json();
      setAnalysisResult(data);
      // Automatically select the first high or medium risk clause if available
      const firstRisk = data.clauses.find((c) => c.risk_level === 'high' || c.risk_level === 'medium');
      setSelectedClause(firstRisk || data.clauses[0] || null);
    } catch (err: any) {
      setError(err.message || 'An error occurred during document analysis.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setAnalysisResult(null);
    setSelectedClause(null);
    setError(null);
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Hero Header when no analysis result */}
      {!analysisResult && (
        <div className="text-center max-w-2xl mx-auto space-y-3">
          <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight sm:text-4xl">
            Legal & Insurance Clause Risk Scanner
          </h2>
          <p className="text-base text-slate-600">
            Upload your lease, insurance policy, loan agreement, or Terms of Service to split clauses and highlight risks against a known-pattern library.
          </p>
        </div>
      )}

      {/* Upload Box */}
      {!analysisResult && (
        <UploadSection
          file={file}
          loading={loading}
          error={error}
          onFileChange={handleFileChange}
          onUpload={handleUpload}
        />
      )}

      {/* Full Dashboard Report View (FR-7) */}
      {analysisResult && (
        <div className="space-y-6">
          {/* Top Summary Bar */}
          <SummaryBar
            documentName={analysisResult.document_name}
            totalClauses={analysisResult.total_clauses}
            summary={analysisResult.summary}
            onReset={handleReset}
          />

          {/* 2-Column Document Viewer & Inspector Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            {/* Left 7 Columns: Document Viewer with Color-Coded Highlights */}
            <div className="lg:col-span-7">
              <DocumentViewer
                clauses={analysisResult.clauses}
                selectedClauseId={selectedClause?.clause_id || null}
                onSelectClause={setSelectedClause}
              />
            </div>

            {/* Right 5 Columns: Click-to-Expand Side Panel Inspector */}
            <div className="lg:col-span-5">
              <ClauseDetailCard clause={selectedClause} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
