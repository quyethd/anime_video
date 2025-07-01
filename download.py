from youtubesearchpython import VideosSearch
import yt_dlp
import time
import os

# ====== CẤU HÌNH ======
MAX_VIDEOS = 1000
QUERY = "Top Shorts funny of all time"
OUTPUT_DIR = "downloads/video"
DURATION_LIMIT = 30  # giây
MIN_VIEWS = 10_000_000

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ====== HÀM HỖ TRỢ ======
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
        return False
    return False


# ====== TÌM KIẾM VIDEO ĐỦ ĐIỀU KIỆN ======
qualified_links = []
search = VideosSearch(QUERY, limit=20)

print(f"🔍 Bắt đầu tìm video phù hợp (<{DURATION_LIMIT}s, ≥10tr view)...")

while len(qualified_links) < MAX_VIDEOS:
    results = search.result()
    for video in results['result']:
        try:
            views = parse_views(video['viewCount']['short'])
            duration = parse_duration(video['duration'])
            if views >= MIN_VIEWS and duration < DURATION_LIMIT:
                link = video['link']
                if link not in qualified_links:
                    qualified_links.append(link)
                    print(f"✔️  {link} | {views:.0f} views | {duration}s")
        except Exception:
            continue

    if not search.hasNextPage:
        break

    search.next()
    time.sleep(1)

print(f"\n🎯 Tổng số video đủ điều kiện: {len(qualified_links)}")


# ====== CẤU HÌNH TẢI VIDEO ======
ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
    'outtmpl': f'{OUTPUT_DIR}/%(title).100s [%(id)s].%(ext)s',
    'merge_output_format': 'mp4',
    'quiet': False,
    'noplaylist': True,
    'ignoreerrors': True,
    'postprocessors': [{
        'key': 'FFmpegMetadata'
    }],
}


# ====== TẢI VIDEO ======
print("\n📥 Bắt đầu tải video...")

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for i, url in enumerate(qualified_links[:MAX_VIDEOS], start=1):
        print(f"\n➡️ [{i}/{MAX_VIDEOS}] Tải: {url}")
        if has_audio_stream(url):
            try:
                ydl.download([url])
            except Exception as e:
                print(f"⚠️  Lỗi: {e}")
        else:
            print("⛔ Bỏ qua: không có audio")


print("\n✅ HOÀN TẤT.")
