import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { transcriptionApi } from '../utils/api';
import type { User, Transcription, DownloadFormat } from '../types';

interface TranscriptionPageProps {
  user: User;
}

export default function TranscriptionPage({ user }: TranscriptionPageProps) {
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
