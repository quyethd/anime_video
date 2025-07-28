import os
from moviepy.editor import VideoFileClip
from moviepy.video.fx.resize import resize
from moviepy.video.fx.crop import crop

# Cấu hình đường dẫn
input_folder = r"D:\4_AI\AnimeGANv3\output\hanu"
output_folder = r"D:\4_AI\AnimeGANv3\output\hanu_new"

os.makedirs(output_folder, exist_ok=True)

# Thông số xử lý
top_crop = 150
bottom_crop = 150
start_trim = 0.5
end_trim = 3.5
tiktok_width = 1080
tiktok_height = 1920
tiktok_ratio = 9 / 16

for filename in os.listdir(input_folder):
    if filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        print(f"🎬 Đang xử lý: {filename}")
        try:
            clip = VideoFileClip(input_path)
            duration = clip.duration

            if duration <= (start_trim + end_trim):
                print(f"⚠️ Bỏ qua {filename} vì quá ngắn ({duration:.2f}s)")
                continue

            # Cắt thời gian
            trimmed = clip.subclip(start_trim, duration - end_trim)

            # Cắt phần trên/dưới
            cropped = trimmed.crop(x1=0, y1=top_crop, x2=clip.w, y2=clip.h - bottom_crop)

            # Resize + pad để đạt 1080x1920 (9:16)
            cropped_ratio = cropped.w / cropped.h
            if abs(cropped_ratio - tiktok_ratio) > 0.01:
                # Resize chiều cao trước
                resized = resize(cropped, height=tiktok_height)

                # Nếu rộng quá, crop ngang
                if resized.w > tiktok_width:
                    x_center = resized.w // 2
                    final = crop(resized, x1=x_center - tiktok_width // 2, x2=x_center + tiktok_width // 2)
                else:
                    # Nếu chưa đủ rộng, pad viền
                    final = resized.on_color(size=(tiktok_width, tiktok_height), color=(0, 0, 0), col_opacity=1)
            else:
                # Nếu đã đúng tỷ lệ, chỉ resize
                final = resize(cropped, width=tiktok_width, height=tiktok_height)

            # Xuất video
            final.write_videofile(output_path, codec="libx264", audio_codec="aac", bitrate="2000k", fps=30)
            print(f"✅ Đã lưu: {output_path}")

        except Exception as e:
            print(f"❌ Lỗi với {filename}: {e}")
