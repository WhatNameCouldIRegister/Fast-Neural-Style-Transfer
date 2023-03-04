from moviepy import *


output_style_file_list = ["./images/outputs/stylized-temp1.mp4", "./images/outputs/stylized-temp2.mp4"]
video = VideoFileClip(output_style_file_list[0])
output_style_file_list.pop(0)
for video_name in output_style_file_list:
    video = concatenate_videoclips([video, VideoFileClip(video_name)], "compose")
video.write_videofile(r"styleRowtaro.mp4")