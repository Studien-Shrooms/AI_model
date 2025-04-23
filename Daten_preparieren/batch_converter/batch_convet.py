import cv2
import os
from PIL import Image

# ==== Hilfsfunktionen ====

def get_video_fps_and_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.release()
    return int(fps), int(total_frames)

def decide_sampling_strategy(duration_sec):
    if duration_sec < 10:
        return 20
    elif duration_sec < 20:
        return 30
    else:
        return 45

def extract_frames(video_path, max_frames=10, skip=10, resize=(224, 224)):
    cap = cv2.VideoCapture(video_path)
    frames = []
    i = 0
    while cap.isOpened() and len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        if i % skip == 0:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_frame).resize(resize)
            frames.append(pil_img)
        i += 1
    cap.release()
    return frames

def combine_frames_horizontally(frames, spacing=5):
    widths, heights = zip(*(f.size for f in frames))
    total_width = sum(widths) + spacing * (len(frames) - 1)
    max_height = max(heights)

    collage = Image.new("RGB", (total_width, max_height), color=(255, 255, 255))
    x_offset = 0
    for img in frames:
        collage.paste(img, (x_offset, 0))
        x_offset += img.width + spacing
    return collage

def create_video_collage(video_path, output_path):
    fps, total_frames = get_video_fps_and_frames(video_path)
    duration_sec = total_frames / fps
    target_frame_count = decide_sampling_strategy(duration_sec)
    skip = max(int(total_frames / target_frame_count), 1)

    frames = extract_frames(video_path, max_frames=target_frame_count, skip=skip)
    if not frames:
        raise ValueError(f"Keine Frames extrahiert für {video_path}")

    collage = combine_frames_horizontally(frames)
    collage.save(output_path)
    print(f"[✔] Gespeichert: {output_path}")

# ==== Hauptfunktion ====

def process_video_folder(input_dir, output_dir):
    supported_ext = (".mp4", ".mov", ".avi", ".mkv", ".webm")
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(supported_ext):
            input_path = os.path.join(input_dir, filename)
            name_only = os.path.splitext(filename)[0]
            output_filename = f"{name_only}_collage.png"
            output_path = os.path.join(output_dir, output_filename)
            print(f"[INFO] Verarbeite: {filename}")
            try:
                create_video_collage(input_path, output_path)
            except Exception as e:
                print(f"[ERROR] Fehler bei {filename}: {e}")

# ==== START ====

if __name__ == "__main__":
    input_folder = r"C:\Users\charl\AI_model\Teaching_files\Signdict_Vidoscraped"      # 🔁 HIER anpassen
    output_folder = r"C:\Users\charl\AI_model\Vidoe_und_Gif_umwnadung\batch_converter\output_batch_collage"      # 🔁 HIER anpassen
    process_video_folder(input_folder, output_folder)
