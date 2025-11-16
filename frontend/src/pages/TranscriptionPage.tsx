import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { transcriptionApi } from '../utils/api';
import type { User, Transcription, DownloadFormat } from '../types';

interface TranscriptionPageProps {
  user: User;
}

export default function TranscriptionPage({ user: _user }: TranscriptionPageProps) {
  const { id } = useParams<{ id: string }>();
  const [transcription, setTranscription] = useState<Transcription | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      loadTranscription(id);
    }
  }, [id]);

  const loadTranscription = async (transcriptionId: string) => {
    try {
      const data = await transcriptionApi.get(transcriptionId);
      setTranscription(data);
    } catch (error) {
      console.error('Failed to load transcription:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (format: DownloadFormat) => {
    if (!id) return;

    try {
      const blob = await transcriptionApi.download(id, format);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `transcription_${id}.${format}`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Failed to download:', error);
    }
  };

  if (loading) {
    return <div className="min-h-screen bg-background flex items-center justify-center">
      <div className="text-primary text-xl">読み込み中...</div>
    </div>;
  }

  if (!transcription) {
    return <div className="min-h-screen bg-background flex items-center justify-center">
      <div className="text-red-600 text-xl">書き起こしが見つかりません</div>
    </div>;
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="bg-white shadow-sm mb-8">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <Link to="/dashboard" className="text-primary hover:underline">
            ← ダッシュボードに戻る
          </Link>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 pb-8">
        {/* プライバシー保護のための自動削除警告 */}
        {transcription.status === 'completed' && transcription.time_until_deletion && (
          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-yellow-700">
                  <strong className="font-bold">プライバシー保護のため、このデータは{transcription.time_until_deletion}で自動削除されます。</strong>
                  <br />
                  必要な場合は今すぐダウンロードしてください。
                </p>
              </div>
            </div>
          </div>
        )}

        <div className="card mb-6">
          <h1 className="text-2xl font-bold mb-4">{transcription.audio_filename}</h1>

          <div className="grid md:grid-cols-2 gap-4 mb-6">
            <div>
              <div className="text-sm text-gray-600">ステータス</div>
              <div className="font-bold">{transcription.status}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">音声長</div>
              <div className="font-bold">
                {transcription.audio_duration ? `${(transcription.audio_duration / 60).toFixed(1)} 分` : '-'}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">処理時間</div>
              <div className="font-bold">
                {transcription.processing_time ? `${transcription.processing_time.toFixed(1)} 秒` : '-'}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">作成日時</div>
              <div className="font-bold">
                {new Date(transcription.created_at).toLocaleString('ja-JP')}
              </div>
            </div>
            {transcription.will_be_deleted_at && (
              <div>
                <div className="text-sm text-gray-600">削除予定日時</div>
                <div className="font-bold text-red-600">
                  {new Date(transcription.will_be_deleted_at).toLocaleString('ja-JP')}
                </div>
              </div>
            )}
          </div>

          {transcription.status === 'completed' && (
            <div className="flex gap-2">
              <button onClick={() => handleDownload('txt')} className="btn-primary">
                TXT ダウンロード
              </button>
              <button onClick={() => handleDownload('json')} className="btn-secondary">
                JSON ダウンロード
              </button>
              <button onClick={() => handleDownload('html')} className="btn-secondary">
                HTML ダウンロード
              </button>
            </div>
          )}
        </div>

        {transcription.full_text && (
          <div className="card">
            <h2 className="text-xl font-bold mb-4">書き起こし結果</h2>
            <div className="bg-gray-50 p-4 rounded-lg whitespace-pre-wrap">
              {transcription.full_text}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
