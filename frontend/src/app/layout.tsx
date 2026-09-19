import './globals.css';
import React from 'react';
import { Shield, AlertTriangle } from 'lucide-react';

export const metadata = {
  title: 'ClauseGuard — Legal & Insurance Clause Risk Flagger',
  description: 'Upload legal/insurance documents to receive clause-by-clause risk awareness reports.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col bg-slate-50 text-slate-900">
        {/* Top Disclaimer Banner - Section 8 & FR-7 Persistent Requirement */}
        <div className="bg-amber-500/10 border-b border-amber-500/20 px-4 py-2 text-xs md:text-sm text-amber-900 flex items-center justify-center gap-2 font-medium">
          <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
          <span>
            <strong>Disclaimer:</strong> ClauseGuard flags patterns for awareness. This is not legal advice — consult a professional for decisions with real consequences.
          </span>
        </div>

        {/* Main Header */}
        <header className="border-b border-slate-200 bg-white sticky top-0 z-10 shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-600 rounded-lg text-white">
                <Shield className="w-6 h-6" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-slate-900 leading-none">ClauseGuard</h1>
                <p className="text-xs text-slate-500 mt-0.5">Legal & Insurance Risk Scanner</p>
              </div>
            </div>
            <span className="text-xs font-semibold uppercase tracking-wider bg-slate-100 text-slate-600 px-2.5 py-1 rounded-full border border-slate-200">
              Hackathon v1.0
            </span>
          </div>
        </header>

        {/* Content */}
        <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
          {children}
        </main>
      </body>
    </html>
  );
}
