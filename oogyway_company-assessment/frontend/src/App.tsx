import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { MessageList } from './components/MessageList';
import { MessageInput } from './components/MessageInput';
import { ArtifactViewer } from './components/ArtifactViewer';
import { api } from './services/api';
import { Session, Message, Artifact, ProviderStatus } from './types';

export const App: React.FC = () => {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [activeArtifact, setActiveArtifact] = useState<Artifact | null>(null);
  const [providerStatus, setProviderStatus] = useState<ProviderStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Load sessions and status on mount
  useEffect(() => {
    fetchInitialData();
  }, []);

  const fetchInitialData = async () => {
    try {
      const [status, sessionList] = await Promise.all([
        api.getProviderStatus(),
        api.listSessions(),
      ]);
      setProviderStatus(status);
      setSessions(sessionList);

      if (sessionList.length > 0) {
        setActiveSessionId(sessionList[0].id);
        loadSessionMessages(sessionList[0].id);
      } else {
        createNewSession();
      }
    } catch (err: any) {
      setErrorMsg('Failed to connect to backend server. Make sure FastAPI server is running on port 8000.');
    }
  };

  const loadSessionMessages = async (sessionId: string) => {
    try {
      const msgs = await api.listMessages(sessionId);
      setMessages(msgs);
      setActiveArtifact(null);
    } catch (err: any) {
      setErrorMsg('Failed to load session messages.');
    }
  };

  const createNewSession = async () => {
    try {
      const newSession = await api.createSession('New Growth Conversation');
      setSessions((prev) => [newSession, ...prev]);
      setActiveSessionId(newSession.id);
      setMessages([]);
      setActiveArtifact(null);
    } catch (err: any) {
      setErrorMsg('Failed to create new chat session.');
    }
  };

  const handleSelectSession = (id: string) => {
    setActiveSessionId(id);
    loadSessionMessages(id);
  };

  const handleDeleteSession = async (id: string) => {
    try {
      await api.deleteSession(id);
      const updated = sessions.filter((s) => s.id !== id);
      setSessions(updated);
      if (activeSessionId === id) {
        if (updated.length > 0) {
          setActiveSessionId(updated[0].id);
          loadSessionMessages(updated[0].id);
        } else {
          createNewSession();
        }
      }
    } catch (err: any) {
      setErrorMsg('Failed to delete session.');
    }
  };

  const handleSendMessage = async (content: string, skillOverride?: string) => {
    if (!activeSessionId) return;

    setLoading(true);
    setErrorMsg(null);

    // Optimistic User Message
    const tempUserMsg: Message = {
      id: `temp-${Date.now()}`,
      session_id: activeSessionId,
      role: 'user',
      content,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, tempUserMsg]);

    try {
      const assistantMsg = await api.sendMessage(activeSessionId, content, skillOverride);
      setMessages((prev) => [...prev.filter((m) => m.id !== tempUserMsg.id), tempUserMsg, assistantMsg]);

      // If message generated an artifact, automatically load and open Artifact Viewer
      if (assistantMsg.artifact_id) {
        handleOpenArtifact(assistantMsg.artifact_id);
      }

      // Refresh session list to update titles
      const updatedSessions = await api.listSessions();
      setSessions(updatedSessions);
    } catch (err: any) {
      const errorText =
        err.response?.data?.error?.message ||
        'Error sending message. Check LLM provider and backend status.';
      setErrorMsg(errorText);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenArtifact = async (artifactId: string) => {
    try {
      const art = await api.getArtifact(artifactId);
      setActiveArtifact(art);
    } catch (err) {
      setErrorMsg('Failed to load artifact.');
    }
  };

  const activeSession = sessions.find((s) => s.id === activeSessionId);

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#0b0f19]">
      {/* Sidebar */}
      <Sidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        onSelectSession={handleSelectSession}
        onNewChat={createNewSession}
        onDeleteSession={handleDeleteSession}
      />

      {/* Main Container */}
      <div className="flex-1 flex flex-col h-full overflow-hidden relative">
        <Header providerStatus={providerStatus} activeSessionTitle={activeSession?.title} />

        {/* Global Error Banner */}
        {errorMsg && (
          <div className="bg-rose-950/80 border-b border-rose-800 text-rose-200 px-4 py-2 text-xs flex items-center justify-between">
            <span>⚠️ {errorMsg}</span>
            <button
              onClick={() => setErrorMsg(null)}
              className="text-rose-400 hover:text-rose-100 font-bold ml-2"
            >
              ✕
            </button>
          </div>
        )}

        <MessageList
          messages={messages}
          loading={loading}
          onOpenArtifact={handleOpenArtifact}
          activeArtifact={activeArtifact}
        />

        <MessageInput onSendMessage={handleSendMessage} loading={loading} />
      </div>

      {/* Slide-over Artifact Viewer */}
      <ArtifactViewer artifact={activeArtifact} onClose={() => setActiveArtifact(null)} />
    </div>
  );
};

export default App;
