from pytube import YouTube
import os
import re

# Hàm làm sạch tiêu đề file
def clean_filename(s):
    return re.sub(r'[\\/*?:"<>|]', "", s)

# Link video YouTube
video_url = "https://www.youtube.com/watch?v=cZymq3N5a5w"  # Thay VIDEO_ID bằng ID video của bạn
yt = YouTube(video_url)

# Chọn stream có độ phân giải cao nhất, nếu không có chọn stream khác
try:
    stream = yt.streams.get_highest_resolution()  # Chọn video có độ phân giải cao nhất
except Exception as e:
    print(f"⚠️ Lỗi tải video: {e}. Đang thử tải video với stream khác...")
    # Thử tải video với stream có âm thanh và video cùng một lúc
    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()

# Tạo thư mục lưu video nếu chưa có
output_folder = "downloaded_videos"
os.makedirs(output_folder, exist_ok=True)

# Lấy tiêu đề video và làm sạch tên file
title = clean_filename(yt.title)

# Tải video
print(f"⬇️ Đang tải: {title}")
stream.download(output_path=output_folder, filename=f"{title}.mp4")

print("✅ Đã tải xong video.")
