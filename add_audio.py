from moviepy.editor import VideoFileClip, AudioFileClip

# Đường dẫn tới file video và audio
video_clip = VideoFileClip(r"D:\4_AI\AnimeGANv3\output\results\39.mp4")
audio_clip = AudioFileClip(r"D:\4_AI\AnimeGANv3\output\results\39.mp3")

# Cắt audio nếu dài hơn video
audio_clip = audio_clip.subclip(0, video_clip.duration)

# Gán audio vào video
final_clip = video_clip.set_audio(audio_clip)

# Xuất video mới
final_clip.write_videofile(r"video_anime/39.mp4", codec="libx264", audio_codec="aac")