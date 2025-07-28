import yt_dlp

# Playlist URL
playlist_url = 'https://www.youtube.com/playlist?list=PLDtG156FV00AxYp6Q4ya0BPd-GQe6GcT2'

# Cấu hình tải về
ydl_opts = {
    'format': 'bv[height<=1080]+ba/b[height<=1080]/best',  # ưu tiên video 1080p + audio
    'outtmpl': 'downloads/%(playlist_index)s - %(title)s.%(ext)s',  # đường dẫn và tên file
    'merge_output_format': 'mp4',  # gộp audio+video thành mp4
    'noplaylist': False,  # tải toàn bộ playlist
    'quiet': False,  # hiện thông tin chi tiết khi chạy
    'ignoreerrors': True,  # bỏ qua lỗi
    'postprocessors': [
        {
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',  # đảm bảo video ra là mp4
        }
    ],
}

# Thực thi tải video
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([playlist_url])
