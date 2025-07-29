import os
from moviepy.editor import VideoFileClip

# Cấu hình
input_folder = r"D:\4_AI\AnimeGANv3\output\phoid_oxinh_tiktok"

def is_shorts_format(clip):
    width, height = clip.size
    ratio = height / width
    duration = clip.duration
    fps = clip.fps

    return {
        "duration (s)": duration,
        "fps": fps,
        "resolution": f"{width}x{height}",
        "is_vertical": ratio > 1.3,
        "duration_valid": duration <= 120,
        "fps_valid": fps >= 24,
        "resolution_valid": width >= 720 and height >= 1280,
    }

for filename in os.listdir(input_folder):
    if filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
        filepath = os.path.join(input_folder, filename)
        try:
            clip = VideoFileClip(filepath)
            info = is_shorts_format(clip)

            print(f"\n🎞 Video: {filename}")
            for k, v in info.items():
                print(f"{k:20}: {v}")

            if all(info[k] for k in ["is_vertical", "duration_valid", "fps_valid", "resolution_valid"]):
                print("✅ Đây là video đạt chuẩn YouTube Shorts.\n")
            else:
                print("❌ Video KHÔNG đạt chuẩn Shorts.\n")

        except Exception as e:
            print(f"⚠️ Lỗi khi đọc {filename}: {e}")
