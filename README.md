# PiZero OpenClaw 语音助手

基于 Raspberry Pi Zero + PiSugar WhisPlay 的本地语音助手项目。交互方式是按键按住说话，松开后自动转写、请求大模型、流式显示回答，并可选语音播报。

项目核心能力：
- 按键对讲（PTT）
- 语音识别（阿里云百炼 ASR）
- 大模型流式回复（OpenClaw 网关）
- 屏幕实时渲染（240x240 LCD）
- 可选 TTS 播报（阿里云百炼 TTS）
- 会话历史记忆与静音门限过滤

## 1. 系统流程

```text
按下按钮开始录音
  -> 松开按钮停止录音
  -> 检测静音（RMS）
  -> 调用百炼 ASR 转写
  -> 携带历史会话请求 OpenClaw（SSE 流式）
  -> LCD 实时渲染增量文本
  -> 可选：TTS 分句播报
  -> 等待超时/再次按键后回到待机页
```

核心入口见 `main.py`，状态机由 `button_ptt.py` 管理。

## 2. 代码结构

```text
main.py               主流程编排（录音/转写/请求/显示/TTS）
display.py            LCD 渲染与动画（待机页/状态页/角色/滚动文本）
openclaw_client.py    OpenClaw 流式请求客户端（/v1/responses）
transcribe_bailian.py 百炼 ASR
tts_bailian.py        百炼 TTS + 本地播放 + 口型时间轴
record_audio.py       arecord 录音与音量检测
button_ptt.py         按键状态机
config.py             环境变量读取与配置中心
pizero-openclaw.service systemd 服务文件
sync.sh               便捷部署脚本
```

## 3. 运行环境

硬件建议：
- Raspberry Pi Zero W / Zero 2 W
- PiSugar WhisPlay（含屏幕、麦克风、喇叭、按键）

软件依赖：
- Python 3.11+
- 系统库：`numpy`、`Pillow`
- Python 包：`requests`、`python-dotenv`

安装示例：

```bash
sudo apt update
sudo apt install -y python3-numpy python3-pil
python3 -m pip install -r requirements.txt
```

`requirements.txt` 当前包含：
- `numpy`
- `Pillow`
- `requests`
- `python-dotenv`

## 4. 配置说明（.env）

复制模板：

```bash
cp .env.example .env
```

关键变量：

| 变量名 | 说明 | 默认值 |
|---|---|---|
| `DASHSCOPE_API_KEY` | 百炼 API Key（ASR/TTS） | 空 |
| `OPENCLAW_TOKEN` | OpenClaw 网关 Bearer Token | 空 |
| `OPENCLAW_BASE_URL` | OpenClaw 网关地址（不建议结尾带 `/`） | `http://localhost:18789` |
| `BAILIAN_API_BASE_URL` | 百炼原生 API 地址 | `https://dashscope.aliyuncs.com/api/v1` |
| `BAILIAN_COMPATIBLE_BASE_URL` | 百炼 OpenAI 兼容地址 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| `BAILIAN_ASR_MODEL` | ASR 模型 | `qwen3-asr-flash` |
| `BAILIAN_ASR_LANGUAGE` | ASR 语言提示 | `zh` |
| `BAILIAN_ASR_ENABLE_ITN` | 是否启用 ITN | `false` |
| `ENABLE_TTS` | 是否启用 TTS | `true` |
| `BAILIAN_TTS_MODEL` | TTS 模型 | `qwen3-tts-instruct-flash` |
| `BAILIAN_TTS_VOICE` | TTS 音色 | `Cherry` |
| `BAILIAN_TTS_LANGUAGE` | TTS 语言 | `Chinese` |
| `BAILIAN_TTS_GAIN_DB` | TTS 增益 | `9` |
| `BAILIAN_TTS_INSTRUCTIONS` | TTS 风格提示词 | 内置中文提示 |
| `AUDIO_DEVICE` | 录音设备 | `plughw:1,0` |
| `AUDIO_OUTPUT_DEVICE` | 播放设备 | `default` |
| `AUDIO_OUTPUT_CARD` | 播放声卡序号 | `0` |
| `AUDIO_SAMPLE_RATE` | 采样率 | `16000` |
| `LCD_BACKLIGHT` | 背光亮度 0-100 | `70` |
| `UI_MAX_FPS` | 屏幕最大刷新率 | `4` |
| `CONVERSATION_HISTORY_LENGTH` | 保留历史轮数 | `5` |
| `SILENCE_RMS_THRESHOLD` | 静音门限 | `200` |

## 5. 启动方式

开发运行：

```bash
python3 main.py
```

systemd 运行：

```bash
sudo cp pizero-openclaw.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now pizero-openclaw
sudo systemctl status pizero-openclaw
```

查看日志：

```bash
sudo journalctl -u pizero-openclaw -f
cat /tmp/openclaw.log
```

## 6. 屏幕渲染与字体

`display.py` 使用 Pillow 在内存里绘制图像，再转 `RGB565` 推到 LCD。

字体策略：
- `_FONT_PATH`：主状态/标题/时钟等
- `_FONT_PATH_REGULAR`：副标题、正文、提示文本等

如果中文显示方框，通常是字体字形缺失，不是硬件问题。建议安装并使用支持中文的字体，例如：
- `NotoSansCJK-Regular.ttc`
- `DroidSansFallbackFull.ttf`

字体安装后刷新缓存：

```bash
fc-cache -f -v
fc-list :lang=zh | head
```

## 7. OpenClaw 网关注意事项

`openclaw_client.py` 会请求：
- `POST {OPENCLAW_BASE_URL}/v1/responses`
- `Authorization: Bearer <OPENCLAW_TOKEN>`
- `Accept: text/event-stream`

请求体（简化）：

```json
{
  "model": "openclaw",
  "stream": true,
  "input": "..." 或消息数组
}
```

若出现 `404 domain doesn't exist`，通常是隧道域名（如 cpolar 临时域名）失效，不是请求体问题。请检查：
- 隧道是否在线
- 域名是否变更
- `.env` 是否更新并重启服务

## 8. 交互行为细节

- 录音按钮按下开始、松开处理
- 处理过程中再次按键可取消
- 空白语音会被 RMS 静音门限直接丢弃
- LLM 回复按 token 增量显示
- 开启 TTS 时，按句子边界分批播报（更自然）
- 屏幕在空闲一段时间后自动休眠

## 9. 常见问题

1. 中文是方框
- 原因：字体不含中文字形
- 处理：安装中文字体并更新 `display.py` 字体路径

2. 时间/英文乱码
- 原因：将不适合拉丁字符的字体用于时钟字体
- 处理：为 `_FONT_PATH` 选择可读的拉丁字体，正文可用 `_FONT_PATH_REGULAR` 指向中文字体

3. OpenClaw 第一次成功后持续失败
- 原因：网关地址或隧道域名失效
- 处理：验证 `OPENCLAW_BASE_URL` 可达并重启服务

4. 无声音或录不到音
- 处理：核对 `AUDIO_DEVICE`、`AUDIO_OUTPUT_DEVICE`、声卡编号、ALSA 权限

## 10. 安全建议

- 不要把 `.env`（含密钥）提交到仓库
- 建议在生产环境使用固定域名或内网地址，不使用会漂移的临时隧道

## 11. 许可证

MIT
