import os
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2

# ==== CẤU HÌNH ====
INPUT_DIR = r"D:\3_AI\anime_video\output\hanu_new"
OUTPUT_DIR = os.path.join(INPUT_DIR, "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_PATH = r"D:\3_AI\anime_video\font\NotoSans-VariableFont_wdth,wght.ttf"
TEXT = "PlayVerseVN"
TEXT_COLOR = (255, 255, 255, 255)
STROKE_COLOR = (0, 0, 0, 255)
STROKE_WIDTH = 3
MARGIN = 20
TEXT_SCALE = 0.05
BLUR_BORDER_WIDTH = 50

# ==== LÀM MỜ VIỀN ====
def blur_border(frame):
    h, w = frame.shape[:2]
    blurred = cv2.GaussianBlur(frame, (0, 0), sigmaX=15, sigmaY=15)

    mask = np.zeros((h, w), dtype=np.uint8)
    mask[:BLUR_BORDER_WIDTH, :] = 255
    mask[-BLUR_BORDER_WIDTH:, :] = 255
    mask[:, :BLUR_BORDER_WIDTH] = 255
    mask[:, -BLUR_BORDER_WIDTH:] = 255
    mask = cv2.GaussianBlur(mask, (21, 21), 0) / 255.0
    mask = mask[..., None]

    return (mask * blurred + (1 - mask) * frame).astype(np.uint8)

# ==== TẠO CLIP CHỮ ====
def make_text_clip(w, h, duration):
    fontsize = max(16, int(h * TEXT_SCALE))
    try:
        font = ImageFont.truetype(FONT_PATH, fontsize)
        # Tính kích thước chữ cho font TTF
        dummy = Image.new("RGBA", (10, 10))
        draw = ImageDraw.Draw(dummy)
        bbox = draw.textbbox((0, 0), TEXT, font=font, stroke_width=STROKE_WIDTH)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except Exception as e:
        print(f"[!] Không dùng được font TTF ({e}), dùng font mặc định")
        font = ImageFont.load_default()
        dummy = Image.new("RGBA", (10, 10))
        draw = ImageDraw.Draw(dummy)
        tw, th = draw.textsize(TEXT, font=font)  # Cách cũ cho font mặc định

    img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), TEXT, font=font, fill=TEXT_COLOR,
              stroke_width=STROKE_WIDTH, stroke_fill=STROKE_COLOR)

    return ImageClip(np.array(img)).set_position((w - tw - MARGIN, h - th - MARGIN)).set_duration(duration)


# ==== XỬ LÝ TỪNG VIDEO ====
def process_video(video_path):
    filename = os.path.basename(video_path)
    output_path = os.path.join(OUTPUT_DIR, filename)

    clip = VideoFileClip(video_path)
    processed_clip = clip.fl_image(blur_border)
    text_clip = make_text_clip(clip.w, clip.h, clip.duration)

    final_clip = CompositeVideoClip([processed_clip, text_clip])
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

# ==== CHẠY XỬ LÝ TOÀN BỘ ====
for file in os.listdir(INPUT_DIR):
    if file.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
        print(f"🔄 Đang xử lý: {file}")
        process_video(os.path.join(INPUT_DIR, file))

print("✅ Hoàn tất!")
