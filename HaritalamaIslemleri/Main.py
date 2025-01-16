from VideoProcessor import VideoProcessor
from ObjectDetector import ObjectDetector
from RaporGenerator import ReportGenerator
from collections import defaultdict


def main(video_path, model_path, class_names):
    # Video işleyici, nesne tespit edici ve rapor oluşturucu başlatılır
    video_processor = VideoProcessor(video_path)
    detector = ObjectDetector(model_path, class_names)
    report_generator = ReportGenerator(video_processor.fps)

    # Video işlenir ve kareler çıkartılır
    frames_per_second = video_processor.get_frames_per_second()
    detections = defaultdict(list)  # Her saniye için tespitleri saklar

    # Her saniye için nesne tespiti yapılır
    for second, frames in enumerate(frames_per_second):
        frame_detections = []
        for frame in frames:
            # Her karede nesne tespiti yapılır
            frame_detections.append(detector.detect_objects(frame))  # Tespit edilen nesneler
        detections[second] = frame_detections  # Tespitleri saniyeye göre sakla

    # Rapor oluştur ve yazdır
    reports = report_generator.generate_report(detections)
    for second, avg_counts in reports:
        print(f"Saniye {second}: {avg_counts}")  # Her saniye için ortalama nesne sayısını yazdır

if __name__ == "__main__":
    video_path = "../YoloTestleri/TestVideos/test2.mp4"  # Gerçek video dosyasının yolu
    model_path = "../YoloTestleri/runs/train/exp4/weights/best.pt"  # Gerçek YOLO modeli yolunu buraya yazın
    class_names = ['Plastic Bottle', 'Plastic Bag', 'Can', 'Packing Waste', 'Net', 'Glass', 'Mask', 'Glove', 'Balloon', 'Cigarette Butt', 'Other']  # Sınıflar
    main(video_path, model_path, class_names)
