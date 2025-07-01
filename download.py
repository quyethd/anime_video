from youtubesearchpython import VideosSearch
import yt_dlp
import os
import time

# === 1. Cấu hình ===
os.makedirs('downloads/video', exist_ok=True)

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

# === 2. Tìm video thỏa điều kiện (dưới 30s, > 10tr view) ===
search = VideosSearch("Top Shorts funny of all time", limit=20)
qualified_links = []

while len(qualified_links) < 100:
    results = search.result()
    for video in results['result']:
        try:
            views = parse_views(video['viewCount']['short'])
            duration = parse_duration(video['duration'])
            if views >= 10_000_000 and duration < 30:
                qualified_links.append(video['link'])
        except Exception:
            continue

    if not search.hasNextPage:
        break
    search.next()
    time.sleep(1)

qualified_links = list(dict.fromkeys(qualified_links))[:100]

# === 3. Cấu hình tải video có cả audio ===
video_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'outtmpl': 'downloads/video/%(title).80s.%(ext)s',
    'merge_output_format': 'mp4',
    'quiet': False,
    'noplaylist': True,
}

# === 4. Kiểm tra nếu video đã có audio → chỉ tải video đầy đủ ===
def has_audio_stream(url):
    try:
        ydl = yt_dlp.YoutubeDL({'quiet': True})
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        for fmt in formats:
            if fmt.get('vcodec', 'none') != 'none' and fmt.get('acodec', 'none') != 'none':
                return True
        return False
    except Exception as e:
        print(f"⚠️ Không kiểm tra được audio của {url}: {e}")
        return False

# === 5. Tải ===
print(f"🔍 Có {len(qualified_links)} video đạt yêu cầu (<30s, >10tr view).")

with yt_dlp.YoutubeDL(video_opts) as ydl:
    for url in qualified_links:
        print(f"\n📥 Đang xử lý: {url}")
        if has_audio_stream(url):
            print("✅ Video có audio. Đang tải...")
            try:
                ydl.download([url])
            except Exception as e:
                print(f"❌ Lỗi khi tải: {e}")
        else:
            print("⛔ Bỏ qua vì video không có audio.")
