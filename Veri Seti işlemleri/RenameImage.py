import os
import uuid
import shutil


#Bu fonksiyonda belirli bir klasördeki resim ve etiket dosyalarını eşleştiririp yeni bir benzersiz isimle kopyalansın diyoruz
def rename_paired_files(root_folder, output_base_folder):

    #Çıktı klasörlerimiz yani resimler ve etiketler için ayrılmış alt klasörler oluşturulalım
    output_images_dir = os.path.join(output_base_folder, "images")
    output_labels_dir = os.path.join(output_base_folder, "labels")
    os.makedirs(output_images_dir, exist_ok=True)  #Resimler için klasör oluşturuduk
    os.makedirs(output_labels_dir, exist_ok=True)  #Etiketler için klasör oluşturduk

    #Girdi klasörlerimiz yani resim ve etiket dosyalarının olduğu klasörleri gösteriyorum
    images_dir = os.path.join(root_folder, "images")
    labels_dir = os.path.join(root_folder, "labels")

    # Resim ve etiket dosyalarının eşleştirilmesi için
    paired_files = {}

    # kullanıcağımız resim uzantıları
    image_extensions = {'.png', '.jpg', '.jpeg'}
    for filename in os.listdir(images_dir):  # Resim klasöründeki dosyaları tarıyoruz
        name, ext = os.path.splitext(filename)  # Dosya adı ve uzantısı ayrıştırılsın
        if ext.lower() in image_extensions:  # Desteklenen uzantılardan biri mi kontrol edilir.
            paired_files[name] = {  # Resim dosyasının bilgileri yukarudaki alana ekleyelim
                'image': (filename, ext)
            }

    for filename in os.listdir(labels_dir):  #Etiket klasöründeki dosyalar
        name, ext = os.path.splitext(filename)  # Dosya adı ve uzantısı ayrıştırılsın
        if ext.lower() == '.txt' and name in paired_files:  #Sadece `.txt` uzantılı dosyaları alıyoruz
            paired_files[name]['label'] = (filename, ext)  #Etiket dosyaslarını alıp ekledik


    # Eşleşmiş dosyaları işleyip yeni benzersiz isimlerle kopyalıyoruz
    for original_name, files in paired_files.items():
        if 'image' in files and 'label' in files:  #Hem resim hem de etiketi eşleşmiş dosyalar için işler

            #Benzersiz bir isim oluşturulur (UUID).
            new_name = str(uuid.uuid4())

            #Resim ve etiket dosyalarının orijinal bilgileri alınıyoruz
            image_filename, image_ext = files['image'] #image olanlar
            label_filename, label_ext = files['label'] #etiket olanlar

            #Yeni dosya yolları oluşturuluruyoruz
            new_image_path = os.path.join(output_images_dir, f"{new_name}{image_ext}")
            new_label_path = os.path.join(output_labels_dir, f"{new_name}{label_ext}")

            try:
                #Resim ve etiket dosyaları yeni konumuna yüklüyoruz
                shutil.copy2(
                    os.path.join(images_dir, image_filename),
                    new_image_path
                )
                shutil.copy2(
                    os.path.join(labels_dir, label_filename),
                    new_label_path
                )
                print(f"Başarıyla işlendi: {original_name} -> {new_name}")
            except Exception as e:
                #Hata durumunda mesaj yazdırsın
                print(f"Hatalı işlem {original_name}: {str(e)}")

    return True


#Giriş ve çıkış klasör yollarının yolunu verdik
root_folder = r"C:\Users\umutk\OneDrive\Masaüstü\Yeni klasör\oceana waste.v2i.yolov11\valid"
output_base_folder = r"C:\Users\umutk\OneDrive\Masaüstü\Yeni klasör\ismiDegisen\valid"

#Fonksiyon başlatarak işlemi çalıştırıyoruz
rename_paired_files(root_folder, output_base_folder)