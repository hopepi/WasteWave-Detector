from ultralytics import YOLO

model = YOLO('runs/train/exp4/weights/best.pt')

video_path = "TestVideos/test1.mp4"

model.predict(
    source=video_path,  # Test edilecek video yolu
    save=False,         # Tahmin sonuçlarını kaydetme avi video olarak
    save_txt=False,     # Tahmin sonuçlarını .txt olarak kaydetme
    save_conf=True,     # Tahmin sonuçlarına güven skoru ekleme
    conf=0.25,          # Minimum güven skoru
    show=True           # Sonuçları gerçek zamanlı gösterme
)