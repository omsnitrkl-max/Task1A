#!/usr/bin/env python3

import os
from script import analyze_video

# ==========================================
# BASE DIRECTORY
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# ==========================================
# VIDEO PATH
# ==========================================

video_path = os.path.join(
    BASE_DIR,
    "Test_videos",
    "arena_video_1.mp4"
)

# ==========================================
# RUN STUDENT SCRIPT
# ==========================================

result = analyze_video(video_path)

# ==========================================
# DISPLAY OUTPUT
# ==========================================

print("\n========== DETECTED OUTPUT ==========\n")

print(f"top_wall_hits    : {result['top_wall_hits']}")
print(f"bottom_wall_hits : {result['bottom_wall_hits']}")
print(f"left_wall_hits   : {result['left_wall_hits']}")
print(f"right_wall_hits  : {result['right_wall_hits']}")

print("\n=====================================\n")
