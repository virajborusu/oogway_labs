import React, { useState, useRef, useEffect } from 'react';
import { Send, Feather, FileCode, CornerDownLeft } from 'lucide-react';

interface MessageInputProps {
  onSendMessage: (text: string, skillOverride?: string) => void;
  loading: boolean;
}

export const MessageInput: React.FC<MessageInputProps> = ({ onSendMessage, loading }) => {
  const [text, setText] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`;
    }
  }, [text]);

  const handleSubmit = (override?: string) => {
    if (!text.trim() || loading) return;
    onSendMessage(text.trim(), override);
    setText('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleChipClick = (prompt: string, override?: string) => {
    setText(prompt);
    if (textareaRef.current) {
      textareaRef.current.focus();
    }
  };

  return (
    <div className="p-4 bg-[#0d1322] border-t border-slate-800/80">
      <div className="max-w-4xl mx-auto space-y-2.5">
        {/* Quick Suggestion Skill Chips */}
        <div className="flex items-center space-x-2 overflow-x-auto pb-1 text-xs select-none">
          <button
            onClick={() =>
              handleChipClick(
                'Write a Ship 30 for 30 essay on Brian Chesky\'s 11-star experience design.',
                'ship_30_for_30'
              )
            }
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-indigo-950/60 hover:bg-indigo-900/60 text-indigo-300 border border-indigo-800/50 shrink-0 transition-colors"
          >
            <Feather className="w-3.5 h-3.5" />
            <span>Ship 30 for 30 Skill</span>
          </button>

          <button
            onClick={() =>
              handleChipClick(
                'Create a Product Strategy One-Pager artifact for freemium conversion.',
                'artifact'
              )
            }
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-emerald-950/60 hover:bg-emerald-900/60 text-emerald-300 border border-emerald-800/50 shrink-0 transition-colors"
          >
            <FileCode className="w-3.5 h-3.5" />
            <span>Artifact Generator</span>
          </button>

          <button
            onClick={() =>
              handleChipClick('What is Casey Winters\' definition of product-market fit and retention?')
            }
            className="px-3 py-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 text-slate-300 border border-slate-700/50 shrink-0 transition-colors"
          >
            Casey Winters PMF
          </button>

          <button
            onClick={() =>
              handleChipClick('How does Elena Verna recommend setting up product-led sales?')
            }
            className="px-3 py-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 text-slate-300 border border-slate-700/50 shrink-0 transition-colors"
          >
            Elena Verna PLG
          </button>
        </div>

        {/* Text Area & Submit Controls */}
        <div className="relative flex items-end rounded-2xl bg-slate-900 border border-slate-700/80 focus-within:border-sky-500/80 focus-within:ring-1 focus-within:ring-sky-500/80 transition-all p-2 shadow-inner">
          <textarea
            ref={textareaRef}
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a growth question, request a 30 for 30 essay, or generate an artifact..."
            rows={1}
            disabled={loading}
            className="flex-1 bg-transparent border-0 text-slate-100 placeholder-slate-500 text-sm focus:outline-none resize-none px-3 py-2 min-h-[44px]"
          />

          <div className="flex items-center space-x-2 pb-1 pr-1">
            <span className="hidden sm:inline text-[10px] text-slate-500 flex items-center">
              <span>Press Enter</span>
              <CornerDownLeft className="w-3 h-3 ml-1" />
            </span>

            <button
              onClick={() => handleSubmit()}
              disabled={!text.trim() || loading}
              className="p-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 disabled:opacity-40 disabled:hover:bg-sky-600 text-white transition-all shadow-md shadow-sky-600/30 active:scale-95"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
