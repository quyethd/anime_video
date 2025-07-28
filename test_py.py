import os
import random
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"

from moviepy.editor import VideoFileClip, clips_array, TextClip, CompositeVideoClip
text_list = [
    "Bạn chọn ai?", "Real vs Anime – Ai nhảy cuốn hơn?", "So kè từng bước nhảy!",
    "2 thế giới – 1 trend!", "Người thật hay nhân vật anime chất hơn?", "Ai nhảy giống idol hơn?",
    "Đối đầu không khoan nhượng!", "Ai làm bạn phải xem lại 3 lần?", "Đọ dáng cực gắt 🔥",
    "Tưởng tượng vs thực tế 😱", "Pick your side!", "Ai làm bạn thả tim?", "So sánh không hồi kết!",
    "Người thật liệu có thua anime?", "Vũ đạo đỉnh cao – bạn vote ai?", "Động tác nào mượt hơn?",
    "Ai đang lên trend đây?", "Ai hút mắt hơn?", "Thế giới thật vs thế giới ảo!", "Vibe ai chất hơn?",
    "Cú xoay nào chất hơn?", "Bước nhảy nào viral hơn?", "Ai khiến bạn replay?", "So kè từng frame!",
    "Không thể rời mắt!", "Bạn thích kiểu nào hơn?", "So với idol bạn sẽ chọn?",
    "Đây là nhảy hay hóa phép?", "Như trong mơ hay đời thật?", "Vừa cute vừa cháy!",
    "Bạn pick real hay anime?", "Combo thần sầu!", "Chuyển động nào mượt hơn?",
    "Chọn trong 3 giây!", "Khó chọn thật sự 😳", "Chọn 1 bên, đừng do dự!", "Trend này ai thắng?",
    "2 phiên bản – 1 linh hồn", "Bạn nghiêng về ai?", "Không phải ai cũng làm được!",
    "Động tác đỉnh của chóp!", "Cảnh này bạn thích bên nào?", "Khớp đến từng mili giây!",
    "Visual ai ăn điểm hơn?", "Ai khiến bạn phải Wow?", "Sánh ngang idol Nhật?", "Mlem nhất hôm nay?",
    "Bạn vote cho ai?", "Tưởng tượng vs hiện thực!", "So kè nhịp nhàng đến từng bước!"
]

start_text = random.choice(text_list)
clip = (TextClip("Bạn chọn ai? 👉 Comment", fontsize=40, font="Arial", color="yellow",
                                        stroke_color="black", stroke_width=2, method="label")
                               .set_duration(3)
                               .set_position(("center", "bottom"))
                               .fadein(0.5)
                               .fadeout(0.5))
clip.write_videofile("test_textclip.mp4", fps=24)
