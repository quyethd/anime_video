import os
import random
import pygame
from moviepy.editor import VideoFileClip, clips_array, CompositeVideoClip, ImageClip

# 🔤 Khởi tạo Pygame để render text
pygame.init()

# ✅ Danh sách text mở đầu
text_list = [
    "Bạn chọn ai?", "Real vs Anime – Ai nhảy cuốn hơn?", "So kè từng bước nhảy!",
    "2 thế giới – 1 trend!", "Người thật hay nhân vật anime chất hơn?", "Ai nhảy giống idol hơn?",
    "Đối đầu không khoan nhượng!", "Ai làm bạn phải xem lại 3 lần?", "Đọ dáng cực gắt",
    "Tưởng tượng vs thực tế", "Pick your side!", "Ai làm bạn thả tim?", "So sánh không hồi kết!",
    "Người thật liệu có thua anime?", "Vũ đạo đỉnh cao – bạn vote ai?", "Động tác nào mượt hơn?",
    "Ai đang lên trend đây?", "Ai hút mắt hơn?", "Thế giới thật vs thế giới ảo!", "Vibe ai chất hơn?",
    "Cú xoay nào chất hơn?", "Bước nhảy nào viral hơn?", "Ai khiến bạn replay?", "So kè từng frame!",
    "Không thể rời mắt!", "Bạn thích kiểu nào hơn?", "So với idol bạn sẽ chọn?",
    "Đây là nhảy hay hóa phép?", "Như trong mơ hay đời thật?", "Vừa cute vừa cháy!",
    "Bạn pick real hay anime?", "Combo thần sầu!", "Chuyển động nào mượt hơn?",
    "Chọn trong 3 giây!", "Khó chọn thật sự ?", "Chọn 1 bên, đừng do dự!", "Trend này ai thắng?",
    "2 phiên bản – 1 linh hồn", "Bạn nghiêng về ai?", "Không phải ai cũng làm được!",
    "Động tác đỉnh của chóp!", "Cảnh này bạn thích bên nào?", "Khớp đến từng mili giây!",
    "Visual ai ăn điểm hơn?", "Ai khiến bạn phải Wow?", "Sánh ngang idol Nhật?", "Mlem nhất hôm nay?",
    "Bạn vote cho ai?", "Tưởng tượng vs hiện thực!", "So kè nhịp nhàng đến từng bước!"
]

# 🔍 Thư mục
left_folder = r"D:\4_AI\AnimeGANv3\output\phoid_oxinh"
right_folder = r"D:\4_AI\AnimeGANv3\downloads\phoid_oxinh"
output_folder = r"D:\4_AI\AnimeGANv3\output\phoid_oxinh_merge"
font_path = r"D:\4_AI\AnimeGANv3\font\NotoSans-VariableFont_wdth,wght.ttf"
os.makedirs(output_folder, exist_ok=True)

def render_text_to_image(text, font_path, font_size=65):
    """Tạo ảnh từ text bằng Pygame với màu và hiệu ứng ngẫu nhiên (trả về đường dẫn ảnh tạm)."""

    # 🎨 Danh sách màu dễ nhìn trên nền trắng
    good_colors = [
        (255, 255, 0),    # vàng
        (0, 255, 255),    # cyan
        (255, 100, 0),    # cam
        (255, 0, 127),    # hồng
        (0, 255, 0),      # xanh lá
        (0, 128, 255),    # xanh da trời
        (255, 50, 50),    # đỏ nhạt
    ]
    text_color = random.choice(good_colors)
    outline_color = (0, 0, 0)  # màu viền: đen

    font = pygame.font.Font(font_path, font_size)

    # ✨ Tạo surface chữ có outline
    text_surface = font.render(text, True, text_color)
    w, h = text_surface.get_size()

    outline_surface = pygame.Surface((w + 4, h + 4), pygame.SRCALPHA)

    # Vẽ outline bằng cách vẽ chữ nhiều lần lệch vị trí
    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:
            if dx != 0 or dy != 0:
                offset_surface = font.render(text, True, outline_color)
                outline_surface.blit(offset_surface, (2 + dx, 2 + dy))

    # Vẽ lớp chính giữa (chữ màu chính)
    outline_surface.blit(text_surface, (2, 2))

    # Lưu ảnh tạm
    temp_path = f"temp_text_{random.randint(0, 999999)}.png"
    pygame.image.save(outline_surface, temp_path)
    return temp_path

for filename in os.listdir(left_folder):
    if filename.endswith(".mp4"):
        left_path = os.path.join(left_folder, filename)
        right_path = os.path.join(right_folder, filename)

        if not os.path.exists(right_path):
            print(f"❌ Không tìm thấy video anime tương ứng: {filename}")
            continue

        try:
            print(f"\n🔧 Đang xử lý: {filename}")
            left_clip = VideoFileClip(left_path)
            right_clip = VideoFileClip(right_path).resize(height=left_clip.h)

            combined_clip = clips_array([[left_clip, right_clip]])
            combined_clip = combined_clip.set_audio(left_clip.audio)

            # 📝 Text mở đầu
            start_text = random.choice(text_list)
            print(f"📝 Tạo text mở đầu: {start_text}")
            img_start = render_text_to_image(start_text, font_path, font_size=75)
            txt_start_clip = (
                ImageClip(img_start)
                .set_duration(3)
                .set_position(("center", "top"))
                .fadein(0.5)
                .fadeout(0.5)
            )

            # 📝 Text kết thúc
            print("📝 Tạo text kết thúc: Bạn chọn ai? Comment nhé")
            img_end = render_text_to_image("Bạn chọn ai? Comment nhé", font_path, font_size=75)
            txt_end_clip = (
                ImageClip(img_end)
                .set_duration(3)
                .set_position(("center", "bottom"))
                .fadein(0.5)
                .fadeout(0.5)
                .set_start(combined_clip.duration - 3)
            )

            # 🧩 Kết hợp video và text
            final_clip = CompositeVideoClip([combined_clip, txt_start_clip, txt_end_clip])

            output_path = os.path.join(output_folder, filename)
            print(f"💾 Xuất video: {output_path}")
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

            # 🧹 Dọn dẹp
            left_clip.close()
            right_clip.close()
            combined_clip.close()
            final_clip.close()
            os.remove(img_start)
            os.remove(img_end)

        except Exception as e:
            print(f"⚠️ Lỗi khi xử lý {filename}: {e}")
