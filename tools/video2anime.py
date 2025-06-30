import argparse
import os
import cv2
from PIL import Image
from tqdm import tqdm
import numpy as np
import queue
import threading
import onnxruntime as ort
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip, ImageClip

# Xử lý Resampling cho các phiên bản Pillow khác nhau
try:
    resample_method = Image.Resampling.LANCZOS
except AttributeError:
    resample_method = Image.ANTIALIAS

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def parse_args():
    parser = argparse.ArgumentParser(description="AnimeGANv3 ONNX Video Cartoonizer")
    parser.add_argument('-i', '--input_video_path', type=str, required=True, help='Path to input video')
    parser.add_argument('-m', '--model_path', type=str, default='models/AnimeGANv3_Hayao_36.onnx', help='Path to ONNX model')
    parser.add_argument('-o', '--output', type=str, default='video/output/', help='Output directory')
    parser.add_argument('-t', '--IfConcat', type=str, default="None", choices=["None", "Horizontal", "Vertical"], help='Splice original + stylized video')
    parser.add_argument('-d', '--device', type=str, default='gpu', choices=["cpu", "gpu", "trt"], help='Device type')
    return parser.parse_args()

def check_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

class Videocap:
    def __init__(self, video, model_name, limit=1280):
        self.model_name = model_name
        vid = cv2.VideoCapture(video)
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.total = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = vid.get(cv2.CAP_PROP_FPS)
        self.ori_width, self.ori_height = width, height

        max_edge = max(width, height)
        scale_factor = limit / max_edge if max_edge > limit else 1.
        height = int(round(height * scale_factor))
        width = int(round(width * scale_factor))
        self.width, self.height = self.to_8s(width), self.to_8s(height)

        self.count = 0
        self.cap = vid
        self.ret, _ = self.cap.read()
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.q = queue.Queue(maxsize=60)
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    def _reader(self):
        while True:
            self.ret, frame = self.cap.read()
            if not self.ret:
                break
            frame = np.asarray(self.process_frame(frame, self.width, self.height))
            self.q.put(frame)
            self.count += 1
        self.cap.release()

    def read(self):
        f = self.q.get()
        self.q.task_done()
        return f

    def to_8s(self, x):
        if 'tiny' in self.model_name:
            return 256 if x < 256 else x - x % 16
        else:
            return 256 if x < 256 else x - x % 8

    def process_frame(self, img, width, height):
        img = Image.fromarray(img[:, :, ::-1]).resize((width, height), resample_method)
        img = np.array(img).astype(np.float32) / 127.5 - 1.0
        return np.expand_dims(img, axis=0)

class Cartoonizer():
    def __init__(self, arg):
        self.args = arg
        if ort.get_device() == 'GPU' and self.args.device == "gpu":
            self.sess_land = ort.InferenceSession(self.args.model_path, providers=['CUDAExecutionProvider'])
        elif ort.get_device() == 'trt':
            self.sess_land = ort.InferenceSession(self.args.model_path, providers=['TensorrtExecutionProvider', 'CUDAExecutionProvider'])
        else:
            self.sess_land = ort.InferenceSession(self.args.model_path, providers=['CPUExecutionProvider'])
        self.name = os.path.basename(self.args.model_path).rsplit('.', 1)[0]

    def post_precess(self, img, wh):
        img = (img.squeeze() + 1.) / 2 * 255
        img = img.clip(0, 255).astype(np.uint8)
        img = Image.fromarray(img).resize((wh[0], wh[1]), resample_method)
        return np.array(img).astype(np.uint8)

    def __call__(self):
        vid = Videocap(self.args.input_video_path, self.name)

        base_filename = os.path.splitext(os.path.basename(self.args.input_video_path))[0]
        check_folder(self.args.output)
        temp_output_path = os.path.join(self.args.output, f"{base_filename}_temp.mp4")
        final_output_path = os.path.join(self.args.output, f"{base_filename}.mp4")

        if self.args.IfConcat == "Horizontal":
            self.video_out = cv2.VideoWriter(temp_output_path, cv2.VideoWriter_fourcc(*'mp4v'), vid.fps, (vid.ori_width * 2, vid.ori_height))
        elif self.args.IfConcat == "Vertical":
            self.video_out = cv2.VideoWriter(temp_output_path, cv2.VideoWriter_fourcc(*'mp4v'), vid.fps, (vid.ori_width, vid.ori_height * 2))
        else:
            self.video_out = cv2.VideoWriter(temp_output_path, cv2.VideoWriter_fourcc(*'mp4v'), vid.fps, (vid.ori_width, vid.ori_height))

        pbar = tqdm(total=vid.total)
        pbar.set_description(f"Running: {base_filename} ({self.name})")
        num = vid.total

        while num > 0:
            if vid.count < vid.total and not vid.ret and vid.q.empty():
                pbar.close()
                self.video_out.release()
                return "The video is broken."
            frame = vid.read()
            fake_img = self.sess_land.run(None, {self.sess_land.get_inputs()[0].name: frame})[0]
            fake_img = self.post_precess(fake_img, (vid.ori_width, vid.ori_height))
            if self.args.IfConcat == "Horizontal":
                fake_img = np.hstack((self.post_precess(frame, (vid.ori_width, vid.ori_height)), fake_img))
            elif self.args.IfConcat == "Vertical":
                fake_img = np.vstack((self.post_precess(frame, (vid.ori_width, vid.ori_height)), fake_img))
            self.video_out.write(fake_img[:, :, ::-1])
            pbar.update(1)
            num -= 1

        pbar.close()
        self.video_out.release()

        try:
            # Load video đã xử lý (không có âm thanh)
            styled_clip = VideoFileClip(temp_output_path)

            # Lấy âm thanh từ video gốc
            original_audio = VideoFileClip(self.args.input_video_path).audio

            # Ghép audio vào clip đã xử lý
            final = styled_clip.set_audio(original_audio)

            # Xuất video cuối cùng
            final.write_videofile(final_output_path, codec='libx264', audio_codec='aac', preset='slow', threads=4)

            # Xóa file tạm nếu tồn tại
            if os.path.exists(temp_output_path):
                os.remove(temp_output_path)

            return final_output_path
        except Exception as e:
            print("⚠️ Lỗi khi xử lý MoviePy:", e)
            return temp_output_path


if __name__ == '__main__':
    args = parse_args()
    check_folder(args.output)
    cartoonizer = Cartoonizer(args)
    result_path = cartoonizer()
    print(f'✅ Output video: {result_path}')
