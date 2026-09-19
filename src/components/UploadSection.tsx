import React from 'react';
import { UploadCloud, FileText, AlertCircle, Loader2 } from 'lucide-react';

interface UploadSectionProps {
  file: File | null;
  loading: boolean;
  error: string | null;
  onFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onUpload: () => void;
}

export default function UploadSection({
  file,
  loading,
  error,
  onFileChange,
  onUpload,
}: UploadSectionProps) {
  return (
    <div className="max-w-xl mx-auto bg-white p-8 rounded-3xl shadow-sm border border-slate-200">
      <div className="border-2 border-dashed border-slate-300 hover:border-blue-500 transition-colors rounded-2xl p-10 text-center cursor-pointer bg-slate-50/50">
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={onFileChange}
          className="hidden"
          id="file-upload-input"
        />
        <label htmlFor="file-upload-input" className="cursor-pointer block">
          <div className="w-16 h-16 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-blue-100 shadow-sm">
            <UploadCloud className="w-8 h-8" />
          </div>
          <span className="text-slate-900 font-bold block text-lg mb-1">
            {file ? file.name : 'Select or drag PDF / DOCX file'}
          </span>
          <span className="text-xs text-slate-500 block">
            Supported formats: <strong>.pdf</strong>, <strong>.docx</strong> (Max 15MB / 50 pages)
          </span>
        </label>
      </div>

      {error && (
        <div className="mt-4 p-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-xl flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0 text-red-600" />
          <span>{error}</span>
        </div>
      )}

      <div className="mt-6 flex justify-end">
        <button
          onClick={onUpload}
          disabled={!file || loading}
          className="w-full sm:w-auto px-8 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-semibold rounded-xl shadow-sm transition-all flex items-center justify-center gap-2 text-sm"
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Scanning clauses against risk patterns...</span>
            </>
          ) : (
            <>
              <FileText className="w-4 h-4" />
              <span>Analyze Document</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}
