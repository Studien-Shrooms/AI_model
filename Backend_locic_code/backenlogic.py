import os
import mimetypes
import cv2
from PIL import Image
import torch
from transformers import MllamaForConditionalGeneration, AutoProcessor

# === Modell initialisieren ===
base_model = "/kaggle/input/llama-3.2-vision/transformers/11b-vision-instruct/1"
processor = AutoProcessor.from_pretrained(base_model)
model = MllamaForConditionalGeneration.from_pretrained(
    base_model,
    low_cpu_mem_usage=True,
    torch_dtype=torch.float16,
    device_map="auto",
)
torch.cuda.empty_cache()

# === Hilfsfunktionen ===

def get_file_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        raise ValueError("Unbekannter Dateityp.")
    if "image" in mime_type:
        if file_path.lower().endswith(".gif"):
            return "gif"
        else:
            return "image"
    elif "video" in mime_type:
        return "video"
    else:
        raise ValueError(f"Nicht unterstützter Dateityp: {mime_type}")

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

def extract_frames_from_gif(gif_path, max_frames=10, resize=(224, 224)):
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frame = gif.copy().convert("RGB").resize(resize)
            frames.append(frame)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames[:max_frames]

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

def create_collage_if_needed(input_path, temp_output_path="temp_collage.png"):
    file_type = get_file_type(input_path)

    if file_type == "video":
        print("[i] Video erkannt → extrahiere Frames")
        fps, total_frames = get_video_fps_and_frames(input_path)
        duration_sec = total_frames / fps
        target_frame_count = decide_sampling_strategy(duration_sec)
        skip = max(int(total_frames / target_frame_count), 1)
        frames = extract_frames(input_path, max_frames=target_frame_count, skip=skip)

    elif file_type == "gif":
        print("[i] GIF erkannt → extrahiere Frames")
        frames = extract_frames_from_gif(input_path)

    elif file_type == "image":
        print("[i] Direktes Bild erkannt → keine Collage nötig")
        return input_path, False  # Kein temporäres Bild

    else:
        raise ValueError("Nicht unterstützter Dateityp.")

    if not frames:
        raise ValueError("Keine Frames gefunden!")

    print("[i] Erstelle Collage ...")
    collage = combine_frames_horizontally(frames)
    collage.save(temp_output_path)
    return temp_output_path, True

# === Modellanbindung ===
def ask_model_ai(image_path):
    image = Image.open(image_path).resize((224, 224))

    messages = [
        {"role": "user", "content": [
            {"type": "image"},
            {"type": "text", "text": "Analysiere die Bildsequenz. Sie besteht aus mehreren Einzelbildern, die aus einem Video extrahiert wurden. Die Bilder zeigen die zeitliche Entwicklung einer Gebärde, angeordnet von links nach rechts. Gib den gesprochenen Inhalt in Hochdeutsch zurück."}
        ]}
    ]
    input_text = processor.apply_chat_template(messages, add_generation_prompt=True)

    inputs = processor(image, input_text, return_tensors="pt").to(model.device)
    inputs = {k: v.to(dtype=torch.float16) if v.dtype == torch.float32 else v for k, v in inputs.items()}

    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=60)

    return processor.decode(output[0], skip_special_tokens=True)

# === Hauptfunktion ===
def handle_input_file(input_path, loesche_original=True):
    bildpfad = None
    temp_created = False
    result = None

    try:
        bildpfad, temp_created = create_collage_if_needed(input_path)
        result = ask_model_ai(bildpfad)
        print(f"[+] Modellantwort: {result}")

    finally:
        if temp_created and os.path.exists(bildpfad):
            os.remove(bildpfad)
            print(f"[i] Temporäres Bild gelöscht: {bildpfad}")

        if loesche_original and os.path.exists(input_path):
            os.remove(input_path)
            print(f"[i] Originaldatei gelöscht: {input_path}")

    return result

# === Ausführung ===
if __name__ == "__main__":
    testdatei = "/kaggle/input/testingthemodel/test_file_DGL.mp4"
    antwort = handle_input_file(testdatei, loesche_original=True)
    print(f"[✓] FINAL: {antwort}")
