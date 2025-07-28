import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from youtubesearchpython import VideosSearch
import yt_dlp

# Cấu hình chính
MAX_VIDEOS = 100
QUERIES = [
    "anime Việt Sub",
    "anime lồng tiếng",
    "hoạt hình Việt Nam",
    "hoạt hình thiếu nhi",
    "anime hài hước",
    "anime meme clip",
    "hoạt hình hài TikTok",
    "anime trending 2025",
    "anime biểu cảm hài",
    "anime funny moments",
    "anime clip viral",
    "hoạt hình đáng yêu",
    "phim anime học đường",
    "anime cute compilation",
    "anime reaction TikTok",
    "anime meme ngắn",
    "hoạt hình TikTok hot",
    "anime shorts Việt hóa",
    "anime top view TikTok",
    "anime siêu hài 2025",
    "anime meme Việt Nam",
    "truyện tranh chuyển thể hoạt hình",
    "hoạt hình TikTok trend",
    "anime hài TikTok",
    "anime chế meme",
    "anime edit hài",
    "top hoạt hình TikTok",
    "anime trẻ em hài hước",
    "hoạt hình cổ tích remix",
    "anime compilation viral"
]
DURATION_LIMIT = 30  # chỉ lấy video dưới 30 giây
MIN_VIEWS = 1_000_000  # chỉ lấy video trên 1 triệu lượt xem
OUTPUT_DIR = "downloads/shorts_funny"
MAX_WORKERS = 4

# Khởi tạo thư mục và biến toàn cục
os.makedirs(OUTPUT_DIR, exist_ok=True)
video_links = set()
downloaded_links = set()
video_links_lock = threading.Lock()

def parse_views(view_text):
    view_text = view_text.lower().replace('views', '').strip()
    if 'k' in view_text:
        return float(view_text.replace('k', '')) * 1_000
    elif 'm' in view_text:
        return float(view_text.replace('m', '')) * 1_000_000
    return float(view_text.replace(',', ''))

def parse_duration(duration_text):
    parts = duration_text.split(':')
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 1:
        return int(parts[0])
    return 9999

def has_audio_stream(url):
    try:
        ydl = yt_dlp.YoutubeDL({'quiet': True})
        info = ydl.extract_info(url, download=False)
        for fmt in info.get('formats', []):
            if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':
                return True
    except Exception:
        pass
    return False

def download_video(url):
    global downloaded_links
    if url in downloaded_links:
        return
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': f'{OUTPUT_DIR}/%(title).100s [%(id)s].%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': True,
        'noplaylist': True,
        'ignoreerrors': True,
        'postprocessors': [{'key': 'FFmpegMetadata'}],
    }
    if not has_audio_stream(url):
        print(f"⛔ Không có audio: {url}")
        return
    try:
        print(f"⬇️ Đang tải: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        with video_links_lock:
            downloaded_links.add(url)
            print(f"✅ Đã tải: {url} | Tổng: {len(downloaded_links)}/{MAX_VIDEOS}")
    except Exception as e:
        print(f"⚠️ Lỗi tải {url}: {e}")

def search_videos():
    print("🔍 Bắt đầu tìm video...")
    while len(downloaded_links) < MAX_VIDEOS:
        for query in QUERIES:
            try:
                search = VideosSearch(query, limit=50)
                results = search.result().get('result', [])
                for video in results:
                    try:
                        link = video['link']
                        views = parse_views(video['viewCount']['short'])
                        duration = parse_duration(video['duration'])
                        if views >= MIN_VIEWS and duration < DURATION_LIMIT:
                            with video_links_lock:
                                if link not in video_links and link not in downloaded_links:
                                    video_links.add(link)
                                    print(f"🎯 Tìm thấy: {len(video_links)} | Đã tải: {len(downloaded_links)}")
                    except:
                        continue
                time.sleep(1)
            except Exception as e:
                print(f"❌ Lỗi tìm kiếm với từ khóa '{query}': {e}")
                time.sleep(5)
            if len(downloaded_links) >= MAX_VIDEOS:
                break

def main():
    try:
        search_thread = threading.Thread(target=search_videos)
        search_thread.start()
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            while len(downloaded_links) < MAX_VIDEOS:
                with video_links_lock:
                    links_to_download = list(video_links - downloaded_links)
                for link in links_to_download:
                    executor.submit(download_video, link)
                time.sleep(5)
        search_thread.join()
        print(f"\n🎉 Đã tải xong {len(downloaded_links)} video.")
    except KeyboardInterrupt:
        print("\n⛔ Đã dừng bởi người dùng (Ctrl + C).")
        print(f"📦 Đã tải được {len(downloaded_links)} video trước khi thoát.")

if __name__ == "__main__":
    main()
