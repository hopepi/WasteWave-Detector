import matplotlib.pyplot as plt
from fpdf import FPDF
import numpy as np
import tempfile
import os
import math
def save_pdf_report(reports, output_path="rapor.pdf", threshold=1):
    """
    Detaylı video analiz raporunu PDF formatında kaydeder.
    Bu fonksiyon, her saniye için ısı haritası da ekler.

    Args:
        reports (list): Her saniyedeki nesne tespit raporlarını içeren liste.
        output_path (str): PDF dosyasının kaydedileceği yol.
        threshold (float): Raporlanacak minimum yoğunluk değeri.

    Returns:
        str: Kaydedilen PDF dosyasının yolu.
    """
    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Unicode yazı tipi ekle
        pdf.add_font('DejaVu', '', '../dejavu-sans/DejaVuSans.ttf', uni=True)
        pdf.add_font('DejaVu', 'B', '../dejavu-sans/DejaVuSans-Bold.ttf', uni=True)
        pdf.set_font("DejaVu", size=12)

        # Başlık
        pdf.set_font("DejaVu", style="B", size=16)
        pdf.cell(200, 10, txt="Detaylı Video Analiz Raporu", ln=True, align="C")
        pdf.ln(10)

        # Yuvarlanmış ve filtrelenmiş raporları yazdır
        pdf.set_font("DejaVu", size=12)
        for second, avg_counts in reports:
            rounded_counts = {k: (math.ceil(v) if v >= threshold else 0) for k, v in avg_counts.items()}
            pdf.cell(0, 10, f"Saniye {second}: {rounded_counts}", ln=True)

        # Genel yoğunluk grafiği ekleme
        pdf.add_page()
        pdf.set_font("DejaVu", style="B", size=14)
        pdf.cell(200, 10, txt="Genel Yoğunluk Grafiği", ln=True, align="C")
        pdf.ln(10)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_graph_file:
            create_overall_graph(reports, temp_graph_file.name, threshold)
            pdf.image(temp_graph_file.name, x=10, y=30, w=190)
            temp_graph_file_path = temp_graph_file.name

        # Her nesnenin yoğunluğu için ayrı grafikler
        for class_name in reports[0][1].keys():
            # Sadece yoğunluk verisi boş değilse grafiği oluştur
            if any(avg_counts.get(class_name, 0) >= threshold for _, avg_counts in reports):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_graph_file:
                    create_individual_graph(reports, temp_graph_file.name, class_name, threshold)
                    pdf.add_page()
                    pdf.cell(200, 10, txt=f"{class_name} Yoğunluk Grafiği", ln=True, align="C")
                    pdf.image(temp_graph_file.name, x=10, y=30, w=190)
                    temp_graph_file_path = temp_graph_file.name

        # Her saniye için ısı haritası ekleme
        for second, avg_counts in reports:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_graph_file:
                create_heatmap(reports, temp_graph_file.name, second, threshold)
                pdf.add_page()
                pdf.cell(200, 10, txt=f"Saniye {second} Isı Haritası", ln=True, align="C")
                pdf.image(temp_graph_file.name, x=10, y=30, w=190)
                temp_graph_file_path = temp_graph_file.name

        # PDF'yi kaydet
        pdf.output(output_path)

        # Geçici grafik dosyasını sil
        if os.path.exists(temp_graph_file_path):
            os.remove(temp_graph_file_path)

        return output_path
    except Exception as e:
        print(f"PDF oluşturulurken bir hata oluştu: {e}")
        return None


def create_overall_graph(reports, output_path, threshold=1):
    """
    Genel yoğunluk grafiği oluşturur ve kaydeder.

    Args:
        reports (list): Her saniyedeki nesne tespit raporlarını içeren liste.
        output_path (str): Kaydedilecek grafik dosyasının yolu.
        threshold (float): Minimum yoğunluk değeri.
    """
    seconds = []
    total_objects = []

    for second, avg_counts in reports:
        seconds.append(second)
        total_objects.append(sum(math.ceil(v) if v >= threshold else 0 for v in avg_counts.values()))

    plt.figure(figsize=(10, 6))
    plt.plot(seconds, total_objects, marker="o", linestyle="-", color="b", label="Toplam Nesne")
    plt.xlabel("Saniye")
    plt.ylabel("Toplam Nesne Sayısı")
    plt.title("Her Saniyedeki Toplam Nesne Yoğunluğu")
    plt.legend()
    plt.grid()
    plt.savefig(output_path)
    plt.close()


def create_individual_graph(reports, output_path, class_name, threshold=1):
    """
    Belirli bir nesne sınıfı için yoğunluk grafiği oluşturur ve kaydeder.

    Args:
        reports (list): Her saniyedeki nesne tespit raporlarını içeren liste.
        output_path (str): Kaydedilecek grafik dosyasının yolu.
        class_name (str): Yoğunluk grafiği oluşturulacak nesne sınıfı.
        threshold (float): Minimum yoğunluk değeri.
    """
    seconds = []
    class_counts = []

    for second, avg_counts in reports:
        seconds.append(second)
        class_counts.append(math.ceil(avg_counts.get(class_name, 0)) if avg_counts.get(class_name, 0) >= threshold else 0)

    plt.figure(figsize=(10, 6))
    plt.plot(seconds, class_counts, marker="o", linestyle="-", label=class_name)
    plt.xlabel("Saniye")
    plt.ylabel(f"{class_name} Sayısı")
    plt.title(f"Her Saniyedeki {class_name} Yoğunluğu")
    plt.legend()
    plt.grid()
    plt.savefig(output_path)
    plt.close()

def create_heatmap(reports, output_path, second, threshold=1):
    """
    Her saniye için ısı haritası oluşturur ve kaydeder.

    Args:
        reports (list): Her saniyedeki nesne tespit raporlarını içeren liste.
        output_path (str): Kaydedilecek grafik dosyasının yolu.
        second (int): Isı haritası oluşturulacak saniye.
        threshold (float): Minimum yoğunluk değeri.
    """
    # Saniyeye ait yoğunluk verilerini al
    for s, avg_counts in reports:
        if s == second:
            # Her nesnenin yoğunluğunu kontrol et
            grid_size = 10  # Isı haritasının grid boyutu (örnek: 10x10)
            grid = np.zeros((grid_size, grid_size))  # Başlangıçta sıfırlarla dolu bir grid

            # Her nesnenin koordinatları (örnek: (x, y)) ile grid üzerinde yoğunluk hesapla
            for class_name, count in avg_counts.items():
                if count >= threshold:
                    # Burada her nesnenin (x, y) koordinatları verilmiş olmalı
                    # Örnek olarak rastgele x, y değerleri atıyoruz
                    x, y = np.random.randint(0, grid_size), np.random.randint(0, grid_size)
                    grid[x, y] += math.ceil(count)  # Yoğunluğu grid'e ekle

            # Isı haritasını çiz
            plt.figure(figsize=(6, 6))
            plt.imshow(grid, cmap='hot', interpolation='nearest')
            plt.colorbar(label='Yoğunluk')
            plt.title(f"Saniye {second} Isı Haritası")
            plt.xlabel("X Koordinatı")
            plt.ylabel("Y Koordinatı")

            # Görseli kaydet
            plt.savefig(output_path)
            plt.close()
            break