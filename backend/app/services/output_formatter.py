"""
出力フォーマットサービス

書き起こし結果を各種形式（TXT, JSON, HTML）で出力
セッションログとのミックス出力も対応
"""
import json
import logging
from typing import List, Optional
from datetime import datetime, timedelta

from ..models.transcription import TranscriptSegment

logger = logging.getLogger(__name__)


class OutputFormatter:
    """出力フォーマッター"""

    def generate_txt(
        self,
        segments: List[TranscriptSegment],
        session_log: Optional[str] = None,
        include_timestamps: bool = True
    ) -> str:
        """
        TXT形式で出力

        Args:
            segments: 書き起こしセグメント
            session_log: セッションログ
            include_timestamps: タイムスタンプを含めるか

        Returns:
            TXT形式の文字列
        """
        lines = []

        # セッションログがある場合は先頭に追加
        if session_log:
            lines.append("=" * 80)
            lines.append("セッション情報")
            lines.append("=" * 80)
            lines.append(session_log)
            lines.append("")
            lines.append("=" * 80)
            lines.append("書き起こし結果")
            lines.append("=" * 80)
            lines.append("")

        # 書き起こしセグメント
        for segment in segments:
            if include_timestamps:
                timestamp = self._format_timestamp(segment.start)
                lines.append(f"[{timestamp}] {segment.text}")
            else:
                lines.append(segment.text)

        return "\n".join(lines)

    def generate_json(
        self,
        segments: List[TranscriptSegment],
        session_log: Optional[str] = None,
        audio_filename: Optional[str] = None,
        created_at: Optional[datetime] = None
    ) -> str:
        """
        JSON形式で出力

        Args:
            segments: 書き起こしセグメント
            session_log: セッションログ
            audio_filename: 音声ファイル名
            created_at: 作成日時

        Returns:
            JSON形式の文字列
        """
        data = {
            "metadata": {
                "audio_filename": audio_filename,
                "created_at": created_at.isoformat() if created_at else None,
                "session_log": session_log,
                "total_segments": len(segments),
                "total_duration": segments[-1].end if segments else 0
            },
            "segments": [
                {
                    "start": segment.start,
                    "end": segment.end,
                    "duration": segment.end - segment.start,
                    "text": segment.text,
                    "confidence": segment.confidence
                }
                for segment in segments
            ]
        }

        return json.dumps(data, ensure_ascii=False, indent=2)

    def generate_html(
        self,
        segments: List[TranscriptSegment],
        session_log: Optional[str] = None,
        audio_filename: Optional[str] = None,
        created_at: Optional[datetime] = None
    ) -> str:
        """
        HTML形式で出力

        Args:
            segments: 書き起こしセグメント
            session_log: セッションログ
            audio_filename: 音声ファイル名
            created_at: 作成日時

        Returns:
            HTML形式の文字列
        """
        html_parts = []

        # HTMLヘッダー
        html_parts.append("""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>書き起こし結果 - otomochi</title>
    <style>
        body {
            font-family: 'Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Noto Sans JP', sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #FFF4E9;
            color: #333;
        }
        .header {
            background-color: #de8f7d;
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .header h1 {
            margin: 0 0 10px 0;
        }
        .metadata {
            font-size: 0.9em;
            opacity: 0.9;
        }
        .session-log {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #de8f7d;
        }
        .session-log h2 {
            margin-top: 0;
            color: #de8f7d;
        }
        .transcript {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
        }
        .segment {
            margin-bottom: 15px;
            padding: 10px;
            border-bottom: 1px solid #eee;
        }
        .segment:last-child {
            border-bottom: none;
        }
        .timestamp {
            color: #de8f7d;
            font-weight: bold;
            font-size: 0.9em;
            margin-right: 10px;
        }
        .text {
            line-height: 1.6;
        }
        .confidence {
            color: #999;
            font-size: 0.8em;
            margin-left: 10px;
        }
    </style>
</head>
<body>
""")

        # ヘッダー
        html_parts.append('    <div class="header">')
        html_parts.append('        <h1>📝 TRPG セッション書き起こし</h1>')
        html_parts.append('        <div class="metadata">')
        if audio_filename:
            html_parts.append(f'            <p>音声ファイル: {audio_filename}</p>')
        if created_at:
            html_parts.append(f'            <p>作成日時: {created_at.strftime("%Y年%m月%d日 %H:%M")}</p>')
        html_parts.append('        </div>')
        html_parts.append('    </div>')

        # セッションログ
        if session_log:
            html_parts.append('    <div class="session-log">')
            html_parts.append('        <h2>📋 セッション情報</h2>')
            html_parts.append(f'        <p>{self._escape_html(session_log)}</p>')
            html_parts.append('    </div>')

        # 書き起こし結果
        html_parts.append('    <div class="transcript">')
        html_parts.append('        <h2>💬 書き起こし結果</h2>')

        for segment in segments:
            timestamp = self._format_timestamp(segment.start)
            html_parts.append('        <div class="segment">')
            html_parts.append(f'            <span class="timestamp">[{timestamp}]</span>')
            html_parts.append(f'            <span class="text">{self._escape_html(segment.text)}</span>')
            html_parts.append('        </div>')

        html_parts.append('    </div>')

        # HTMLフッター
        html_parts.append('</body>')
        html_parts.append('</html>')

        return '\n'.join(html_parts)

    def generate_mixed_output(
        self,
        segments: List[TranscriptSegment],
        session_log: Optional[str] = None
    ) -> str:
        """
        ミックス出力を生成（セッションログ + 書き起こし結果）

        Args:
            segments: 書き起こしセグメント
            session_log: セッションログ

        Returns:
            ミックス出力文字列
        """
        return self.generate_txt(segments, session_log, include_timestamps=True)

    def _format_timestamp(self, seconds: float) -> str:
        """
        秒数をタイムスタンプ形式に変換 (HH:MM:SS)

        Args:
            seconds: 秒数

        Returns:
            タイムスタンプ文字列
        """
        td = timedelta(seconds=seconds)
        hours = td.seconds // 3600
        minutes = (td.seconds % 3600) // 60
        secs = td.seconds % 60

        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def _escape_html(self, text: str) -> str:
        """
        HTMLエスケープ

        Args:
            text: エスケープするテキスト

        Returns:
            エスケープ済みテキスト
        """
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;')
                .replace('\n', '<br>'))


# シングルトンインスタンス
output_formatter = OutputFormatter()
