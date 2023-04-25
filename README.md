# Fast Neural Style Transfer in PyTorch

<p align="center">
    <img src="assets/zurich.jpg" width="900"\>
</p>

[official Lua implementation] (https://github.com/jcjohnson/fast-neural-style)).

## Train

```
python3 train.py  --dataset_path <path-to-dataset> \
                  --style_image <path-to-style-image> \
                  --epochs 1 \
                  --batch_size 4 \
                  --image_size 256
```

## DD Test Demo

```
# Test on Video

python test_on_video.py --video_path D:/GithubPrj/Fast-Neural-Style-Transfer/images/content/rowtaroVideo.mp4 --checkpoint_model D:\GithubPrj\Fast-Neural-Style-Transfer\style-transfer-models-20230129T081747Z-001\style-transfer-models\starry_night_10000.pth

```

<p align="center">
    <img src="assets/stylized-celtics.gif" width="400"\>
</p>
<p align="center">
    <img src="assets/celeba_mosaic.gif" width="400"\>
</p>
<p align="center">
    Figure: Training progress over the first 10,000 batches.
</p>
