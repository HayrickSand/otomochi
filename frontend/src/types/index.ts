/**
 * 型定義ファイル
 */

// ユーザー
export type PlanType = 'free' | 'lite' | 'standard' | 'unlimited';

export interface UserPlan {
  plan_type: PlanType;
  sessions_limit: number;
  hours_limit: number;
  sessions_used: number;
  hours_used: number;
  billing_cycle_start: string;
  billing_cycle_end: string;
  auto_renew: boolean;
}

export interface User {
  id: string;
  email: string;
  display_name?: string;
  avatar_url?: string;
  plan: UserPlan;
  is_admin: boolean;
}

// 書き起こし
export type TranscriptionStatus = 'pending' | 'processing' | 'completed' | 'failed' | 'cancelled';

export interface TranscriptSegment {
  start: number;
  end: number;
  text: string;
  confidence?: number;
}

export interface Transcription {
  id: string;
  status: TranscriptionStatus;
  audio_filename: string;
  audio_duration?: number;
  audio_size: number;
  full_text?: string;
  segments: TranscriptSegment[];
  session_log?: string;
  mixed_output?: string;
  processing_time?: number;
  error_message?: string;
  created_at: string;
  completed_at?: string;
}

export interface TranscriptionListResponse {
  transcriptions: Transcription[];
  total: number;
  page: number;
  page_size: number;
}

export type DownloadFormat = 'txt' | 'json' | 'html';

// API レスポンス
export interface ApiError {
  detail: string;
  error?: string;
}
