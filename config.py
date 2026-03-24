import os
from dotenv import load_dotenv

load_dotenv()


DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
BAILIAN_API_BASE_URL = os.environ.get(
    "BAILIAN_API_BASE_URL", "https://dashscope.aliyuncs.com/api/v1"
)
BAILIAN_COMPATIBLE_BASE_URL = os.environ.get(
    "BAILIAN_COMPATIBLE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"
)
BAILIAN_ASR_MODEL = os.environ.get("BAILIAN_ASR_MODEL", "qwen3-asr-flash")
BAILIAN_ASR_LANGUAGE = os.environ.get("BAILIAN_ASR_LANGUAGE", "zh")
BAILIAN_ASR_ENABLE_ITN = os.environ.get(
    "BAILIAN_ASR_ENABLE_ITN", "false"
).lower() in ("true", "1", "yes")
BAILIAN_TTS_MODEL = os.environ.get(
    "BAILIAN_TTS_MODEL", "qwen3-tts-instruct-flash"
)
BAILIAN_TTS_VOICE = os.environ.get("BAILIAN_TTS_VOICE", "Cherry")
BAILIAN_TTS_LANGUAGE = os.environ.get("BAILIAN_TTS_LANGUAGE", "Chinese")
BAILIAN_TTS_GAIN_DB = float(os.environ.get("BAILIAN_TTS_GAIN_DB", "9"))
BAILIAN_TTS_INSTRUCTIONS = os.environ.get(
    "BAILIAN_TTS_INSTRUCTIONS",
    "用温暖、甜美、俏皮的语气说话，音调稍高，像一个可爱的小伙伴。"
    "情绪自然、语流顺滑，不要机械或单调，句子之间连贯衔接。",
)

OPENCLAW_BASE_URL = os.environ.get("OPENCLAW_BASE_URL", "http://localhost:18789")
OPENCLAW_TOKEN = os.environ.get("OPENCLAW_TOKEN", "")

AUDIO_DEVICE = os.environ.get("AUDIO_DEVICE", "plughw:1,0")
AUDIO_OUTPUT_DEVICE = os.environ.get("AUDIO_OUTPUT_DEVICE", "default")
AUDIO_OUTPUT_CARD = int(os.environ.get("AUDIO_OUTPUT_CARD", "0"))
AUDIO_SAMPLE_RATE = int(os.environ.get("AUDIO_SAMPLE_RATE", "16000"))

DRY_RUN = not DASHSCOPE_API_KEY

LCD_BACKLIGHT = int(os.environ.get("LCD_BACKLIGHT", "70"))
UI_MAX_FPS = int(os.environ.get("UI_MAX_FPS", "4"))

ENABLE_TTS = os.environ.get("ENABLE_TTS", "true").lower() in ("true", "1", "yes")

CONVERSATION_HISTORY_LENGTH = int(os.environ.get("CONVERSATION_HISTORY_LENGTH", "5"))

SILENCE_RMS_THRESHOLD = float(os.environ.get("SILENCE_RMS_THRESHOLD", "200"))


def print_config():
    """Print non-secret config for debugging."""
    print(f"BAILIAN_API_BASE_URL    = {BAILIAN_API_BASE_URL}")
    print(f"BAILIAN_COMPAT_BASE_URL = {BAILIAN_COMPATIBLE_BASE_URL}")
    print(f"BAILIAN_ASR_MODEL       = {BAILIAN_ASR_MODEL}")
    print(f"BAILIAN_ASR_LANGUAGE    = {BAILIAN_ASR_LANGUAGE}")
    print(f"BAILIAN_ASR_ENABLE_ITN  = {BAILIAN_ASR_ENABLE_ITN}")
    print(f"BAILIAN_TTS_MODEL       = {BAILIAN_TTS_MODEL}")
    print(f"BAILIAN_TTS_VOICE       = {BAILIAN_TTS_VOICE}")
    print(f"BAILIAN_TTS_LANGUAGE    = {BAILIAN_TTS_LANGUAGE}")
    print(f"BAILIAN_TTS_GAIN_DB     = {BAILIAN_TTS_GAIN_DB}")
    print(f"BAILIAN_TTS_INSTR       = {BAILIAN_TTS_INSTRUCTIONS[:60]}...")
    print(f"OPENCLAW_BASE_URL       = {OPENCLAW_BASE_URL}")
    print(f"AUDIO_DEVICE            = {AUDIO_DEVICE}")
    print(f"AUDIO_OUTPUT_DEVICE     = {AUDIO_OUTPUT_DEVICE}")
    print(f"AUDIO_SAMPLE_RATE       = {AUDIO_SAMPLE_RATE}")
    print(f"DRY_RUN                 = {DRY_RUN}")
    print(f"LCD_BACKLIGHT           = {LCD_BACKLIGHT}")
    print(f"DASHSCOPE_API_KEY set   = {bool(DASHSCOPE_API_KEY)}")
    print(f"OPENCLAW_TOKEN set      = {bool(OPENCLAW_TOKEN)}")
    print(f"ENABLE_TTS              = {ENABLE_TTS}")
    print(f"CONVERSATION_HISTORY    = {CONVERSATION_HISTORY_LENGTH}")
    print(f"SILENCE_RMS_THRESHOLD   = {SILENCE_RMS_THRESHOLD}")
