from moviepy import *
import skvideo.io
from models import TransformerNet
from utils import *
import torch
from torch.autograd import Variable
import argparse
import os
import tqdm
from PIL import Image
import os
import argparse
#from moviepy import *
from concurrent import futures

# basic settings
style_nums = 2
content_dir = r"./images/content/"
style_dir = r"./images/styles/"
style_model_dir = r"./style-transfer-models-20230129T081747Z-001/style-transfer-models/"
output_dir = r"./images/outputs/"
temp_dir = r"./images/styles/"
output_style_file_list = list()

video_path = content_dir + "rowtaroVideo.mp4"

# Load mp4
def VideoCuts(video_path, temp_path1, temp_path2):
    if os.path.exists("./temp1.,p4") or os.path.exists("./temp2.mp4"):
        print(" temp file exist !!!")
        return -1
    video = VideoFileClip(video_path)
    time_len = int (video.duration)
    sub_clip1 = video.subclip(0, 1/2 * time_len)
    sub_clip2 = video.subclip(1/2 * time_len, time_len)

    sub_clip1.write_videofile(temp_path1, fps = 30)
    sub_clip2.write_videofile(temp_path2, fps = 30)
    return 0

def setStyle(index = 0):
    style_map = list()
    style_map = os.listdir(style_dir)
    style_image_path = ""
    if index >= 0:
        style_image_path = style_map[index]
    elif index > style_map.len():
        raise Exception(" Index for styles overflow")
    else:
        raise Exception(" Invalid index ")
    

def videoTransfer(video_path, checkpoint_model, device):
    transform = style_transform()

    # Define model and load model checkpoint
    transformer = TransformerNet().to(device)
    transformer.load_state_dict(torch.load(checkpoint_model))
    transformer.eval()

    stylized_frames = []
    for frame in tqdm.tqdm(extract_frames(video_path), desc="Processing frames"):
        # Prepare input frame
        image_tensor = Variable(transform(frame)).to(device).unsqueeze(0)
        # Stylize image
        with torch.no_grad():
            stylized_image = transformer(image_tensor)
        # Add to frames
        stylized_frames += [deprocess(stylized_image)]

    # Create video from frames
    video_name = video_path.split("/")[-1].split(".")[0]
    writer = skvideo.io.FFmpegWriter(f"images/outputs/stylized-{video_name}.mp4")
    for frame in tqdm.tqdm(stylized_frames, desc="Writing to video"):
        writer.writeFrame(frame)
    writer.close()
    output_style_file_list.append(f"images/outputs/stylized-{video_name}.mp4")


if __name__ == '__main__':
    #parser =  argparse.ArgumentParser()
    #parser.add_argument("--video_path", type=str, required=True, help="Path to video")
    #parser.add_argument("--checkpoint_model_dir", type=str, required=True, help="Path to checkpoint model")
    #args = parser.parse_args()
    #print(args)

    os.makedirs(output_dir, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    style_model_list = os.listdir(style_model_dir)
    print ("model list: ", style_model_list)
    temp_paths = ["./temp1.mp4", "./temp2.mp4"]
    VideoCuts(video_path, temp_paths[0], temp_paths[1])
    print( "Begin to handling concurrent tasks")
    async_list = list()
    with futures.ThreadPoolExecutor(style_nums) as executor:
        for index in range(style_nums):
            checkpoint_model = style_model_dir + style_model_list[index]
            print (" Current style is to submit: ", style_model_list[index], "... ")
            executor.submit(executor.submit(videoTransfer, temp_paths[index], checkpoint_model, device))
    
    ## concat temp-videos
   
    video = VideoFileClip(output_style_file_list[0])
    output_style_file_list.pop(0)
    for video_name in output_style_file_list:
        video = concatenate_videoclips([video, VideoFileClip(video_name)], "compose")
    res = output_dir + "res.mp4"
    video.write_videofile(res)
       


    