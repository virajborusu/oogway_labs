export interface SourceItem {
  title: str;
  source: string;
  speaker?: string;
  episode_url?: string;
  snippet: string;
  relevance_score?: number;
}

export interface Message {
  id: string;
  session_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  sources?: SourceItem[];
  created_at: string;
  artifact_id?: string;
  meta_info?: Record<string, any>;
}

export interface Session {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count?: number;
}

export interface Artifact {
  id: string;
  session_id: string;
  message_id?: string;
  title: string;
  artifact_type: 'markdown' | 'html';
  content: string;
  sanitized_content: string;
  created_at: string;
}

export interface ProviderStatus {
  provider: string;
  model: string;
  is_available: boolean;
  status_message: string;
  available_providers: string[];
  ollama_health?: Record<string, any>;
}
