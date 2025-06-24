from googleapiclient.discovery import build
import isodate
import time

API_KEY = 'AIzaSyBqgbQSZhI8eIa761aUEgaIGf13SGgAWh8'
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_video_details(video_ids):
    request = youtube.videos().list(
        part='snippet,statistics,contentDetails',
        id=','.join(video_ids)
    )
    response = request.execute()
    videos = []
    for item in response['items']:
        duration_sec = isodate.parse_duration(item['contentDetails']['duration']).total_seconds()
        if duration_sec < 60:
            videos.append({
                'title': item['snippet']['title'],
                'videoId': item['id'],
                'views': int(item['statistics'].get('viewCount', 0))
            })
    return videos

def get_shorts_by_keyword(keyword, max_results=200):
    videos = []
    next_page_token = None

    while len(videos) < max_results:
        request = youtube.search().list(
            part='id',
            type='video',
            videoDuration='short',  # <4 phút
            maxResults=50,
            pageToken=next_page_token,
            q=keyword
        )
        response = request.execute()

        video_ids = [item['id']['videoId'] for item in response['items']]
        videos.extend(get_video_details(video_ids))

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

        time.sleep(1)  # tránh lỗi giới hạn tốc độ API

    return videos[:max_results]

def get_many_shorts(keywords, max_total=1000):
    all_videos = []
    seen_ids = set()

    for kw in keywords:
        print(f"Lấy video cho từ khóa: {kw}")
        videos = get_shorts_by_keyword(kw, max_results=200)
        for v in videos:
            if v['videoId'] not in seen_ids:
                all_videos.append(v)
                seen_ids.add(v['videoId'])

        if len(all_videos) >= max_total:
            break

    # Sắp xếp theo views giảm dần và cắt max_total
    all_videos.sort(key=lambda x: x['views'], reverse=True)
    return all_videos[:max_total]

def save_to_file(videos, filename='many_shorts_videos.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for idx, v in enumerate(videos, 1):
            f.write(f"{idx}. {v['title']} - {v['views']} views - https://youtu.be/{v['videoId']}\n")
    print(f"Saved {len(videos)} videos to {filename}")

if __name__ == '__main__':
    keywords = ['music', 'funny', 'gaming', 'news', 'viral', 'life', 'tech', 'sports', 'food', 'travel']
    videos = get_many_shorts(keywords, max_total=1000)
    save_to_file(videos)
