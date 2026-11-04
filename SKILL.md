# Reel Generator Skill for Antigravity

**COMMAND TRIGGER:**
When the user types `/reel [topic]`, you must immediately start the Reel Generation workflow for that topic without asking any extra questions.

**STEP 1: The Viral Scripting (130-150 words limit)**
Write a fast-paced Hinglish script following this strict formula:
- 0-5s: Aggressive Hook (Start with a mind-blowing question).
- 5-15s: Context & Build-up.
- 15-45s: Core Explanation (Fast facts, data-driven).
- 45-55s: The Climax (A secret or shocking fact).
- 55-60s: CTA ("Aapki is par kya raye hai? Comments me batayein aur follow karein!").
Output the script with punctuation (commas for short pause, periods for long pause). Never use emojis.

**STEP 2: Asset & SFX Tagging (JSON Output)**
Do not render anything yet. First, create a JSON blueprint.
Tag specific words in the script where visual changes must happen.
Use only these local SFX: [whoosh.mp3, pop.mp3, deep_boom.mp3, digital_typing.mp3, glitch.mp3].
Specify if a public figure's image needs to be fetched.
Example: `{"word": "Sardar", "action": "fetch_image", "query": "Sardar Vallabhbhai Patel", "sfx": "pop.mp3"}`

**STEP 3: Tool Execution Sequence**
You must call the local Python tools in this exact order:
1. Run `tools/tts_engine.py` to generate `audio.mp3` and `captions.vtt` using edge-tts (hi-IN-MadhurNeural, +10% rate).
2. Run `tools/whisper_sync.py` to convert `.vtt` into a precise word-level timestamp JSON.
3. Run `tools/asset_fetcher.py` to download leader images from Wikipedia and remove backgrounds using `rembg`.
4. Run `tools/video_render.py` (MoviePy) to stitch everything together based on the Whisper timestamps.

**STEP 4: Render Rules (After Effects Polish)**
Instruct `video_render.py` to strictly enforce these cinematic rules:
- Apply a continuous 1% slow zoom-in (Ken Burns effect) to the background SVG map to prevent static scenes.
- Add a black drop-shadow/glow to all transparent PNGs fetched by rembg for 3D depth.
- Use Spring Easing (Ease-Out) for all image and text pop-ups (no linear robotic slides).
- Hardcode the watermark (e.g., @StudyFarm) at the top-right corner permanently.
