import json
import sys
import os
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip

def render_reel(audio_path="audio.mp3", json_path="word_timestamps.json", bg_image="assets/map_bg.jpg", cutout_image="leader_cutout.png", output_file="final_reel.mp4"):
    print("🎬 Render Engine Start ho raha hai... After Effects wala magic load ho raha hai!")

    if not os.path.exists(audio_path) or not os.path.exists(json_path):
        print("❌ Error: Audio ya JSON file nahi mili. Pehle tts_engine aur whisper_sync chalao!")
        return

    # 1. Audio Layer load karna
    audio = AudioFileClip(audio_path)
    video_duration = audio.duration

    # 2. Background Map with Ken Burns (Slow Zoom Effect)
    # Background hamesha 1% speed se zoom hoga taaki video static na lage
    print("🗺️ Background Map setup ho raha hai (Applying slow zoom)...")
    bg_clip = ImageClip(bg_image).set_duration(video_duration)
    # Note: Custom zoom lambda function for continuous smooth scale
    bg_clip = bg_clip.resize(lambda t: 1 + 0.02 * t).set_position('center')

    # 3. Permanent Watermark Layer (@StudyFarm)
    print("💧 Watermark lagaya ja raha hai...")
    watermark = TextClip("@StudyFarm", fontsize=35, color='white', font='Arial-Bold', opacity=0.6)
    watermark = watermark.set_position(("right", "top")).margin(top=30, right=30, opacity=0).set_duration(video_duration)

    clips_to_render = [bg_clip, watermark]

    # 4. Image Cutout Layer (Agar agent ne download ki hai)
    if os.path.exists(cutout_image):
        print("👤 Leader ki photo add ho rahi hai...")
        leader_clip = ImageClip(cutout_image).set_duration(video_duration - 1)
        # Niche center me rakhenge, aur start time me 1 sec ka delay (Pop-up effect)
        leader_clip = leader_clip.resize(height=500).set_position(("center", "bottom")).set_start(1)
        # (Advance easing yahan MoviePy custom functions se hoti hai)
        clips_to_render.append(leader_clip)

    # 5. Kinetic Captions (Data-Driven Sync from JSON)
    print("📝 Whisper JSON se perfect subtitles sync ho rahe hain...")
    with open(json_path, 'r', encoding='utf-8') as f:
        words_data = json.load(f)

    for w in words_data:
        word_text = w['word']
        start_time = w['start']
        end_time = w['end']
        
        # Har word ka ek popup text clip
        txt_clip = TextClip(word_text, fontsize=80, color='yellow', stroke_color='black', stroke_width=3, font='Impact')
        txt_clip = txt_clip.set_position(("center", "center")).set_start(start_time).set_end(end_time)
        clips_to_render.append(txt_clip)

    # 6. Final Composite & Render
    print("⚙️ Sab kuch merge karke Video render ki ja rahi hai... (Isme thoda time lagega)")
    final_video = CompositeVideoClip(clips_to_render, size=(1080, 1920)) # Vertical 9:16 Reel Size
    final_video = final_video.set_audio(audio)
    
    # 60 FPS aur fast rendering config
    final_video.write_videofile(output_file, fps=30, codec="libx264", audio_codec="aac", preset="ultrafast", threads=4)
    print(f"✅ BAAAM! Aapki pro-level Reel '{output_file}' bilkul ready hai!")

if __name__ == "__main__":
    render_reel()
