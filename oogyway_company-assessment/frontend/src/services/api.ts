import axios from 'axios';
import { Session, Message, Artifact, ProviderStatus } from '../types';

const API_BASE = '/api/v1';

export const api = {
  // Health & Provider
  getProviderStatus: async (): Promise<ProviderStatus> => {
    const res = await axios.get(`${API_BASE}/providers/status`);
    return res.data;
  },

  // Sessions
  listSessions: async (): Promise<Session[]> => {
    const res = await axios.get(`${API_BASE}/sessions`);
    return res.data;
  },

  createSession: async (title?: string): Promise<Session> => {
    const res = await axios.post(`${API_BASE}/sessions`, { title });
    return res.data;
  },

  deleteSession: async (sessionId: string): Promise<void> => {
    await axios.delete(`${API_BASE}/sessions/${sessionId}`);
  },

  // Messages
  listMessages: async (sessionId: string): Promise<Message[]> => {
    const res = await axios.get(`${API_BASE}/sessions/${sessionId}/messages`);
    return res.data;
  },

  sendMessage: async (sessionId: string, content: string, skillOverride?: string): Promise<Message> => {
    const res = await axios.post(`${API_BASE}/sessions/${sessionId}/messages`, {
      content,
      skill_override: skillOverride,
    });
    return res.data;
  },

  // Artifacts
  getArtifact: async (artifactId: string): Promise<Artifact> => {
    const res = await axios.get(`${API_BASE}/artifacts/${artifactId}`);
    return res.data;
  },

  listSessionArtifacts: async (sessionId: string): Promise<Artifact[]> => {
    const res = await axios.get(`${API_BASE}/sessions/${sessionId}/artifacts`);
    return res.data;
  }
};
