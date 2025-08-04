from moviepy.editor import VideoFileClip
import numpy as np
import cv2
import os

# Thư mục chứa các video nguồn
input_folder = r"D:\4_AI\AnimeGANv3\output\Minecraft"

# Thư mục đích chứa video đã làm mờ
output_folder = r"D:\4_AI\AnimeGANv3\output\Minecraft_blur"
os.makedirs(output_folder, exist_ok=True)  # Tạo thư mục nếu chưa có

# Thiết lập vùng làm mờ
blur_y = 0           # Khoảng cách từ đỉnh
blur_height = 25      # Chiều cao vùng làm mờ
margin_x = 250        # Lề trái/phải
blur_strength = (65, 65)  # Độ mờ (GaussianBlur)

def apply_blur_strip(frame, w, h):
    blurred_frame = frame.copy()
    blur_x1 = margin_x
    blur_x2 = w - margin_x
    strip = frame[blur_y:blur_y+blur_height, blur_x1:blur_x2]
    blurred_strip = cv2.GaussianBlur(strip, blur_strength, 0)
    blurred_frame[blur_y:blur_y+blur_height, blur_x1:blur_x2] = blurred_strip
    return blurred_frame

for filename in os.listdir(input_folder):
    if filename.lower().endswith(".mp4"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"{filename}")
        
        print(f"▶️ Đang xử lý: {filename}")
        try:
            clip = VideoFileClip(input_path)
            w, h = clip.size
            
            blurred_clip = clip.fl_image(lambda frame: apply_blur_strip(frame, w, h))
            blurred_clip.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")
            print(f"✅ Đã lưu: {output_path}\n")
        except Exception as e:
            print(f"❌ Lỗi với {filename}: {e}\n")
