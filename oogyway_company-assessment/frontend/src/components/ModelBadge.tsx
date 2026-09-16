import React from 'react';
import { Cpu, CheckCircle2, AlertTriangle } from 'lucide-react';
import { ProviderStatus } from '../types';

interface ModelBadgeProps {
  status: ProviderStatus | null;
}

export const ModelBadge: React.FC<ModelBadgeProps> = ({ status }) => {
  if (!status) {
    return (
      <div className="flex items-center space-x-2 px-3 py-1.5 rounded-full bg-gray-800/80 text-gray-400 text-xs border border-gray-700/50">
        <Cpu className="w-3.5 h-3.5 animate-spin" />
        <span>Connecting provider...</span>
      </div>
    );
  }

  const isLocal = status.provider.toLowerCase() === 'ollama';

  return (
    <div className="flex items-center space-x-2 px-3 py-1.5 rounded-full bg-slate-900/90 text-xs border border-slate-700/60 shadow-sm">
      <div className="flex items-center space-x-1.5">
        {status.is_available ? (
          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
        ) : (
          <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
        )}
        <span className="font-semibold text-slate-200 uppercase tracking-wider text-[10px]">
          {status.provider}
        </span>
      </div>
      <span className="text-slate-500">|</span>
      <span className="text-sky-300 font-mono text-[11px]">{status.model}</span>
      <span className="px-1.5 py-0.5 rounded bg-sky-950 text-sky-400 text-[9px] font-medium uppercase">
        {isLocal ? 'Local Ollama' : 'Cloud'}
      </span>
    </div>
  );
};
