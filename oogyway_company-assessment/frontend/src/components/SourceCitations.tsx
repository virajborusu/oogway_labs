import React, { useState } from 'react';
import { BookOpen, ChevronDown, ExternalLink, User } from 'lucide-react';
import { SourceItem } from '../types';

interface SourceCitationsProps {
  sources: SourceItem[];
}

export const SourceCitations: React.FC<SourceCitationsProps> = ({ sources }) => {
  const [isOpen, setIsOpen] = useState(false);

  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-3 pt-3 border-t border-slate-800/80">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 text-xs font-semibold text-sky-400 hover:text-sky-300 transition-colors"
      >
        <BookOpen className="w-3.5 h-3.5" />
        <span>Grounded Transcript Sources ({sources.length})</span>
        <ChevronDown className={`w-3.5 h-3.5 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="mt-2 space-y-2">
          {sources.map((src, idx) => (
            <div
              key={idx}
              className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 text-xs space-y-1.5"
            >
              <div className="flex items-center justify-between">
                <span className="font-semibold text-slate-200">{src.title}</span>
                {src.episode_url && (
                  <a
                    href={src.episode_url}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center space-x-1 text-[11px] text-sky-400 hover:underline"
                  >
                    <span>View Transcript</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </div>
              <div className="flex items-center space-x-2 text-[11px] text-slate-400">
                <User className="w-3 h-3 text-slate-500" />
                <span>Guest: {src.speaker || 'Podcast Guest'}</span>
                {src.relevance_score && (
                  <span className="ml-auto text-emerald-400 font-mono text-[10px]">
                    {(src.relevance_score * 100).toFixed(0)}% match
                  </span>
                )}
              </div>
              <p className="text-[11px] text-slate-300 italic bg-slate-950/60 p-2 rounded border border-slate-800/50">
                "{src.snippet}"
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
