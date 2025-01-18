from ultralytics import YOLO

def train_model(yaml_path, epochs=30, batch_size=8, img_size=640):
    try:
        # Modeli yükle
        model = YOLO('yolov8s.pt')

        # Modeli eğit
        model.train(
            data=yaml_path,
            task='detect',
            epochs=epochs,
            batch=batch_size,
            imgsz=img_size,
            workers=0,
            optimizer="SGD",
            lr0=0.001,
            lrf=0.1,
            momentum=0.9,
            weight_decay=0.0001,
            patience=10,
            augment=False,
            val=True,
            device=0,
            project="runs/train",
            name="exp",
            save_period=5,
            seed=42,
            verbose=True,
        )

        # Model doğrulama
        results = model.val()
        print("Doğrulama sonuçları:", results)
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == '__main__':
    # YAML dosya yolunu ve eğitim parametrelerini tanımla
    data_yaml_path = r"C:\Users\umutk\OneDrive\Masaüstü\test\SeaSight.v2i.yolov11\data.yaml"
    train_model(data_yaml_path)
