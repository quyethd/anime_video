import os
from moviepy.editor import VideoFileClip

# Đường dẫn thư mục chứa video đầu vào
input_folder = r"D:\4_AI\AnimeGANv3\downloaded_videos"
# Đường dẫn thư mục lưu file mp3 đầu ra
output_folder = r"D:\4_AI\AnimeGANv3\output\results"

# Tạo thư mục đầu ra nếu chưa tồn tại
os.makedirs(output_folder, exist_ok=True)

# Duyệt qua tất cả các file trong thư mục
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".mp4"):
        video_path = os.path.join(input_folder, filename)
        audio_filename = os.path.splitext(filename)[0] + ".mp3"
        audio_path = os.path.join(output_folder, audio_filename)

        try:
            print(f"🔄 Đang xử lý: {filename}")
            video = VideoFileClip(video_path)
            audio = video.audio

            if audio:
                audio.write_audiofile(audio_path)
                print(f"✅ Đã lưu: {audio_path}")
                audio.close()
            else:
                print(f"⚠️ Video không có audio: {filename}")

            video.close()

        except Exception as e:
            print(f"❌ Lỗi với {filename}: {e}")
