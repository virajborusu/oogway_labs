import React from 'react';
import { User, Bot, FileText, Sparkles, AlertCircle } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Message, Artifact } from '../types';
import { SourceCitations } from './SourceCitations';

interface MessageListProps {
  messages: Message[];
  loading: boolean;
  onOpenArtifact: (artifactId: string) => void;
  activeArtifact: Artifact | null;
}

export const MessageList: React.FC<MessageListProps> = ({
  messages,
  loading,
  onOpenArtifact,
  activeArtifact,
}) => {
  if (messages.length === 0 && !loading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-8 text-center select-none">
        <div className="p-4 rounded-2xl bg-gradient-to-tr from-sky-600/20 to-indigo-600/20 border border-sky-500/30 mb-4">
          <Sparkles className="w-10 h-10 text-sky-400" />
        </div>
        <h2 className="text-xl font-bold text-slate-100 mb-2">The Lenny Growth Assistant</h2>
        <p className="text-sm text-slate-400 max-w-md leading-relaxed mb-6">
          Grounded product strategy, PLG insights, and Ship 30 for 30 essay generation trained on Lenny's Podcast transcripts.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-xl text-left text-xs">
          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-slate-300">
            <span className="font-semibold text-sky-400 block mb-1">Grounded Q&A</span>
            "What is Casey Winters' mental model for product-market fit?"
          </div>
          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-slate-300">
            <span className="font-semibold text-indigo-400 block mb-1">Ship 30 for 30 Skill</span>
            "Write a Ship 30 for 30 essay on Brian Chesky's 11-star experience design."
          </div>
          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-slate-300">
            <span className="font-semibold text-emerald-400 block mb-1">Artifact Generator</span>
            "Create a product strategy one-pager artifact for PLG sales conversion."
          </div>
          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-slate-300">
            <span className="font-semibold text-amber-400 block mb-1">Out-of-Domain Guardrail</span>
            "What is the recipe for chocolate cake?" (Returns grounded refusal)
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
      {messages.map((msg) => {
        const isUser = msg.role === 'user';
        const hasArtifact = !!msg.artifact_id;

        return (
          <div
            key={msg.id}
            className={`flex items-start space-x-3 max-w-4xl mx-auto ${
              isUser ? 'flex-row-reverse space-x-reverse' : ''
            }`}
          >
            {/* Avatar */}
            <div
              className={`p-2 rounded-xl shrink-0 ${
                isUser
                  ? 'bg-sky-600 text-white shadow-md shadow-sky-600/20'
                  : 'bg-slate-800 text-sky-400 border border-slate-700'
              }`}
            >
              {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>

            {/* Bubble Container */}
            <div
              className={`flex-1 rounded-2xl p-4 text-sm leading-relaxed border ${
                isUser
                  ? 'bg-sky-950/60 text-slate-100 border-sky-800/40 rounded-tr-none'
                  : 'bg-slate-900/80 text-slate-200 border-slate-800/80 rounded-tl-none shadow-lg'
              }`}
            >
              {/* Message Header */}
              <div className="flex items-center justify-between mb-2 text-[11px] text-slate-400">
                <span className="font-semibold">{isUser ? 'You' : 'Lenny Growth Assistant'}</span>
                {msg.meta_info?.provider && (
                  <span className="font-mono text-[10px] text-sky-400/80 bg-slate-950 px-2 py-0.5 rounded">
                    {msg.meta_info.provider}:{msg.meta_info.model}
                  </span>
                )}
              </div>

              {/* Message Body */}
              <div className="prose prose-invert max-w-none text-slate-200 text-sm space-y-2">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
              </div>

              {/* Artifact Button Trigger */}
              {hasArtifact && (
                <div className="mt-3 pt-3 border-t border-slate-800">
                  <button
                    onClick={() => onOpenArtifact(msg.artifact_id!)}
                    className="flex items-center space-x-2 px-3.5 py-2 rounded-xl bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-500 hover:to-indigo-500 text-white font-medium text-xs transition-all shadow-md active:scale-95"
                  >
                    <FileText className="w-4 h-4" />
                    <span>
                      {activeArtifact?.id === msg.artifact_id
                        ? 'Viewing Artifact in Side Panel'
                        : 'Open Generated Artifact Viewer'}
                    </span>
                  </button>
                </div>
              )}

              {/* Grounded Source Citations */}
              {!isUser && msg.sources && <SourceCitations sources={msg.sources} />}
            </div>
          </div>
        );
      })}

      {/* Loading Indicator */}
      {loading && (
        <div className="flex items-start space-x-3 max-w-4xl mx-auto">
          <div className="p-2 rounded-xl bg-slate-800 text-sky-400 border border-slate-700">
            <Bot className="w-4 h-4" />
          </div>
          <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 text-xs text-sky-400 flex items-center space-x-2">
            <div className="w-2 h-2 rounded-full bg-sky-400 animate-ping" />
            <span>Searching transcripts & generating grounded response...</span>
          </div>
        </div>
      )}
    </div>
  );
};
