import cv2
from PIL import Image
import os

def get_video_fps_and_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.release()
    return int(fps), int(total_frames)

def decide_sampling_strategy(duration_sec):
    if duration_sec < 10:
        return 10
    elif duration_sec < 20:
        return 20
    else:
        return 40

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

def create_video_collage(video_path, output_path="collage.png"):
    print(f"🎬 Lade Video: {video_path}")
    fps, total_frames = get_video_fps_and_frames(video_path)
    duration_sec = total_frames / fps
    print(f"📊 Video FPS: {fps}, Dauer: {duration_sec:.2f} Sekunden")

    target_frame_count = decide_sampling_strategy(duration_sec)
    skip = max(int(total_frames / target_frame_count), 1)
    print(f"🎯 Extrahiere {target_frame_count} Frames (alle {skip} Frames)")

    frames = extract_frames(video_path, max_frames=target_frame_count, skip=skip)

    if not frames:
        raise ValueError("Keine Frames extrahiert. Überprüfe die Videodatei.")

    collage = combine_frames_horizontally(frames)
    collage.save(output_path)
    print(f"✅ Collage gespeichert unter: {output_path}")

# === MAIN: Einfach hier deinen Pfad anpassen ===
if __name__ == "__main__":
    input_path = "./Teaching_files/Signdict_Vidoscraped/Alles.mp4"          # <--- HIER Pfad zum Video oder GIF angeben!
    output_path = "meine_collage_alles.png"
    create_video_collage(input_path, output_path)
