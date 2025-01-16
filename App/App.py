import tkinter as tk
from tkinter import filedialog, messagebox
from HaritalamaIslemleri.VideoProcessor import VideoProcessor
from HaritalamaIslemleri.ObjectDetector import ObjectDetector
from HaritalamaIslemleri.RaporGenerator import ReportGenerator
from HaritalamaIslemleri.PdfGenerator import save_pdf_report
from collections import defaultdict
from ultralytics import YOLO

def process_video(video_path, model_path, class_names):
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
            frame_detections.append(detector.detect_objects(frame))  # Tespit edilen nesneler
        detections[second] = frame_detections  # Tespitleri saniyeye göre sakla

    # Rapor oluştur
    reports = report_generator.generate_report(detections)
    return reports

def choose_video():
    filepath = filedialog.askopenfilename(
        title="Bir video seçin",
        filetypes=(("MP4 Dosyaları", "*.mp4"), ("Tüm Dosyalar", "*.*"))
    )
    return filepath


def live_view():
    try:

        # YOLO modelini yükle
        model = YOLO('../YoloTestleri/runs/train/exp4/weights/best.pt')

        # Test videosu yolu
        video_path = filedialog.askopenfilename(
            title="Bir video seçin",
            filetypes=(("MP4 Dosyaları", "*.mp4"), ("Tüm Dosyalar", "*.*"))
        )
        if not video_path:
            return

        # Model ile tahmin yap
        model.predict(
            source=video_path,  # Test edilecek video yolu
            save=False,  # Tahmin sonuçlarını kaydetme avi video olarak
            save_txt=False,  # Tahmin sonuçlarını .txt olarak kaydetme
            save_conf=True,  # Tahmin sonuçlarına güven skoru ekleme
            conf=0.25,  # Minimum güven skoru
            show=True  # Sonuçları gerçek zamanlı gösterme
        )
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

def summary_report():
    video_path = choose_video()
    if not video_path:
        return
    model_path = "../YoloTestleri/runs/train/exp4/weights/best.pt"  # Model yolu
    class_names = ['Plastic Bottle', 'Plastic Bag', 'Can', 'Packing Waste', 'Net', 'Glass', 'Mask', 'Glove', 'Balloon', 'Cigarette Butt', 'Other']

    try:
        reports = process_video(video_path, model_path, class_names)

        # Detaylı PDF raporu oluştur
        pdf_path = save_pdf_report(reports)
        messagebox.showinfo("Başarılı", f"Rapor PDF olarak kaydedildi: {pdf_path}")

        # Sonuçları GUI'de göster
        result_window = tk.Toplevel()
        result_window.title("Özet Rapor")
        text = tk.Text(result_window, wrap=tk.WORD)
        text.pack(expand=True, fill=tk.BOTH)

        for second, avg_counts in reports:
            text.insert(tk.END, f"Saniye {second}: {avg_counts}\n")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

# Tkinter arayüzü
root = tk.Tk()
root.title("Deniz Çöpü Tespit Aracı")

label = tk.Label(root, text="Lütfen bir seçenek seçin", font=("Helvetica", 16))
label.pack(pady=20)

live_button = tk.Button(root, text="Canlı İzleme", command=live_view, font=("Helvetica", 14), width=20)
live_button.pack(pady=10)

summary_button = tk.Button(root, text="Özet Çıkarma", command=summary_report, font=("Helvetica", 14), width=20)
summary_button.pack(pady=10)

exit_button = tk.Button(root, text="Çıkış", command=root.quit, font=("Helvetica", 14), width=20, bg="red", fg="white")
exit_button.pack(pady=20)

root.mainloop()
