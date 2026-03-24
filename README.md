# pizero-openclaw

A voice-controlled AI assistant built on a Raspberry Pi Zero W with a [PiSugar WhisPlay board](https://www.pisugar.com). Press a button, speak, and get a streamed response on the LCD — powered by [OpenClaw](https://openclaw.ai) and Alibaba Cloud Bailian.

## How it works

```
Button press → Record audio → Transcribe (Bailian Qwen ASR) → Stream LLM response (OpenClaw) → Display on LCD
                                                                                             → Speak aloud (Bailian Qwen-TTS, optional)
```

1. **Press & hold** the button to record your voice via ALSA
2. **Release** — the WAV is sent to Bailian for transcription
3. The transcript (with conversation history) is streamed to an **OpenClaw gateway** for a response
4. Text streams onto the **LCD** in real time with pixel-accurate word wrapping
5. Optionally **speaks the response** via Bailian Qwen-TTS as sentences complete
6. The idle screen shows a **clock, date, battery %, and WiFi status**

The device maintains **conversation memory** across exchanges and includes a **silence gate** to skip empty recordings.

## Hardware

- **Raspberry Pi Zero 2 W** (or Pi Zero W)
- **[PiSugar WhisPlay board](https://www.pisugar.com)** — 1.54" LCD (240x240), push-to-talk button, LED, speaker, microphone
- **PiSugar battery** (optional) — shows charge level on screen

## Setup

### Prerequisites

- Raspberry Pi OS (Bookworm or later)
- Python 3.11+
- A Bailian / DashScope API key for speech-to-text and TTS
- An [OpenClaw](https://openclaw.ai) gateway running somewhere accessible on your network

### Install dependencies

```bash
sudo apt install python3-numpy python3-pil
pip install requests python-dotenv   # or: pip install -r requirements.txt
```

The WhisPlay hardware driver should be installed at `/home/pi/Whisplay/Driver/` per the [PiSugar WhisPlay setup guide](https://github.com/PiSugar/whisplay-ai-chatbot).

### Configure

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
```

Edit `.env`:

```bash
export DASHSCOPE_API_KEY="sk-your-bailian-api-key"
export OPENCLAW_TOKEN="your-openclaw-gateway-token"
```

### Run

```bash
python3 main.py
```

Or deploy as a systemd service (see below).

## Configuration

All settings are configured via environment variables (loaded from `.env`):

| Variable | Default | Description |
|---|---|---|
| `DASHSCOPE_API_KEY` | _(required)_ | Bailian / DashScope API key for ASR and TTS |
| `OPENCLAW_TOKEN` | _(required)_ | Auth token for the OpenClaw gateway |
| `OPENCLAW_BASE_URL` | `https://...` | OpenClaw gateway URL |
| `BAILIAN_API_BASE_URL` | `https://dashscope.aliyuncs.com/api/v1` | Bailian native API base URL |
| `BAILIAN_COMPATIBLE_BASE_URL` | `https://dashscope.aliyuncs.com/compatible-mode/v1` | Bailian OpenAI-compatible base URL |
| `BAILIAN_ASR_MODEL` | `qwen3-asr-flash` | Short-audio ASR model |
| `BAILIAN_ASR_LANGUAGE` | `zh` | Optional ASR language hint |
| `BAILIAN_ASR_ENABLE_ITN` | `false` | Enable inverse text normalization |
| `ENABLE_TTS` | `true` | Speak responses aloud via Bailian Qwen-TTS |
| `BAILIAN_TTS_MODEL` | `qwen3-tts-instruct-flash` | TTS model |
| `BAILIAN_TTS_VOICE` | `Cherry` | TTS voice |
| `BAILIAN_TTS_LANGUAGE` | `Chinese` | TTS language type |
| `BAILIAN_TTS_GAIN_DB` | `9` | Software volume boost in dB |
| `BAILIAN_TTS_INSTRUCTIONS` | built-in | Natural-language style control for TTS |
| `AUDIO_DEVICE` | `plughw:1,0` | ALSA input device |
| `AUDIO_OUTPUT_DEVICE` | `default` | ALSA output device |
| `AUDIO_SAMPLE_RATE` | `16000` | Recording sample rate |
| `LCD_BACKLIGHT` | `70` | Backlight brightness (0–100) |
| `UI_MAX_FPS` | `4` | Max display refresh rate |
| `CONVERSATION_HISTORY_LENGTH` | `5` | Past exchanges to keep for context |
| `SILENCE_RMS_THRESHOLD` | `200` | Audio RMS below this is skipped |

## Deploy with systemd

The included `sync.sh` script deploys to the Pi and sets up the service:

```bash
./sync.sh
```

This rsyncs the project to `pi@pizero.local`, installs the systemd unit, and restarts the service. Logs are available via:

```bash
# On the Pi:
sudo journalctl -u pizero-openclaw -f

# Or check the debug log:
cat /tmp/openclaw.log
```

## Project structure

```
main.py               — Entry point and orchestrator
display.py            — LCD rendering (status, responses, idle clock, spinner)
openclaw_client.py    — Streaming HTTP client for the OpenClaw gateway
transcribe_bailian.py — Speech-to-text via Bailian Qwen ASR
tts_bailian.py        — Text-to-speech via Bailian Qwen-TTS + ALSA playback
record_audio.py       — Audio recording via ALSA arecord
button_ptt.py         — Push-to-talk button state machine
config.py             — Centralized configuration from .env
sync.sh               — Deploy script (rsync + systemd restart)
```

## License

MIT
