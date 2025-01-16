class ReportGenerator:
    def __init__(self, fps):
        self.fps = fps  # Frame rate bilgisini sakla

    def generate_report(self, detections):
        """
        Tespit edilen nesneler için her saniyenin ortalama değerlerini içeren rapor oluşturur.

        ObjectDetector gelen dict burada kullanıyorum
            Örnek format:
            {
                1: [{"plastic bottle": 20, "plastic bag": 1}, {"plastic bottle": 10, "plastic bag": 3}...],
                2: [{"plastic bottle": 22, "plastic bag": 5}, {"plastic bottle": 6, "plastic bag": 1}],
                ...
            }

        Geriye liste halinde tutuyoruz ve geri yolluyoruz
            Örnek format:
            [(1, {"plastic bottle": 15, "plastic bag": 2}), (2, {"plastic bottle": 14, "plastic bag": 3})]
        """
        # Raporları saklayacak listeyi başlat
        reports = []

        # Her saniye için tespit edilen nesneler üzerinde döngü başlat
        for second, frame_detections in detections.items():
            # Her saniye için ortalama değerleri saklayacak bir sözlük başlat
            avg_counts = {}

            # İlk framedeki tüm sınıf isimlerini alarak döngü başlat
            for class_name in frame_detections[0].keys():
                # Sınıfın toplam sayısını hesaplamak için bir değişken başlat
                total_count = 0

                # Her frame için o sınıfın tespit edilen sayısını topla
                for frame in frame_detections:
                    total_count += frame[class_name]

                # Ortalama sayıyı hesapla toplam değer / frame sayısı
                avg_count = total_count / len(frame_detections)

                # Hesaplanan ortalamayı sınıf adıyla birlikte avg_counts sözlüğüne ekle
                avg_counts[class_name] = avg_count

            # Saniye ve ortalama değerleri raporlar listesine ekle
            reports.append((second, avg_counts))

        # Tüm raporları döndür
        return reports
