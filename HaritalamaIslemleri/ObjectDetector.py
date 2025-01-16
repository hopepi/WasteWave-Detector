from collections import defaultdict  # Nesne sayısını kolayca saklamak için defaultdict kullanılıyor
from ultralytics import YOLO  # YOLO modeli için gerekli kütüphane


class ObjectDetector:
    def __init__(self, model_path, class_names):
        self.model = self.load_yolo_model(model_path)  # Modeli yükle
        self.class_names = class_names  # Sınıf adlarını sakla

    def load_yolo_model(self, model_path):
        """
        YOLO modelini yükler ve geriye döndürür
        """
        model = YOLO(model_path)  # YOLO modelini belirtilen yoldan yükle
        return model

    def detect_objects(self, frame):
        """
        Verilen bir karede nesne tespiti yapar kısacası resim 25 fps ise 25 kare vardır demek bunların hepsini
        tek tek tespit edip nesnelerin türünü ve sayısını defaultdict kütüphanesi yardımıyla geriye döndürüyor
        """
        results = self.model(frame)  # Modeli kullanarak nesneleri tespit et

        # Tespit edilen nesneleri saklamak için bir defaultdict oluştur
        detected_objects = defaultdict(int)

        # Tespit edilen nesneler üzerinde döngü
        for result in results[0].boxes:  # Her tespit edilen nesne için döngü
            confidence = result.conf  # Tespit edilen nesnenin güven skoru
            class_id = int(result.cls)  # Nesnenin sınıf kimliği
            class_name = self.class_names[class_id]  # Sınıf kimliğinden sınıf adı bulunur

            # Sadece güven skoru 0.25ten yüksek olan nesneleri dikkate al
            if confidence > 0.25:
                detected_objects[class_name] += 1  # Sınıfa ait nesne sayısını artır

        return detected_objects  # Tespit edilen nesneleri döndür
