import cv2
import os

def create_video_summary(video_path, output_path):
    capture = cv2.VideoCapture(video_path)
    frame_rate = capture.get(cv2.CAP_PROP_FPS)
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    summary_frames = []

    while True:
        ret, frame = capture.read()

        if not ret:
            break

        summary_frames.append(frame)

        current_frame_pos = capture.get(cv2.CAP_PROP_POS_FRAMES)
        next_frame_pos = current_frame_pos + (frame_rate * 5)
        capture.set(cv2.CAP_PROP_POS_FRAMES, next_frame_pos)

    capture.release()

    selected_frames = []
    for i in range(len(summary_frames) - 1):
        difference = cv2.absdiff(summary_frames[i], summary_frames[i + 1])
        non_zero_count = cv2.countNonZero(difference)

        if non_zero_count > (frame_width * frame_height * 0.01):
            selected_frames.append(summary_frames[i])

    selected_frames.append(summary_frames[-1])

    fourcc = cv2.VideoWriter_fourcc(*"DAV ")
    writer = cv2.VideoWriter(output_path, fourcc, frame_rate, (frame_width, frame_height), True)

    for frame in selected_frames:
        writer.write(frame)

    writer.release()

def process_directory(base_dir):
    for dirpath, _, filenames in os.walk(base_dir):
        for filename in filenames:
            if filename.endswith(".DAV"):
                video_path = os.path.join(dirpath, filename)
                output_path = os.path.join(dirpath, filename[:-4] + "_summary.DAV")
                create_video_summary(video_path, output_path)

if __name__ == "__main__":
    base_dir = "C:\\Users\\hjorquera\\Desktop\\DAV"
    process_directory(base_dir)