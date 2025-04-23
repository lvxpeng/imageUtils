import cv2
import os

def extract_frames(input_path, output_path, n):
    # 确保输出路径存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 打开视频文件
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        print(f"Error: Could not open video file {input_path}")
        return

    frame_count = 0
    extracted_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 每隔n帧提取一帧
        if frame_count % n == 0:
            frame_filename = os.path.join(output_path, f"frame_{extracted_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            extracted_count += 1

        frame_count += 1

    cap.release()
    print(f"Extracted {extracted_count} frames from {input_path} to {output_path}")

# 示例调用
input_video_path = "D:/temp/video/100-GaMDLC_Resnet101_micabrainDec19shuffle1_snapshot_010_p60_labeled.mp4"
output_frames_path = "D:/temp/video/frames"
n = 10  # 每隔10帧提取一帧

extract_frames(input_video_path, output_frames_path, n)
