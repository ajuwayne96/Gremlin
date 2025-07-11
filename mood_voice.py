import asyncio
import edge_tts
import pygame
import os

VOICE = "ja-JP-NanamiNeural"
OUTPUT_FILE = "assets/voice_output.mp3"

voice_lines = {
    "happy": "やった！今日もちゃんとコードを書いたね！えらい！",
    "meh": "うーん、今日はちょっとだけだったかな？",
    "angry": "バカ！全然コード書いてないじゃん！",
    "cry": "ご主人様……どうして書いてくれないの……？"
}

async def speak_mood(mood):
    if mood not in voice_lines:
        print(f"[WARN] Unknown mood: {mood}")
        return

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    print(f"[TTS] Generating speech for mood: {mood}")
    communicate = edge_tts.Communicate(voice_lines[mood], VOICE)
    await communicate.save(OUTPUT_FILE)
    print("[TTS] Audio saved:", OUTPUT_FILE)

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(OUTPUT_FILE)
        pygame.mixer.music.play()
        print("[AUDIO] Playing voice...")

        # Wait until audio playback is done
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)

        print("[AUDIO] Playback complete.")

    except Exception as e:
        print(f"[ERROR] Failed to play audio: {e}")
