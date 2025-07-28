import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# === 1. Cấu hình trình duyệt (headless) ===
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options)

# === 2. Mở trang reels ===
profile_url = "https://www.instagram.com/phoid_oxinh/reels/"
driver.get(profile_url)
time.sleep(5)

# === 3. Scroll để load thêm video ===
SCROLL_TIMES = 5
for _ in range(SCROLL_TIMES):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

# === 4. Thu thập các link Reels ===
reel_links = set()
anchors = driver.find_elements(By.TAG_NAME, "a")
for a in anchors:
    href = a.get_attribute("href")
    if href and "/reel/" in href:
        reel_links.add(href)

print(f"🔗 Tìm được {len(reel_links)} video Reels")

# === 5. Tạo thư mục lưu ===
output_folder = "downloaded_reels"
os.makedirs(output_folder, exist_ok=True)

# === 6. Truy cập từng link và tải video ===
for url in reel_links:
    try:
        driver.get(url)
        time.sleep(5)

        video_url = driver.find_element(By.TAG_NAME, "video").get_attribute("src")
        if video_url:
            print("▶️ Đang tải:", video_url)
            filename = url.rstrip("/").split("/")[-1] + ".mp4"
            response = requests.get(video_url, stream=True)
            with open(os.path.join(output_folder, filename), 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    f.write(chunk)
            print("✅ Đã lưu:", filename)
        else:
            print("❌ Không tìm thấy video tại:", url)
    except Exception as e:
        print("🚫 Lỗi:", e)

driver.quit()
