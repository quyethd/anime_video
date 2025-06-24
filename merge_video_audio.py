import os
from moviepy.editor import VideoFileClip, AudioFileClip

# Thư mục đầu vào và đầu ra
input_folder = r"D:\3_AI\AnimeGANv3\1_video"
output_folder = os.path.join(input_folder, "output")

# Tạo thư mục output nếu chưa có
os.makedirs(output_folder, exist_ok=True)

# Duyệt tất cả các file video trong thư mục
for filename in os.listdir(input_folder):
    name, ext = os.path.splitext(filename)

    if ext.lower() == '.mp4':
        video_path = os.path.join(input_folder, filename)
        audio_path = os.path.join(input_folder, name + '.webm')

        # Kiểm tra nếu file audio tương ứng tồn tại
        if os.path.exists(audio_path):
            print(f"Ghép: {filename} + {name}.webm")

            # Load video và audio
            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)

            # Ghép audio vào video
            final = video.set_audio(audio)

            # Tên file xuất ra (giữ nguyên tên)
            output_path = os.path.join(output_folder, f"{name}.mp4")
            final.write_videofile(output_path, codec="libx264", audio_codec="aac")

print("✅ Hoàn tất ghép tất cả file!")
