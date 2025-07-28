import os
from moviepy.editor import VideoFileClip

# Thư mục nguồn và đích
input_folder = r'D:\3_AI\anime_video\output\hanu'
output_folder = r'D:\3_AI\anime_video\output\hanu_new'

# Tạo thư mục đích nếu chưa có
os.makedirs(output_folder, exist_ok=True)

# Duyệt qua các file trong thư mục
for filename in os.listdir(input_folder):
    if filename.endswith('.mp4'):
        input_path = os.path.join(input_folder, filename)
        output_name = filename.replace('.mp4', '_cut.mp4')
        output_path = os.path.join(output_folder, output_name)

        try:
            clip = VideoFileClip(input_path)
            duration = clip.duration

            # Chỉ xử lý video dài hơn 4 giây
            if duration > 4:
                trimmed_clip = clip.subclip(1, duration - 3)
                trimmed_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
                print(f"✅ Đã xử lý: {output_name}")
            else:
                print(f"⚠️ Video quá ngắn, bỏ qua: {filename}")
        except Exception as e:
            print(f"❌ Lỗi với {filename}: {e}")
