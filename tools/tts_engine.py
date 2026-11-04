import asyncio
import edge_tts
import sys
import os

# Settings
VOICE = "hi-IN-MadhurNeural" # Authoritative Hindi Male Voice
RATE = "+10%"                # Reels ke hisaab se thodi fast speed

async def generate_audio_and_subs(text, audio_file="audio.mp3", vtt_file="captions.vtt"):
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    sub_maker = edge_tts.SubMaker()

    with open(audio_file, "wb") as audio_fd:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_fd.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                # Timestamp nikalna har word ka
                sub_maker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

    # VTT subtitle file save karna
    with open(vtt_file, "w", encoding="utf-8") as vtt_fd:
        vtt_fd.write(sub_maker.generate_subs())
        
    print(f"✅ Success: '{audio_file}' aur '{vtt_file}' generate ho gaye hain!")

if __name__ == "__main__":
    # Antigravity agent terminal se seedha text bhejega
    if len(sys.argv) > 1:
        script_text = sys.argv[1]
    else:
        # Agar text nahi diya, toh test text
        script_text = "Kya aap jante hain, ki China ka naya masterplan India ko kaise affect karega?"
    
    asyncio.run(generate_audio_and_subs(script_text))
