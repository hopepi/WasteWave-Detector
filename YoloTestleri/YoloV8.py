from ultralytics import YOLO

def main():
    # Modeli yükle
    model = YOLO('yolov8n.pt')  # Alternatif olarak 'yolov8s.pt', 'yolov8m.pt n s m l xl tarzı gidiyor' kullanabilirsiniz.

    data_yaml_path = r"C:\Users\umutk\OneDrive\Masaüstü\Yeni veri seti\SeaSight.v2i.yolov11\data.yaml"
    # Modeli eğit
    model.train(
        data=data_yaml_path,        # YAML dosyasının yolu.
        task = 'detect',            # Tespit görevine odaklandığınızı belirtir
        epochs=30,                  # Modelin eğitileceği epoch sayısı. Yüksek değer daha iyi öğrenme sağlar ama aşırı öğrenmeye (overfitting) yol açabilir.
        batch=12,                   # Bir batch'teki görüntü sayısı. GPU belleği ile optimize edilmelidir.
        imgsz=640,                  # Görüntülerin boyutu (genişlik x yükseklik). Daha büyük boyut, daha iyi doğruluk sağlar ama daha fazla GPU belleği tüketir.
        workers=3,                  # Veriyi işlemek için kullanılacak CPU çekirdeği sayısı. Yüksek sayılar veri yüklemesini hızlandırabilir.
        optimizer="Adam",           # Optimizasyon algoritması. 'SGD' (Stochastic Gradient Descent) veya 'Adam' kullanılabilir.
        lr0=0.0005,                 # Başlangıç öğrenme oranı. Daha küçük değerler daha yavaş ama sağlam öğrenme sağlar.
        lrf=0.1,                    # Öğrenme oranı sonuna kadar azalma faktörü. 0.2, öğrenme oranını 1/5 oranında azaltır.
        momentum=0.9,               # SGD optimizasyonu için momentum. Yüksek değerler daha kararlı eğitim sağlar.
        weight_decay=0.0001,        # Ağırlık zayıflama katsayısı. Aşırı öğrenmeyi önlemek için kullanılır.
        patience=10,                # Eğer doğrulama kaybı belirli bir süre boyunca iyileşmezse, erken durma mekanizmasını tetikler.
        augment=False,              # Veri artırma (data augmentation). Çeşitli dönüşümlerle veri artırmayı etkinleştirir.
        val=True,                   # Doğrulama işlemini eğitim sırasında etkinleştirir.
        cache=False,                # Veriyi belleğe alarak yükleme hızını artırır.
        device=0,                   # Kullanılacak cihaz. '0' bir GPU kullanır; 'cpu' CPU kullanır.
        project="runs/train",       # Eğitim sonuçlarının kaydedileceği proje adı.
        name="exp",                 # Deneme adı. Klasör adını özelleştirir.
        exist_ok=False,             # Mevcut bir klasörü üzerine yazıp yazmama durumu.
        save_period=5,              # Modele ait ağırlıkları belirli epoch'larda kaydeder.
        freeze=[0],                 # Belirtilen katmanları dondurur. İnce ayar (fine-tuning) sırasında kullanışlıdır.
        seed=42,                    # Rastgelelik için kullanılan başlangıç değeri. Deneylerin tekrarlanabilir olmasını sağlar.
        verbose=True,               # Daha ayrıntılı çıktı almak için etkinleştirilir.
    )

    results = model.val()

    print(results)

    precision = results.metrics['precision']
    recall = results.metrics['recall']
    map_50 = results.metrics['map50']
    map_50_95 = results.metrics['map']

    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"mAP@0.5: {map_50:.4f}")
    print(f"mAP@0.5:0.95: {map_50_95:.4f}")

if __name__ == '__main__':
    main()
