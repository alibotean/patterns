"""
Facade Pattern

Intent: Provide a unified, simplified interface to a set of interfaces in a subsystem,
making it easier to use without hiding it entirely.

Example: a video conversion pipeline with several specialist subsystems.
The client calls VideoConverter.convert() — a single method that hides
codec selection, buffering, encoding, and file I/O.
"""

from __future__ import annotations


# ── Subsystem classes (complex internals) ─────────────────────────────────────

class VideoDecoder:
    def decode(self, filepath: str, codec: str) -> bytes:
        print(f"  [VideoDecoder] Decoding '{filepath}' with {codec} codec")
        return b"<raw_video_frames>"


class AudioDecoder:
    def decode(self, filepath: str) -> bytes:
        print(f"  [AudioDecoder] Extracting audio from '{filepath}'")
        return b"<raw_audio_samples>"


class VideoEncoder:
    def encode(self, raw: bytes, target_codec: str) -> bytes:
        print(f"  [VideoEncoder] Encoding to {target_codec}")
        return b"<encoded_video>"


class AudioEncoder:
    def encode(self, raw: bytes, bitrate: int) -> bytes:
        print(f"  [AudioEncoder] Encoding audio at {bitrate} kbps")
        return b"<encoded_audio>"


class Multiplexer:
    """Combines encoded video and audio streams into a container file."""
    def mux(self, video: bytes, audio: bytes, output_path: str) -> None:
        print(f"  [Multiplexer] Muxing streams → '{output_path}'")


class FileWriter:
    def write(self, path: str, data: bytes) -> None:
        print(f"  [FileWriter] Writing {len(data)} bytes to '{path}'")


# ── Facade ────────────────────────────────────────────────────────────────────

class VideoConverter:
    """
    Hides the entire conversion pipeline behind two parameters: input file and format.
    The client never interacts with any of the six subsystem classes above.
    """

    # Codec lookup table — maps file extensions to codec names
    _VIDEO_CODECS = {"mp4": "H.264", "webm": "VP9",  "avi": "MPEG-4"}
    _AUDIO_BITRATES = {"mp4": 192, "webm": 128, "avi": 128}

    def __init__(self) -> None:
        # Wire up subsystems internally — the client never sees these
        self._video_dec = VideoDecoder()
        self._audio_dec = AudioDecoder()
        self._video_enc = VideoEncoder()
        self._audio_enc = AudioEncoder()
        self._muxer     = Multiplexer()
        self._writer    = FileWriter()

    def convert(self, input_file: str, output_format: str) -> str:
        """
        One-call conversion from any supported format to another.
        Returns the path of the output file.
        """
        fmt = output_format.lower().lstrip(".")
        if fmt not in self._VIDEO_CODECS:
            raise ValueError(f"Unsupported format: {fmt}")

        output_path  = input_file.rsplit(".", 1)[0] + f".{fmt}"
        target_codec = self._VIDEO_CODECS[fmt]
        audio_rate   = self._AUDIO_BITRATES[fmt]

        print(f"[VideoConverter] Converting '{input_file}' → '{output_path}'")

        # Orchestrate the subsystems in the correct order
        raw_video   = self._video_dec.decode(input_file, "auto")
        raw_audio   = self._audio_dec.decode(input_file)
        enc_video   = self._video_enc.encode(raw_video, target_codec)
        enc_audio   = self._audio_enc.encode(raw_audio, audio_rate)
        self._muxer.mux(enc_video, enc_audio, output_path)

        print(f"[VideoConverter] Done → '{output_path}'\n")
        return output_path


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    converter = VideoConverter()

    # One call to do all the work — subsystem complexity is invisible
    converter.convert("holiday_2025.avi", "mp4")
    converter.convert("screencast.mp4",   "webm")
