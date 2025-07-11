import os
import datetime
import asyncio
import edge_tts
import pygame

# === CONFIGURATION === #
VOICE = "ja-JP-NanamiNeural"
OUTPUT_FILE = "assets/voice_output.mp3"
CODE_FOLDER = "E:\Chumma"  # <- Change this to your actual code directory path

voice_lines = {
    "happy": "やった！今日もちゃんとコードを書いたね！えらい！",
    "meh": "うーん、今日はちょっとだけだったかな？",
    "angry": "バカ！全然コード書いてないじゃん！",
    "cry": "ご主人様……どうして書いてくれないの……？"
}

# === DETECT LAST CODE ACTIVITY === #
def get_last_code_edit_date(code_dir):
    latest_time = 0
    for root, _, files in os.walk(code_dir):
        for file in files:
            if file.endswith((".py", ".cs", ".js", ".cpp", ".java", ".html", ".css")):
                try:
                    path = os.path.join(root, file)
                    file_time = os.path.getmtime(path)
                    if file_time > latest_time:
                        latest_time = file_time
                except:
                    continue
    return datetime.datetime.fromtimestamp(latest_time) if latest_time > 0 else None

def determine_mood(last_edit_date):
    if last_edit_date is None:
        return "cry"
    days_passed = (datetime.datetime.now() - last_edit_date).days
    if days_passed == 0:
        return "happy"
    elif days_passed == 1:
        return "meh"
    elif days_passed <= 3:
        return "angry"
    else:
        return "cry"

# === SPEAK THE MOOD USING edge-tts === #
async def speak_mood(mood):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    communicate = edge_tts.Communicate(voice_lines[mood], VOICE)
    await communicate.save(OUTPUT_FILE)

    pygame.mixer.init()
    pygame.mixer.music.load(OUTPUT_FILE)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)

# === MAIN === #
async def main():
    last_edit = get_last_code_edit_date(CODE_FOLDER)
    mood = determine_mood(last_edit)
    print(f"[INFO] Last coded on: {last_edit} → Mood: {mood}")
    await speak_mood(mood)

asyncio.run(main())
