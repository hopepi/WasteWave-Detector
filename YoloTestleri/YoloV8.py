from ultralytics import YOLO

def main():
    # Modeli yükle
    model = YOLO('yolov8s.pt')  # Alternatif olarak 'yolov8s.pt', 'yolov8m.pt n s m l xl tarzı gidiyor' kullanabilirsiniz.

    data_yaml_path = r"C:\Users\umutk\OneDrive\Masaüstü\Yeni veri seti2\SeaSight.v2i.yolov11\data.yaml"
    # Modeli eğit
    model.train(
        data=data_yaml_path,        # Eğiticeğimiz YAML dosyasının yolunu veriyoz
        task = 'detect',            # detect ile 'tespit' görevine odaklandığımızı belirtiyoz
        epochs=30,                  # Modelimizin eğitilceği epoch sayısı. Yüksek değer ile daha iyi öğrenme sağlar ama aşırı öğrenmeye (overfitting) yol açabilir.
        batch=9,                    # bir batch'teki görüntü sayısımız. Tek seferde kaç resim eğitileceği
        imgsz=640,                  # Görüntülerimizin boyutu (genişlik x yükseklik şeklinde)
        workers=0,                  # Verimizi işlemek için kullanılacak CPU çekirdeği sayısı. Yüksek sayılar veri yüklemesini hızlandırabilir.
        optimizer="SGD",            # Optimizasyon algoritmamız. 'SGD' (Stochastic Gradient Descent) açılımı. 'Adam' da denedik.
        lr0=0.001,                  # Başlangıç öğrenme oranı belirliyoruz. Daha küçük değerler daha yavaş ama sağlam öğrenme sağlar.
        lrf=0.1,                    # Öğrenme oranı sonuna doğru azalma faktörüdür. Sona doğru iyi oran almamızı sağladı
        momentum=0.9,               # SGD optimizasyonu için momentum. Yüksek değerlerde daha kararlı eğitim sağladı
        weight_decay=0.0001,        # Ağırlık zayıflama katsayısı. Aşırı öğrenmeyi önlemek için kullanılır.
        patience=10,                # Eğer doğruluk oranımız belirli bir süre boyunca iyileşmezse die erken durma mekanizmasını devreye sokuyoruz
        augment=False,              # Veri artırma işlemi için 'True' yapılabilir. Biz kendimiz veride oynama yaptığımzdan kapattık
        val=True,                   # Doğrulama işlemini eğitim sırasında etkinleştirir
        device=0,                   # Kullanılacak cihazı belirliyoruz. '0' bir GPU kullanıyo, 'cpu' CPU kullanılıyo
        project="runs/train",       # Eğitim sonuçlarının kaydedileceği proje adı şekli
        name="exp",                 # eğitilen modelin kaydedilceği ismini veriyoruz
        save_period=5,              # model ağırlığını ne kadarda bir kaydettiğini veriyoruz
        seed=42,                    # Rastgelelik için kullanılan başlangıç değeri
        verbose=True,               # Daha ayrıntılı çıktı almaız için aktifleştirdik
    )

    results = model.val()

    if results:
        precision = results.metrics['precision']    # Algılanan nesnelerin ne kadar doğru sınıflandırıldığını gösterir
        recall = results.metrics['recall']          # Tüm gerçek nesnelerin ne kadarının tespit edildiğini gösterir
        map_50 = results.metrics['map50']           # Tespit doğruluğunu (IoU = 0.5 eşik değeriyle) ölçer
        map_50_95 = results.metrics['map']          # Farklı IoU eşiklerinde genel doğruluk ölçütü
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"mAP@0.5: {map_50:.4f}")
        print(f"mAP@0.5:0.95: {map_50_95:.4f}")
    else:
        print("Doğrulama sonuçları boş. Veri kümenizi veya model yapılandırmanızı kontrol edin.")

if __name__ == '__main__':
    main()
