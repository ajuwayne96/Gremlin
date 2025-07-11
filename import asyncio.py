import asyncio
import edge_tts
from playsound import playsound

VOICE = "ja-JP-NanamiNeural"  # Anime-style Japanese voice
OUTPUT_FILE = "voice_output.mp3"

async def speak(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(OUTPUT_FILE)
    playsound(OUTPUT_FILE)

if __name__ == "__main__":
    text = "こんにちは、バカ！あなたは今日もコードを書いていません！"
    asyncio.run(speak(text))
