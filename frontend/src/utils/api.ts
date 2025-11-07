/**
 * API クライアント
 */
import axios, { AxiosError } from 'axios';
import type { Transcription, TranscriptionListResponse, User, DownloadFormat } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

// Axios インスタンス
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// リクエストインターセプター（認証トークン付与）
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// レスポンスインターセプター（エラーハンドリング）
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // 認証エラー時はログアウト
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// 認証
export const authApi = {
  login: async (email: string, password: string) => {
    const response = await apiClient.post('/auth/login', { email, password });
    return response.data;
  },

  signup: async (email: string, password: string) => {
    const response = await apiClient.post('/auth/signup', { email, password });
    return response.data;
  },

  oauthLogin: async (provider: 'google' | 'twitter') => {
    const response = await apiClient.post('/auth/oauth', { provider });
    return response.data;
  },

  logout: async () => {
    await apiClient.post('/auth/logout');
    localStorage.removeItem('access_token');
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },
};

// 書き起こし
export const transcriptionApi = {
  create: async (audioFile: File, sessionLog?: string): Promise<Transcription> => {
    const formData = new FormData();
    formData.append('audio_file', audioFile);
    if (sessionLog) {
      formData.append('session_log', sessionLog);
    }

    const response = await apiClient.post('/transcriptions', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  list: async (page = 1, pageSize = 10): Promise<TranscriptionListResponse> => {
    const response = await apiClient.get('/transcriptions', {
      params: { page, page_size: pageSize },
    });
    return response.data;
  },

  get: async (id: string): Promise<Transcription> => {
    const response = await apiClient.get(`/transcriptions/${id}`);
    return response.data;
  },

  download: async (id: string, format: DownloadFormat): Promise<Blob> => {
    const response = await apiClient.get(`/transcriptions/${id}/download`, {
      params: { format },
      responseType: 'blob',
    });
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/transcriptions/${id}`);
  },
};

// ユーザー
export const userApi = {
  getProfile: async (): Promise<User> => {
    const response = await apiClient.get('/users/me');
    return response.data;
  },

  updateProfile: async (displayName: string): Promise<User> => {
    const response = await apiClient.patch('/users/me', {
      display_name: displayName,
    });
    return response.data;
  },

  getUsage: async () => {
    const response = await apiClient.get('/users/me/usage');
    return response.data;
  },

  updatePlan: async (planType: string, autoRenew = true): Promise<User> => {
    const response = await apiClient.post('/users/me/plan', {
      plan_type: planType,
      auto_renew: autoRenew,
    });
    return response.data;
  },
};

// 課金・決済
export const billingApi = {
  createCheckout: async (planType: string) => {
    const response = await apiClient.post('/billing/checkout', {
      plan_type: planType,
    });
    return response.data;
  },

  createPortalSession: async () => {
    const response = await apiClient.post('/billing/portal');
    return response.data;
  },

  createOneshotPayment: async (hours: number) => {
    const response = await apiClient.post('/billing/oneshot', null, {
      params: { hours },
    });
    return response.data;
  },

  cancelSubscription: async (subscriptionId: string, atPeriodEnd = true) => {
    const response = await apiClient.post('/billing/cancel-subscription', null, {
      params: { subscription_id: subscriptionId, at_period_end: atPeriodEnd },
    });
    return response.data;
  },

  getConfig: async () => {
    const response = await apiClient.get('/billing/config');
    return response.data;
  },
};

export default apiClient;
