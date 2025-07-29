import os
import numpy as np
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from moviepy.video.fx.resize import resize
from PIL import Image, ImageFilter, ImageEnhance

# ======== Thư mục ============
input_folder = r"D:\4_AI\AnimeGANv3\output\phoid_oxinh_merge"
output_folder = r"D:\4_AI\AnimeGANv3\output\phoid_oxinh_tiktok"
os.makedirs(output_folder, exist_ok=True)

# ======== Kích thước chuẩn TikTok ============
tiktok_width = 1080
tiktok_height = 1920
tiktok_ratio = tiktok_width / tiktok_height


# ======== Hàm tạo nền mờ + tối đi ============
def make_blurred_background(clip):
    # Lấy frame đầu tiên
    frame = clip.get_frame(5)
    img = Image.fromarray(frame)

    # Resize nền sao cho phủ toàn khung TikTok
    img_ratio = img.width / img.height
    if img_ratio > tiktok_ratio:
        new_height = tiktok_height
        new_width = int(new_height * img_ratio)
    else:
        new_width = tiktok_width
        new_height = int(new_width / img_ratio)

    img = img.resize((new_width, new_height))

    # Làm mờ
    blurred = img.filter(ImageFilter.GaussianBlur(radius=15))

    # Giảm độ sáng (darken)
    enhancer = ImageEnhance.Brightness(blurred)
    darkened = enhancer.enhance(0.6)  # 0.6 = giảm 40% độ sáng

    # Cắt về đúng kích thước TikTok
    left = (darkened.width - tiktok_width) // 2
    top = (darkened.height - tiktok_height) // 2
    cropped = darkened.crop((left, top, left + tiktok_width, top + tiktok_height))

    # Chuyển về clip
    bg_array = np.array(cropped)
    bg_clip = ImageClip(bg_array).set_duration(clip.duration)
    return bg_clip


# ======== Xử lý từng video ============
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        print(f"🎬 Đang xử lý: {filename}")
        try:
            clip = VideoFileClip(input_path)
            duration = clip.duration

            # Tạo nền blur + darken
            bg = make_blurred_background(clip)

            # Resize foreground sao cho vừa màn (giữ nguyên nội dung)
            original_ratio = clip.w / clip.h
            if original_ratio > tiktok_ratio:
                fg = resize(clip, width=tiktok_width)
            else:
                fg = resize(clip, height=tiktok_height)

            fg = fg.set_position(("center", "center")).set_duration(duration)

            # Ghép nền và foreground
            final = CompositeVideoClip([bg, fg], size=(tiktok_width, tiktok_height))
            final = final.set_duration(duration)

            # Xuất video
            final.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                bitrate="3000k",
                fps=30,
                preset="medium"
            )

            print(f"✅ Đã lưu: {output_path}")

        except Exception as e:
            print(f"❌ Lỗi với {filename}: {e}")
