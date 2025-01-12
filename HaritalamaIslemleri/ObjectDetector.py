from collections import defaultdict
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path, class_names):
        self.model = self.load_yolo_model(model_path)
        self.class_names = class_names

    def load_yolo_model(self, model_path):
        model = YOLO(model_path)
        return model

    def detect_objects(self, frame):
        results = self.model(frame)

        # Tespit edilen nesneleri saklamak için bir defaultdict oluştur
        detected_objects = defaultdict(int)

        # Sonuçlar içinde her bir nesne tespiti için döngü
        for result in results[0].boxes:  # Her tespit için döngü
            confidence = result.conf  # Tespit edilen nesnenin güven skoru
            class_id = int(result.cls)  # Nesnenin sınıf kimliği
            class_name = self.class_names[class_id]  # Sınıf kimliğinden sınıf adını al

            if confidence > 0.25:
                detected_objects[class_name] += 1  # Nesne türüne göre sayıyı artır

        return detected_objects