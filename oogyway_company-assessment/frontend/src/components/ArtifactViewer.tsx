import React, { useState } from 'react';
import { X, Code, Eye, Copy, Check, FileText, ShieldCheck } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Artifact } from '../types';

interface ArtifactViewerProps {
  artifact: Artifact | null;
  onClose: () => void;
}

export const ArtifactViewer: React.FC<ArtifactViewerProps> = ({ artifact, onClose }) => {
  const [activeTab, setActiveTab] = useState<'preview' | 'source'>('preview');
  const [copied, setCopied] = useState(false);

  if (!artifact) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(artifact.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="w-[450px] lg:w-[550px] bg-[#0d1322] border-l border-slate-800 flex flex-col h-full shadow-2xl z-20">
      {/* Top Bar */}
      <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/60">
        <div className="flex items-center space-x-2.5 min-w-0 pr-4">
          <div className="p-2 rounded-lg bg-sky-950 text-sky-400 border border-sky-800/50">
            <FileText className="w-4 h-4" />
          </div>
          <div className="min-w-0">
            <h2 className="font-bold text-slate-100 text-sm truncate">{artifact.title}</h2>
            <div className="flex items-center space-x-2 text-[10px] text-slate-400">
              <span className="uppercase px-1.5 py-0.5 rounded bg-slate-800 text-sky-300 font-mono">
                {artifact.artifact_type}
              </span>
              <span className="flex items-center text-emerald-400">
                <ShieldCheck className="w-3 h-3 mr-1" />
                Sandboxed & Sanitized
              </span>
            </div>
          </div>
        </div>

        <button
          onClick={onClose}
          className="p-1.5 text-slate-400 hover:text-slate-200 rounded-lg hover:bg-slate-800 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Mode Controls Bar */}
      <div className="px-4 py-2 bg-slate-950/80 border-b border-slate-800/80 flex items-center justify-between text-xs">
        <div className="flex bg-slate-900 p-1 rounded-lg border border-slate-800">
          <button
            onClick={() => setActiveTab('preview')}
            className={`flex items-center space-x-1.5 px-3 py-1 rounded-md text-xs font-medium transition-all ${
              activeTab === 'preview'
                ? 'bg-sky-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Eye className="w-3.5 h-3.5" />
            <span>Preview</span>
          </button>

          <button
            onClick={() => setActiveTab('source')}
            className={`flex items-center space-x-1.5 px-3 py-1 rounded-md text-xs font-medium transition-all ${
              activeTab === 'source'
                ? 'bg-sky-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Code className="w-3.5 h-3.5" />
            <span>Source Code</span>
          </button>
        </div>

        <button
          onClick={handleCopy}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition-colors border border-slate-700/50"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
          <span>{copied ? 'Copied!' : 'Copy Code'}</span>
        </button>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-auto p-4 bg-[#090d16]">
        {activeTab === 'preview' ? (
          artifact.artifact_type === 'html' ? (
            /* Sandboxed HTML Render using iframe */
            <div className="w-full h-full min-h-[500px] bg-white rounded-xl overflow-hidden border border-slate-700 shadow-inner">
              <iframe
                title={artifact.title}
                srcDoc={artifact.sanitized_content}
                sandbox="allow-same-origin"
                className="w-full h-full border-0"
              />
            </div>
          ) : (
            /* Markdown Artifact Render */
            <div className="prose prose-invert max-w-none text-slate-200 text-sm leading-relaxed space-y-3">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {artifact.content}
              </ReactMarkdown>
            </div>
          )
        ) : (
          /* Raw Source Code View */
          <pre className="p-4 rounded-xl bg-slate-950 text-sky-300 font-mono text-xs overflow-x-auto border border-slate-800 whitespace-pre-wrap">
            {artifact.content}
          </pre>
        )}
      </div>
    </div>
  );
};
