import os
import cv2

def extract_frames_from_video(video_path, output_folder, frame_rate=25):
    os.makedirs(output_folder, exist_ok=True)  # Karelerin kaydedileceği klasörü oluşturur.
    cap = cv2.VideoCapture(video_path)  # Video dosyasını açar.
    frame_id = 0

    while cap.isOpened():
        ret, frame = cap.read()  # Videodan bir kare okur.
        if not ret:
            break
        if frame_id % frame_rate == 0:
            frame_filename = os.path.join(output_folder, f"frame_{frame_id}.jpg")  # Kare ismini oluşturur.
            cv2.imwrite(frame_filename, frame)  # Kareyi dosya olarak kaydeder.
        frame_id += 1

    cap.release()  # Video dosyasını kapatır.


def process_videos_in_folder(video_folder, output_folder, frame_rate=5):
    os.makedirs(output_folder, exist_ok=True)  # Çıktı klasörünü oluşturur.

    for video_file in os.listdir(video_folder):  # Klasördeki tüm video dosyalarını işler.
        video_path = os.path.join(video_folder, video_file)  # Videonun tam yolunu oluşturur.
        if not os.path.isfile(video_path):  # Eğer dosya değilse (örn. klasör), işlemez.
            continue
        video_output_folder = os.path.join(output_folder, video_file.split('.')[0])  # Her video için karelerin kaydedileceği klasörü belirler.
        extract_frames_from_video(video_path, video_output_folder, frame_rate=frame_rate)  # Videoyu karelere ayırarak klasöre kaydeder.


# Kullanım Örneği
video_folder = "C:\\Users\\umutk\\PycharmProjects\\dataCombiner\\Videos"
output_folder = r"C:\Users\umutk\PycharmProjects\dataCombiner\newData"
frame_rate = 5

process_videos_in_folder(video_folder, output_folder, frame_rate)