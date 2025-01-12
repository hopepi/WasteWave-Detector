import numpy as np

class ReportGenerator:
    def __init__(self, fps):
        self.fps = fps

    def generate_report(self, detections):
        # Raporları saklayacak listeyi başlat
        reports = []
        # Her saniye için tespit edilen nesneler üzerinde döngü başlat
        for second, frame_detections in detections.items():
            # Her saniye için nesne türlerinin ortalama sayısını hesapla
            avg_counts = {}
            for class_name in frame_detections[0].keys():
                # İlk frame'deki tüm sınıf isimlerini alarak, her bir sınıf için ortalama hesaplanır
                total_count = 0
                # Her frame için, o frame'deki ilgili nesne sınıfının sayısını toplamaya başla
                for frame in frame_detections:
                    total_count += frame[class_name]
                # Ortalama sayıyı hesapla
                avg_count = total_count / len(frame_detections)  # Toplam sayıyı frame sayısına bölerek ortalama al
                # Hesaplanan ortalamayı, sınıf adı ile birlikte avg_counts sözlüğüne ekle
                avg_counts[class_name] = avg_count
            reports.append((second, avg_counts))

        return reports