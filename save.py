from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument("--headless")  # Chạy không mở cửa sổ trình duyệt
options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options)

search_url = "https://www.youtube.com/results?search_query=Top+Shorts+of+all+time"

print("🔍 Đang tải trang kết quả tìm kiếm...")
driver.get(search_url)
time.sleep(3)

# Cuộn xuống nhiều lần để load thêm video
for _ in range(10):
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2)

# Tìm video
videos = driver.find_elements(By.XPATH, '//ytd-video-renderer')

results = []
for v in videos:
    try:
        title_elem = v.find_element(By.ID, 'video-title')
        title = title_elem.get_attribute('title')
        url = title_elem.get_attribute('href')

        meta_line = v.find_element(By.ID, 'metadata-line').text
        if "views" in meta_line:
            views_text = meta_line.split("•")[0].strip()
        else:
            views_text = "N/A"

        duration_elem = v.find_element(By.CLASS_NAME, "ytd-thumbnail-overlay-time-status-renderer")
        duration_text = duration_elem.text.strip()
        duration_sec = 0

        if duration_text:
            parts = duration_text.split(":")
            if len(parts) == 2:
                duration_sec = int(parts[0]) * 60 + int(parts[1])
            elif len(parts) == 1:
                duration_sec = int(parts[0])

        if duration_sec < 60:
            results.append((title, views_text, url))

    except Exception as e:
        continue

driver.quit()

# Ghi ra file
with open("top_shorts_search_results.txt", "w", encoding="utf-8") as f:
    for i, (title, views, link) in enumerate(results, 1):
        f.write(f"{i}. {title} - {views} - {link}\n")

print(f"✅ Đã lưu {len(results)} video ngắn vào top_shorts_search_results.txt")
