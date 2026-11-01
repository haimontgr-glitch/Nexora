#!/usr/bin/env bash
# Rebuilds output/nexora_animatic.mp4 (voice + music/SFX) and output/nexora_animatic_voice_only.mp4
# usage: tools/build_animatic.sh /path/to/NEXORA.mp3     (needs ffmpeg, python3, numpy, pillow with raqm, FreeSans font)
set -euo pipefail
A="$1"; R="$(cd "$(dirname "$0")/.." && pwd)"; mkdir -p "$R/output"; T="$(mktemp -d)"
python3 -I "$R/tools/animatic.py" "$R" "$T/v.mp4"
python3 -I "$R/tools/make_audio.py" "$A" "$T/bed.wav"
ffmpeg -y -loglevel error -i "$T/v.mp4" -i "$A" -i "$T/bed.wav" -filter_complex "[1:a][2:a]amix=inputs=2:normalize=0:duration=longest,alimiter=limit=0.97[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -t 43.0 "$R/output/nexora_animatic.mp4"
ffmpeg -y -loglevel error -i "$T/v.mp4" -i "$A" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -t 43.0 "$R/output/nexora_animatic_voice_only.mp4"
