"""
Faster-Whisper 音声認識サービス

large-v3-turbo モデルを使用した高速・高精度な日本語書き起こし
"""
import logging
from typing import List, Optional
from faster_whisper import WhisperModel
import subprocess

from ..core.config import settings
from ..models.transcription import TranscriptSegment

logger = logging.getLogger(__name__)


class WhisperService:
    """Whisper 音声認識サービス"""

    def __init__(self):
        """
        Whisper モデルを初期化

        GPU(CUDA) での実行を前提とし、float16 精度で高速化
        """
        self.model = None
        self.device = settings.WHISPER_DEVICE
        self.compute_type = settings.WHISPER_COMPUTE_TYPE

        # CUDA 利用可能性チェック
        if self.device == "cuda" and not self._is_cuda_available():
            logger.warning("CUDA is not available, falling back to CPU")
            self.device = "cpu"
            self.compute_type = "int8"

        logger.info(
            f"Initializing Whisper model: {settings.WHISPER_MODEL} "
            f"on {self.device} with {self.compute_type}"
        )

    def load_model(self):
        """モデルをロード（遅延初期化）"""
        if self.model is None:
            self.model = WhisperModel(
                settings.WHISPER_MODEL,
                device=self.device,
                compute_type=self.compute_type,
                download_root=None,  # デフォルトのキャッシュディレクトリを使用
            )
            logger.info("Whisper model loaded successfully")

    def transcribe(
        self,
        audio_path: str,
        language: str = "ja",
        task: str = "transcribe",
        initial_prompt: Optional[str] = None
    ) -> tuple[List[TranscriptSegment], str]:
        """
        音声ファイルを書き起こし

        Args:
            audio_path: 音声ファイルパス
            language: 言語コード（デフォルト: ja）
            task: タスク（transcribe または translate）
            initial_prompt: 初期プロンプト（TRPG用語辞書など）

        Returns:
            (セグメントリスト, 全文テキスト)
        """
        self.load_model()

        # TRPG用語を含む初期プロンプト
        if initial_prompt is None:
            initial_prompt = self._get_trpg_initial_prompt()

        logger.info(f"Starting transcription: {audio_path}")

        # Whisper 実行
        segments, info = self.model.transcribe(
            audio_path,
            language=language,
            task=task,
            beam_size=settings.WHISPER_BEAM_SIZE,
            patience=settings.WHISPER_PATIENCE,
            temperature=settings.WHISPER_TEMPERATURE,
            vad_filter=settings.WHISPER_VAD_FILTER,
            condition_on_previous_text=settings.WHISPER_CONDITION_ON_PREVIOUS_TEXT,
            initial_prompt=initial_prompt,
        )

        logger.info(
            f"Detected language: {info.language} "
            f"(probability: {info.language_probability:.2f})"
        )

        # セグメント変換
        transcript_segments = []
        full_text_parts = []

        for segment in segments:
            transcript_segments.append(
                TranscriptSegment(
                    start=segment.start,
                    end=segment.end,
                    text=segment.text.strip(),
                    confidence=segment.avg_logprob if hasattr(segment, 'avg_logprob') else None
                )
            )
            full_text_parts.append(segment.text.strip())

        full_text = " ".join(full_text_parts)

        logger.info(
            f"Transcription completed: {len(transcript_segments)} segments, "
            f"{len(full_text)} characters"
        )

        return transcript_segments, full_text

    def _get_trpg_initial_prompt(self) -> str:
        """
        TRPG用語辞書を含む初期プロンプトを生成

        Whisper のゼロショット学習を活用し、TRPG特有の用語を
        正しく認識させるための初期プロンプト
        """
        trpg_terms = [
            # システム名
            "クトゥルフ神話TRPG", "Call of Cthulhu", "CoC",
            "ソード・ワールド", "Sword World",
            "ダンジョンズ&ドラゴンズ", "D&D",

            # 基本用語
            "ゲームマスター", "GM", "キーパー", "KP",
            "プレイヤーキャラクター", "PC", "ノンプレイヤーキャラクター", "NPC",
            "ダイスロール", "ロール", "判定",

            # ダイス表記
            "1D100", "1d100", "2D6", "2d6", "1D20", "1d20",
            "ファンブル", "クリティカル", "スペシャル",

            # 能力値
            "STR", "CON", "POW", "DEX", "APP", "SIZ", "INT", "EDU",
            "HP", "MP", "SAN", "正気度",

            # 技能
            "目星", "聞き耳", "図書館", "説得", "心理学",
            "回避", "隠れる", "忍び歩き",

            # その他
            "シナリオ", "セッション", "シーン",
            "探索", "戦闘", "イベント",
        ]

        return "、".join(trpg_terms) + "。"

    def _is_cuda_available(self) -> bool:
        """
        CUDA利用可能性チェック（PyTorch不要）

        nvidia-smiコマンドでGPUの存在を確認
        """
        try:
            result = subprocess.run(
                ['nvidia-smi'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def cleanup(self):
        """モデルをメモリから解放"""
        if self.model is not None:
            del self.model
            self.model = None
            logger.info("Whisper model cleaned up")


# シングルトンインスタンス
whisper_service = WhisperService()
