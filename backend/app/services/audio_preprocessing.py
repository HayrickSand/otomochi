"""
音声前処理サービス

ノイズ除去、正規化、フォーマット変換などを実施
"""
import logging
import os
from typing import Optional
import soundfile as sf
import numpy as np
try:
    import noisereduce as nr
except ImportError:
    nr = None

from ..core.config import settings

logger = logging.getLogger(__name__)


class AudioPreprocessor:
    """音声前処理クラス"""

    def __init__(self):
        """初期化"""
        self.target_sample_rate = 16000  # Whisper の推奨サンプリングレート

    def preprocess(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        apply_noise_reduction: bool = True,
        normalize_audio: bool = True
    ) -> str:
        """
        音声ファイルを前処理

        Args:
            input_path: 入力音声ファイルパス
            output_path: 出力音声ファイルパス（省略時は一時ファイル）
            apply_noise_reduction: ノイズ除去を適用するか
            normalize_audio: 音量正規化を適用するか

        Returns:
            処理後の音声ファイルパス
        """
        logger.info(f"Preprocessing audio: {input_path}")

        # 音声ファイル読み込み
        audio_data, sample_rate = sf.read(input_path)

        # モノラル変換（ステレオの場合）
        if len(audio_data.shape) > 1:
            logger.info("Converting stereo to mono")
            audio_data = np.mean(audio_data, axis=1)

        # リサンプリング
        if sample_rate != self.target_sample_rate:
            logger.info(f"Resampling from {sample_rate}Hz to {self.target_sample_rate}Hz")
            audio_data = self._resample(audio_data, sample_rate, self.target_sample_rate)
            sample_rate = self.target_sample_rate

        # ノイズ除去
        if apply_noise_reduction and nr is not None:
            logger.info("Applying noise reduction")
            audio_data = nr.reduce_noise(
                y=audio_data,
                sr=sample_rate,
                stationary=True,
                prop_decrease=0.5
            )
        elif apply_noise_reduction and nr is None:
            logger.warning("noisereduce not available, skipping noise reduction")

        # 音量正規化（LUFS -23 ~ -16 目標）
        if normalize_audio:
            logger.info("Normalizing audio volume")
            audio_data = self._normalize_volume(audio_data)

        # 出力パス決定
        if output_path is None:
            output_path = os.path.join(
                settings.RAMDISK_PATH,
                f"preprocessed_{os.path.basename(input_path)}"
            )

        # WAV形式で保存（Whisperに最適）
        output_path = os.path.splitext(output_path)[0] + ".wav"
        sf.write(output_path, audio_data, sample_rate)

        logger.info(f"Preprocessing completed: {output_path}")
        return output_path

    def _resample(
        self,
        audio_data: np.ndarray,
        original_sr: int,
        target_sr: int
    ) -> np.ndarray:
        """
        リサンプリング

        NOTE: より高品質なリサンプリングには librosa の使用を推奨
        ここでは簡易的な実装
        """
        # 簡易リサンプリング（線形補間）
        duration = len(audio_data) / original_sr
        target_length = int(duration * target_sr)

        indices = np.linspace(0, len(audio_data) - 1, target_length)
        resampled = np.interp(indices, np.arange(len(audio_data)), audio_data)

        return resampled

    def _normalize_volume(self, audio_data: np.ndarray, target_db: float = -20.0) -> np.ndarray:
        """
        音量正規化

        Args:
            audio_data: 音声データ
            target_db: 目標音量（dB）

        Returns:
            正規化された音声データ
        """
        # RMS計算
        rms = np.sqrt(np.mean(audio_data ** 2))

        if rms == 0:
            return audio_data

        # 目標RMSを計算
        target_rms = 10 ** (target_db / 20)

        # 正規化
        normalized = audio_data * (target_rms / rms)

        # クリッピング防止
        max_val = np.max(np.abs(normalized))
        if max_val > 1.0:
            normalized = normalized / max_val * 0.95

        return normalized

    def get_audio_duration(self, audio_path: str) -> float:
        """
        音声ファイルの長さを取得（秒）

        Args:
            audio_path: 音声ファイルパス

        Returns:
            音声長（秒）
        """
        audio_data, sample_rate = sf.read(audio_path)
        duration = len(audio_data) / sample_rate
        return duration


# シングルトンインスタンス
audio_preprocessor = AudioPreprocessor()
