import React from 'react';
import { ModelBadge } from './ModelBadge';
import { ProviderStatus } from '../types';

interface HeaderProps {
  providerStatus: ProviderStatus | null;
  activeSessionTitle?: string;
}

export const Header: React.FC<HeaderProps> = ({ providerStatus, activeSessionTitle }) => {
  return (
    <header className="h-16 px-6 bg-[#0d1322] border-b border-slate-800/80 flex items-center justify-between z-10">
      <div className="flex items-center space-x-3">
        <h2 className="font-bold text-slate-100 text-sm md:text-base tracking-tight truncate max-w-md">
          {activeSessionTitle || 'The Lenny Growth Assistant'}
        </h2>
      </div>

      <div className="flex items-center space-x-4">
        <ModelBadge status={providerStatus} />
      </div>
    </header>
  );
};
