import os
import subprocess

# Đường dẫn thư mục chứa video
input_dir = "1_Video"
output_dir = "output/results"
model_path = "deploy/AnimeGANv3_Hayao_36.onnx"

# Tạo thư mục output nếu chưa có
os.makedirs(output_dir, exist_ok=True)

# Lặp qua tất cả file trong thư mục
for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        input_path = os.path.join(input_dir, filename)
        name_without_ext = os.path.splitext(filename)[0]

        # Gọi lệnh chuyển video
        command = [
            "python", "tools/video2anime.py",
            "-i", input_path,
            "-o", output_dir,
            "-m", model_path
        ]
        print(f"Đang xử lý: {filename}")
        subprocess.run(command)
