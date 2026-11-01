# NEXORA — 43-second vertical ad: production plan

**Status: no video has been rendered.** This is a timing analysis, a scene plan, ready-to-paste AI video prompts, a Nepali SRT and a CapCut assembly guide. Nothing here is photoreal CGI that I produced. The 3D clips come from an AI video tool using the prompts below, and you assemble them in CapCut.

Files in this repo:
- `assets/NEXORA_logo.png`: your logo, unmodified.
- `subtitles/nexora_ne_plain.srt`: clean Nepali SRT, 20 cues.
- `subtitles/nexora_ne_gold_tags.srt`: the same cues with gold keyword tags (`<font color>`). Some editors ignore the tags, so see section 6.
- `tools/gen_timing.py`: regenerates the SRTs and trigger times if you edit anything.

---

## 0. What is measured and what is estimated

| Item | Status |
|---|---|
| Audio duration **43.00 s** | Measured (ffprobe) |
| The 13 speech-segment boundaries | Measured (ffmpeg silencedetect, −35 dB, min pause 0.25 s) |
| Which script sentence sits in which segment | Inferred. It is a best fit on duration and word count, verified by loudness, and could not be checked by listening. |
| Phrase and keyword times inside a segment (marked **≈**) | Estimated. I spread the phrases across the segment in proportion to their character counts. They are not recognised word timestamps, and the error is typically ±0.3–0.5 s. |

### Mapping notes
- Segments 2 (6.08–6.41) and 4 (10.60–10.98) average about −34 and −30 dB, against about −17 to −20 dB for the speech around them. I treat them as breaths or trailing sounds with no script text. They get no subtitle, and no sentence was assigned to them.
- That leaves 11 speech segments for 12 script sentences. The only place where the durations fit is **segment 7 (6.27 s) holding sentence 5 plus sentence 6** ("…अवसर दिँदैछौँ! तपाईंले गर्नुपर्ने यति मात्रै हो:"), with a pause of less than 0.25 s between them. I put the split at **≈ 22.97 s**.
- **Please check these three spots by ear and tell me if any is wrong:** 6.08 s and 10.60 s should be breaths, and the sentence-6 start near 22.97 s sits inside segment 7.

---

## 1. Sentence-to-segment map

| Seg | Time (measured) | Dur | Script text | Notes |
|---|---|---|---|---|
| 1 | 0.00–5.53 | 5.53 | के तपाईंको Social Media Account मा Followers, Likes र Views एकदमै कम छन्? | S1 |
| 2 | 6.08–6.41 | 0.33 | (breath, no text) | |
| 3 | 6.93–10.03 | 3.10 | आफ्नो Video मा राम्रो Views नआएर चिन्तित हुनुहुन्छ? | S2 |
| 4 | 10.60–10.98 | 0.38 | (breath, no text) | |
| 5 | 11.40–13.34 | 1.94 | त्यसो भए अब चिन्ता नगर्नुहोस्! | S3 |
| 6 | 13.74–17.99 | 4.25 | किनकि NEXORA ले ल्याएको छ एउटा विशेष FREE PROMOTION CAMPAIGN! | S4 |
| 7 | 18.34–24.61 | 6.27 | हामी पहिलो ५० जना भाग्यशाली व्यक्तिहरूलाई Free मा आफ्नो पहिलो Video Promote गर्ने अवसर दिँदैछौँ! + तपाईंले गर्नुपर्ने यति मात्रै हो: | S5 + S6 (inferred merge) |
| 8 | 25.05–26.91 | 1.86 | यो Video लाई Like गर्नुहोस्। | S7 |
| 9 | 27.26–28.90 | 1.64 | आफ्ना १० जना साथीहरूलाई Mention गर्नुहोस्। | S8 |
| 10 | 29.24–31.79 | 2.55 | अनि आफ्नो Story मा Repost गर्नुहोस्। | S9 |
| 11 | 32.07–34.52 | 2.45 | साथै NEXORA को Official Page Follow गर्न नभुल्नुहोला! | S10 |
| 12 | 34.88–38.50 | 3.62 | चयन भएका ५० जनालाई हामी DM मार्फत सम्पर्क गर्नेछौँ। | S11 |
| 13 | 38.95–42.70 | 3.75 | NEXORA – Upgrade Your Digital Life! | S12 |

The audio ends at 43.00 s. The last 0.30 s is silence, which is where the logo holds and fades.

### Estimated trigger times (≈)
Followers 2.63 · Likes 3.54 · Views 4.08 · "एकदमै कम" 4.53 · Views (S2) 8.20 · चिन्तित 8.83 · "अब चिन्ता" 11.92 · NEXORA 14.15 · FREE PROMOTION 16.19 · "५० जना" 18.85 · Free 20.37 · Video 20.99 · Promote 21.56 · तपाईंले 22.97 · Like 25.82 · "१० जना" 27.48 · Mention 28.15 · Story 29.90 · Repost 30.47 · NEXORA 32.28 · Official 32.71 · Follow 33.35 · "५० जनालाई" 35.47 · DM 36.48 · NEXORA (final) 38.95 · Upgrade 39.83

---

## 2. Scene timeline (43.00 s, 16 scenes)

Cuts fall inside pauses wherever the audio has one. Elsewhere they sit on the estimated trigger word, so allow ±0.3 s.

| # | Time | Spoken (approx.) | Visual | Transition out |
|---|---|---|---|---|
| 01 | 0.00–3.20 | के तपाईंको Social Media Account मा Followers | Dark room, creator's phone, a profile panel with a **low follower counter** appears ≈2.6 | Hard cut on the counter tick |
| 02 | 3.20–3.95 | Likes | Dim, cracked-glass heart icons, **low likes counter** ≈3.54 | Quick push-in cut |
| 03 | 3.95–6.50 | Views एकदमै कम छन्? | Video player with **low views counter** ≈4.08; a flat stat graph droops ≈4.5 | Dip to black through the 6.08 breath |
| 04 | 6.50–10.30 | आफ्नो Video… चिन्तित हुनुहुन्छ? | Creator checking a post that is getting no engagement. **Worried face** ≈8.83 | Camera pushes in on the face and the screen glare dims to near black |
| 05 | 10.30–13.60 | त्यसो भए अब चिन्ता नगर्नुहोस्! | Silence and darkness through 11.40, then a **golden portal** opens ≈11.92 and the room transforms into a futuristic golden world | Flash-white-gold wipe |
| 06 | 13.60–15.90 | किनकि NEXORA ले ल्याएको छ | **Logo reveal** (your PNG) ≈14.15 with metallic gold light sweep | Light-streak into the next scene |
| 07 | 15.90–18.20 | एउटा विशेष FREE PROMOTION CAMPAIGN! | **Golden gift box opens** ≈16.2–17.9 | Particle burst carries into scene 08 |
| 08 | 18.20–20.30 | हामी पहिलो ५० जना… | **50 golden particles** swirl and form the number 50 ≈18.85–20.0 | Particles dissolve into the phone screen |
| 09 | 20.30–22.90 | Free मा आफ्नो पहिलो Video Promote गर्ने… | **Phone plays a video** ≈20.4–21.5, then **rises into a golden spotlight** ≈21.56 | Hold, then a soft shine |
| 10 | 22.90–25.00 | तपाईंले गर्नुपर्ने यति मात्रै हो: | Four golden step-pedestals light up in sequence (a teaser for Like, Mention, Repost and Follow) | Pedestal 1 flares into the heart |
| 11 | 25.00–27.10 | यो Video लाई Like गर्नुहोस्। | **3D golden heart** pulses ≈25.82 | Heart bursts into a sparkle |
| 12 | 27.10–29.10 | आफ्ना १० जना साथीहरूलाई Mention गर्नुहोस्। | **Exactly 10 profile icons** pop in one by one ≈27.40–28.90, then an @ badge on Mention ≈28.15 | Icons fly into the phone |
| 13 | 29.10–32.00 | अनि आफ्नो Story मा Repost गर्नुहोस्। | **Rotating 3D repost symbol** orbits a phone ≈30.47 | Orbit ring wipes the frame |
| 14 | 32.00–34.70 | साथै NEXORA को Official Page Follow गर्न नभुल्नुहोला! | Official-page screen with a **golden Follow button**, pressed ≈33.35 | Press-flash cut |
| 15 | 34.70–38.70 | चयन भएका ५० जनालाई हामी DM मार्फत… | A "50 selected" badge ≈35.5, then a **phone receives a message notification** ≈36.48 | Notification expands into light |
| 16 | 38.70–43.00 | NEXORA – Upgrade Your Digital Life! | **Final cinematic logo reveal** ≈38.95, hold to 43.00, fade to black | None |

---

## 3. AI video prompts (one per scene)

Use these in Runway, Kling, Veo, Sora or similar. Set the aspect ratio to 9:16 and generate about 1 s more than the scene length, so you have trim handles.

**Rules that matter:**
- **Do not let the AI draw your logo, any text, or the numbers 50 and 10.** Generators misspell, distort and miscount. Every prompt asks for blank or no-text output. In CapCut, composite the real `assets/NEXORA_logo.png`, the counters, the "50" and the subtitles.
- If a generator gives you the wrong number of profile icons or particles, rebuild those two scenes in CapCut from single clips: exactly 10 icons in scene 12, and the "50" in scene 08.

**Style block, paste at the start of every prompt:**
> Ultra-premium cinematic 3D CGI commercial, vertical 9:16. Black, polished metallic gold and silver palette. Unreal Engine 5 look, realistic PBR gold with sharp anisotropic reflections, volumetric light rays, shallow depth of field, floating golden dust particles, smooth camera motion, 24 fps. No text, no letters, no numbers, no logos, no watermarks.

**Negative prompt, where supported:** `text, letters, numbers, logo, watermark, subtitles, cartoon, flat 2D, low quality, distorted hands, extra fingers, blurry, stock footage`

### Scene 01 — Low followers (0.00–3.20, generate 4 s)
[Style block] A dim, moody room lit only by a phone screen. Extreme close-up on a hand holding a smartphone showing a social media profile page with a few small grey avatar icons and an empty, dim counter panel. A cold desaturated blue-grey tone with only a hint of gold at the edges. Slow push-in toward the screen.
- **Camera:** slow dolly-in, slight handheld drift.
- **Animation:** the grey follower icons flicker faintly. In CapCut, overlay a low follower count (for example "128") that ticks up at ≈2.6.

### Scene 02 — Low likes (3.20–3.95, generate 3 s)
[Style block] Macro shot of three glass-and-dull-gold 3D heart icons floating in a dark void, hairline cracks across them, dim and nearly unlit. One heart slowly pulses faintly. Cool, desaturated.
- **Camera:** quick push-in, shallow depth of field.
- **Animation:** hearts bob slightly. Overlay a low likes counter in CapCut at ≈3.54.

### Scene 03 — Low views (3.95–6.50, generate 4 s)
[Style block] A large floating 3D video-player screen in a dark void, showing only a still dim thumbnail with a play triangle and a stat panel with a flat, drooping line graph. A single dim spotlight. Mood is quiet and discouraging.
- **Camera:** slow orbit left, easing into a push-in.
- **Animation:** the graph line slumps downward at ≈4.5. Overlay a low views counter at ≈4.1.

### Scene 04 — Worried creator (6.50–10.30, generate 5 s)
[Style block] A stylized 3D animated creator (generic, non-photoreal, no real person) sits at a desk in a dark room, staring at a phone with worry. Brows furrowed, a slight head shake, a hand rubbing the neck. The phone's glow is the only light. Slow push-in to the face. The screen glare fades to near black by the end.
- **Camera:** slow dolly-in to a medium close-up, shallow depth of field.
- **Animation:** subtle breathing, a nervous glance, shoulders dropping at ≈8.8.

### Scene 05 — "Do not worry": golden world (10.30–13.60, generate 5 s)
[Style block] Start in near-total darkness. A thin vertical line of gold light splits open into a swirling golden portal at the center of frame. The dark room dissolves outward from the portal into a vast futuristic golden world: gleaming gold architecture, floating light rings, warm volumetric god-rays and a radiant horizon. The camera rushes forward through the portal.
- **Camera:** static in the dark through ≈11.4, then a fast forward dolly through the portal at ≈11.9 and a glide into the golden world.
- **Animation:** the portal expands from a line to a ring, then a light burst. The scene flips from dark and cold to bright and warm.
- **Sync:** the portal opens at ≈11.92 on "अब चिन्ता".

### Scene 06 — Logo reveal setting (13.60–15.90, generate 3 s)
[Style block] A dark, glossy black stage with a single circular void in the center ringed by thin gold light. A wave of golden light sweeps across the surface and golden sparks drift upward. Leave the center clear for the logo overlay.
- **Camera:** slow push-in, with a lens flare gliding across at ≈14.15.
- **CapCut:** composite your logo here (see section 6).

### Scene 07 — Golden gift box (15.90–18.20, generate 3 s)
[Style block] A large, ornate polished-gold gift box with a black satin ribbon sits on a reflective black floor in a spotlight. The lid lifts and swings open, releasing a spectacular burst of golden light beams, sparkles and floating golden ribbon streamers into the air.
- **Camera:** low-angle hero shot, a slow orbit, then a fast push-in as the lid opens.
- **Animation:** the lid pops at ≈16.8, with the burst peaking ≈17.4–17.9. Keep the box interior glowing with gold light and no visible text.

### Scene 08 — 50 golden particles forming 50 (18.20–20.30, generate 3 s)
[Style block] Glowing golden particles (spheres of molten light) swirl in a vortex in a dark space, then converge and settle into the shape of a large two-digit number in the center of frame. Leave the digits blank, because the number is composited in CapCut.
- **Camera:** pull-back reveal as the particles settle.
- **CapCut recommendation:** use this clip as the swirl, then add the real "50" text with a gold gradient and a particle trail. Count the particles you place if you want exactly 50.

### Scene 09 — First video on a phone, rising into a spotlight (20.30–22.90, generate 4 s)
[Style block] A sleek smartphone floats in the golden world. Its screen plays an abstract glowing video, with a play button animating into motion. At the midpoint the phone lifts upward on a column of golden light into a dramatic overhead spotlight, with sparkles, haze and a gold lens flare.
- **Camera:** medium shot, a slow tilt up following the phone.
- **Animation:** the screen plays from ≈20.4. The rise starts ≈21.56 and the phone settles in the spotlight ≈22.5.

### Scene 10 — The 4 steps teaser (22.90–25.00, generate 3 s)
[Style block] Four tall polished-gold pedestals in a row on a black reflective floor. Each lights up in sequence from left to right, with a golden beam shooting up from each. No icons or text yet.
- **Camera:** slow lateral dolly.
- **Animation:** pedestal 1 flares last and brightest, setting up the heart.

### Scene 11 — Golden heart (25.00–27.10, generate 3 s)
[Style block] A big, glossy 3D golden heart floats in the center, pulsing like a heartbeat, with a soft golden glow rippling outward with each beat. Golden sparkles burst out on the second pulse.
- **Camera:** slight push-in on each beat.
- **Animation:** beat one ≈25.6, beat two ≈25.9 (when "Like" lands), burst ≈26.2.

### Scene 12 — Mention 10 friends (27.10–29.10, generate 3 s)
[Style block] Round gold-ringed profile-picture placeholders pop into a grid one at a time, on a dark glossy background. Each avatar is a neutral generic silhouette and each pops with a tiny spark.
- **Rule:** if the generator will not give you exactly 10, build this in CapCut. Duplicate one avatar clip 10 times, stagger them every ≈0.15 s from ≈27.40, and add a gold "@" badge at ≈28.15.
- **Camera:** gentle push-in.

### Scene 13 — Repost (29.10–32.00, generate 4 s)
[Style block] A smartphone floats upright while a glowing gold 3D circular-arrows repost symbol orbits it, rotating around the phone in a smooth ring with a golden light trail. The ring speeds up and then pulses.
- **Camera:** a 180° orbit around the phone, easing into a slow push-in.
- **Animation:** one full rotation per ≈1.5 s, with the speed peaking at ≈30.47.

### Scene 14 — Follow button (32.00–34.70, generate 3 s)
[Style block] An official-page screen in a dark UI. An elegant gold "Follow" button with a metallic bevel pulses softly. A finger-tap ripple presses it and it flips to a golden check state, with a spark burst around it. Leave all labels blank, because labels are added in CapCut.
- **Camera:** close-up, then a micro push-in on the press.
- **Animation:** the press lands at ≈33.35 on "Follow".

### Scene 15 — "50 selected" and DM notification (34.70–38.70, generate 5 s)
[Style block] A golden badge or medal glows over the dark background (the digits are added in CapCut), then the camera pans to a smartphone. A message notification banner slides in from the top with a soft golden glow, the phone buzzing slightly, and a gold chat bubble icon pops out.
- **Camera:** a slow pan from the badge to the phone, then a push-in on the notification.
- **Animation:** the banner arrives at ≈36.4 on "DM".

### Scene 16 — Final logo reveal (38.70–43.00, generate 5 s)
[Style block] A cinematic finale. In a dark void, a ring of golden light blooms and expands, light rays sweep and a metallic shine passes across a clear central area, with gold dust swirling. Leave the center empty, because the real logo is composited in CapCut. The shot ends with a slow, subtle push-in and the light settling.
- **Camera:** a slow, majestic push-in with a faint lens flare at ≈38.95.
- **Sync:** the burst hits ≈38.95 on "NEXORA", and the glow eases through ≈39.83 on "Upgrade".

---

## 4. Camera movement summary

| Scenes | Movement | Feel |
|---|---|---|
| 01–04 | Slow dollies and push-ins, slight handheld drift | Tense, closing in |
| 05 | Static, then a fast forward rush through the portal | Release |
| 06–09 | Smooth orbits, low-angle hero shots, tilt-ups | Premium, empowering |
| 10–15 | Short lateral dollies and push-ins timed to beats | Fast and clear |
| 16 | Majestic slow push-in | Final authority |

Add a subtle zoom punch of 105–110% in CapCut on each key trigger: ≈2.63, 3.54, 4.08, 14.15, 16.19, 25.82, 33.35, 36.48 and 38.95.

---

## 5. Sound effects and music (suggested; all times ≈)

**Music**
- **0.00–11.40:** a low, tense minor ambient drone with a sparse pulse. Keep it quiet.
- **11.40–11.92:** a reverse-cymbal riser and a sudden pull-back to near silence.
- **11.92 onward:** an uplifting, cinematic-gold track (orchestral hits, shimmering synths, a clean 4/4 beat), building to a finale.
- **Ducking:** keep the music about −18 to −22 dB under the voice, rising to about −12 dB in the pauses and at the final logo. The voiceover must stay clearly audible.

**SFX**

| Time | Event | SFX |
|---|---|---|
| 2.63 | Followers counter | Dull digital tick |
| 3.54 | Likes counter | Soft glassy tick |
| 4.08 | Views counter | Hollow tick |
| 4.53 | Graph droops | Descending tone |
| 8.83 | Worried face | Low heartbeat swell |
| 11.40–11.92 | Pre-portal | Riser into a vacuum silence |
| 11.92 | **Golden portal** | Whoosh plus a deep impact |
| 12.20 | Golden world | Shimmer and a bright choir pad |
| 14.15 | **Logo reveal** | Metallic sting, light-sweep shimmer, sub-bass hit |
| 16.80 | Gift box opens | Latch click, a magical burst and a chime |
| 18.85–20.00 | 50 particles | Swirling rise, then a bright "ding" as the number locks |
| 20.40 | Video plays | Soft UI tap |
| 21.56 | Phone rises | Rising whoosh and a spotlight hum |
| 22.97–24.60 | Pedestals | Four rising tones |
| 25.60 / 25.90 | **Heart** | Two soft heartbeat thumps, then a sparkle |
| 27.40–28.90 | **10 profile icons** | 10 pop ticks, pitched slightly higher each time |
| 28.15 | @ badge | Short chime |
| 29.90–31.60 | **Repost** | Circular whoosh loops, a swish on each rotation |
| 33.35 | **Follow click** | Crisp button click plus a bright "success" ding |
| 36.40 | **Message notification** | Phone buzz and a notification chime |
| 38.95 | **Final logo** | Big cinematic hit and a long shimmering tail to 43.00 |

---

## 6. CapCut assembly

### 6.1 Project setup
1. New project, ratio **9:16**, canvas **1080 × 1920**, frame rate **30 fps**.
2. Import `bf1d403d-NEXORA.mp3` (your voiceover) and place it on the main audio track at **0:00**. Do not trim, speed-change, denoise or re-export it. Leave its volume at 100%.
3. Lock the audio track once placed, so it can't be nudged.
4. Add **timeline markers** (M key) at the segment starts and ends: 0.00, 5.53, 6.93, 10.03, 11.40, 13.34, 13.74, 17.99, 18.34, 24.61, 25.05, 26.91, 27.26, 28.90, 29.24, 31.79, 32.07, 34.52, 34.88, 38.50, 38.95, 42.70, 43.00. These are measured.
5. Add a second set of markers (a different color) at the **≈ trigger times** from section 1. Treat them as adjustable.

### 6.2 Placing the scenes
1. Put the 16 generated clips on the main video track in order and trim each to the **Time** column in section 2. The scenes are contiguous and must total exactly 43.00 s.
2. Zoom the timeline in and scrub the voiceover waveform at each trigger. If the word lands earlier or later than the ≈ estimate, **move the visual to match the audio**, not the other way round. This pass is what turns the estimate into real sync.
3. Add the transitions from the "Transition out" column. Keep them to 0.2–0.4 s: Dip to Black (03→04), Flash / Glow for the golden cuts, and Zoom or Push for the rest.

### 6.3 Your logo (scenes 06 and 16)
1. Place `assets/NEXORA_logo.png` on an overlay track above the clip. It is a 1254 × 1254 badge on a black background.
2. Set **Blend mode: Screen** (Basic > Blend) so the black drops out cleanly and the glowing ring blends into the scene. If your version has no Screen, place the clip over a black base layer instead.
3. Scale the badge to about **900–1000 px wide**, centered slightly above the vertical middle (at about y = 800–900 on the 1920 canvas).
4. **Animation:** Scene 06 uses a Zoom In / Fade In of 0.4 s starting at **14.15**, with a short light sweep. Scene 16 uses a bigger Zoom In with a glow starting at **38.95**, held to 43.00, and a fade to black over the last 0.3 s.
5. Do not recolor, crop, stretch or redraw the logo. Use only scale, position, opacity and glow.

### 6.4 Counters and numbers (built in CapCut, not AI)
- Scenes 01–03: three small gold-on-dark text overlays for the low follower, like and view counters.
- Scene 08: the "50" as large gold gradient text, with a particle-trail sticker or overlay behind it.
- Scene 12: **exactly 10** avatar overlays, each starting ≈0.15 s after the one before from ≈27.40. Count them on the timeline.
- Scene 15: the "50" badge text at ≈35.5.

### 6.5 Subtitles
1. Open **Text > Captions > Local captions (Import)** and choose `subtitles/nexora_ne_plain.srt` (20 cues).
2. **Font:** CapCut's built-in fonts may not support Devanagari. Install a Nepali-capable font (for example **Noto Sans Devanagari** or **Mukta**) on your system, restart CapCut and pick it. Preview the whole video and check that the conjuncts and diacritics render (for example "दिँदैछौँ", "चिन्तित", "मात्रै").
3. **Style:** white text, size about 56–64, a thin soft shadow or outline for contrast, centered, placed at about **70–75% down the frame** (roughly y = 1400–1450). That keeps it clear of the phone UI zones at the bottom.
4. **Gold keywords:** use the gold color `#FFC93C` (or a metallic gradient `#FFD76A` to `#B8860B`) on the keywords. If the import keeps the `<font>` tags from `nexora_ne_gold_tags.srt`, use that file instead. If your version drops the tags, select the keyword inside each caption and color it by hand, or split the cue into two text layers.
   Keywords per segment: Followers, Likes, Views, कम · Views, चिन्तित · चिन्ता नगर्नुहोस् · NEXORA, FREE PROMOTION CAMPAIGN · ५०, Free, Video, Promote · Like · १०, Mention · Repost · NEXORA, Follow · ५०, DM · NEXORA, Upgrade Your Digital Life.
5. The SRT cue boundaries inside a segment are estimates. The segment boundaries are measured. If a cue is clearly early or late against the voice, drag its edge.
6. The SRT has no cue for the breaths at 6.08 and 10.60.

### 6.6 Audio mix
1. Add a music track below the voiceover. Use the ducking plan in section 5 (about −18 to −22 dB under speech). CapCut's **Auto-ducking / Voice enhance for music** can help, but check by ear.
2. Place each SFX on its own track at the times in section 5. Keep SFX peaking about 6–10 dB under the voice.
3. Fade the music out over the last second, finishing on the logo hit.

### 6.7 Export settings
- **Resolution:** 1080p (1080 × 1920), **frame rate** 30 fps, **format** MP4, **codec** H.264. Choose the highest bitrate option.
- **Audio:** AAC, 44.1 kHz or higher.
- **Length check:** the exported file should be **43.00 s**, matching the voiceover with nothing trimmed. If it is not, check for a stray gap on the main track.
- **Quick checks before you export:**
  1. The logo is the original artwork.
  2. The voiceover is audible over the music at every point.
  3. Every spoken keyword has its visual within about ±0.3 s.
  4. Scene 12 has exactly 10 avatars.

---

## 7. What I need from you to tighten it

- A listen at **6.08 s, 10.60 s and ≈22.97 s**, to confirm the mapping notes in section 0.
- If the sync is off anywhere after your first pass in CapCut, give me the real times you hear and I'll re-run `tools/gen_timing.py` and update the SRTs.

---

## 8. 2D animatic (built)

`output/nexora_animatic.mp4` is a 1080×1920, 30 fps, 43.00 s motion-graphics animatic. It is **not** 3D CGI. It is a timing and layout reference for the real edit.
- `output/nexora_animatic.mp4` has your voiceover plus a synthesized music and SFX bed, ducked under the voice.
- `output/nexora_animatic_voice_only.mp4` has the same video with only your voiceover.
- Rebuild with `tools/build_animatic.sh <path to NEXORA.mp3>`.
- The voiceover is mixed at unity gain with no EQ, trim or speed change. MP4 needs AAC, so the MP3 is re-encoded once at 192 kbps and is not bit-identical.
- Visual cut points use the measured segment boundaries. Trigger moments (counters, the 10 icons, the Follow press and so on) use the ≈ estimates from section 1.
- The 50 particles are exactly 50, and the profile icons are exactly 10 (one every 0.15 s from 27.40 s).
