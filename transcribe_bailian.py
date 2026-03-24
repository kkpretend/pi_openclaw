import base64
import mimetypes
import os

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import config

_http_session: requests.Session | None = None


def _get_session() -> requests.Session:
    global _http_session
    if _http_session is None:
        _http_session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=[502, 503, 504],
            allowed_methods=["POST"],
        )
        adapter = HTTPAdapter(max_retries=retry)
        _http_session.mount("http://", adapter)
        _http_session.mount("https://", adapter)
    return _http_session


def _to_data_url(audio_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(audio_path)
    if not mime_type:
        mime_type = "audio/wav"
    with open(audio_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def transcribe(wav_path: str) -> str:
    """Transcribe a local audio file using Bailian Qwen ASR."""
    if config.DRY_RUN:
        print("[transcribe] DRY RUN — type your message:")
        try:
            return input("> ").strip()
        except EOFError:
            return ""

    if not os.path.exists(wav_path):
        raise FileNotFoundError(f"WAV file not found: {wav_path}")

    file_size = os.path.getsize(wav_path)
    if file_size < 100:
        raise ValueError(f"WAV file too small ({file_size} bytes), likely empty recording")
    if file_size > 10 * 1024 * 1024:
        raise ValueError(f"WAV file too large for qwen3-asr-flash ({file_size} bytes > 10MB)")

    url = f"{config.BAILIAN_COMPATIBLE_BASE_URL.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {config.DASHSCOPE_API_KEY}",
        "Content-Type": "application/json",
    }
    asr_options: dict[str, object] = {
        "enable_itn": config.BAILIAN_ASR_ENABLE_ITN,
    }
    if config.BAILIAN_ASR_LANGUAGE:
        asr_options["language"] = config.BAILIAN_ASR_LANGUAGE
    payload = {
        "model": config.BAILIAN_ASR_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": _to_data_url(wav_path),
                        },
                    }
                ],
            }
        ],
        "stream": False,
        "asr_options": asr_options,
    }

    try:
        resp = _get_session().post(url, headers=headers, json=payload, timeout=60)
    except (requests.ConnectionError, requests.Timeout) as e:
        raise RuntimeError(f"Transcription request failed: {e}") from e

    if resp.status_code != 200:
        raise RuntimeError(
            f"Transcription failed ({resp.status_code}): {resp.text[:300]}"
        )

    data = resp.json()
    try:
        transcript = data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, AttributeError, TypeError) as e:
        raise RuntimeError(f"Unexpected transcription response: {data}") from e

    print(f"[transcribe] result: {transcript[:120]}")
    return transcript
