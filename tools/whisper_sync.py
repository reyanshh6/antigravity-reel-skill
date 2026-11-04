import json
import re
import sys
import os

def vtt_to_json(vtt_file="captions.vtt", json_file="word_timestamps.json"):
    if not os.path.exists(vtt_file):
        print(f"❌ Error: '{vtt_file}' nahi mili! Pehle tts_engine.py chalao.")
        return
        
    with open(vtt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    words_data = []
    # VTT time format (HH:MM:SS.mmm) dhoondhne ke liye regex
    time_pattern = re.compile(r"(\d{2}:\d{2}:\d{2}\.\d{3})\s-->\s(\d{2}:\d{2}:\d{2}\.\d{3})")
    
    current_start = ""
    current_end = ""
    
    # HH:MM:SS.mmm ko seconds me convert karne ka function
    def time_to_sec(t):
        h, m, s = t.split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)

    for line in lines:
        line = line.strip()
        time_match = time_pattern.match(line)
        if time_match:
            current_start = time_match.group(1)
            current_end = time_match.group(2)
        elif line and not line.startswith("WEBVTT") and "-->" not in line:
            # Word aur uska exact time dictionary me save karna
            word_info = {
                "word": line,
                "start": time_to_sec(current_start),
                "end": time_to_sec(current_end)
            }
            words_data.append(word_info)

    # Final JSON save karna
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(words_data, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Success: Word timestamps perfectly '{json_file}' me save ho gaye hain!")

if __name__ == "__main__":
    # Agent command line se file path bhej sakta hai
    input_vtt = sys.argv[1] if len(sys.argv) > 1 else "captions.vtt"
    output_json = sys.argv[2] if len(sys.argv) > 2 else "word_timestamps.json"
    
    vtt_to_json(input_vtt, output_json)
