import os
from moviepy.editor import VideoFileClip
from moviepy.video.fx.resize import resize
from moviepy.video.fx.crop import crop

# Cấu hình đường dẫn
input_folder = r"D:\4_AI\AnimeGANv3\output\Minecraft"
output_folder = r"D:\4_AI\AnimeGANv3\output\Minecraft_new"

os.makedirs(output_folder, exist_ok=True)

# Thông số xử lý
top_crop = 50
bottom_crop = 0

for filename in os.listdir(input_folder):
    if filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        print(f"🎬 Đang xử lý: {filename}")
        try:
            clip = VideoFileClip(input_path)
            duration = clip.duration

            # Cắt phần trên/dưới
            final = clip.crop(x1=0, y1=top_crop, x2=clip.w, y2=clip.h - bottom_crop)

            # Xuất video
            final.write_videofile(output_path, codec="libx264", audio_codec="aac", bitrate="2000k", fps=30)
            print(f"✅ Đã lưu: {output_path}")

        except Exception as e:
            print(f"❌ Lỗi với {filename}: {e}")
