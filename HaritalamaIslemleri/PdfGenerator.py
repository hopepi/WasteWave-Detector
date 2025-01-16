import matplotlib.pyplot as plt
from fpdf import FPDF
import numpy as np
import tempfile
import os
import math

def save_pdf_report(reports, output_path="exampleReport.pdf", threshold=1):
    """
    Detaylı video analiz raporunu PDF formatında kaydeder.
    Bu fonksiyon, her saniye için çubuk grafikler de ekler.

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

        # Her saniye için çubuk grafik ekleme
        for second, avg_counts in reports:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_graph_file:
                create_bar_plot(reports, temp_graph_file.name, second, threshold)
                pdf.add_page()
                pdf.cell(200, 10, txt=f"Saniye {second} Çubuk Grafiği", ln=True, align="C")
                pdf.image(temp_graph_file.name, x=10, y=30, w=190)
                temp_graph_file_path = temp_graph_file.name

        # Her nesne sınıfı için yoğunluk grafiği ekleme
        all_classes = set()
        for _, avg_counts in reports:
            all_classes.update(avg_counts.keys())

        for class_name in all_classes:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_graph_file:
                create_individual_graph(reports, temp_graph_file.name, class_name, threshold)
                pdf.add_page()
                pdf.cell(200, 10, txt=f"{class_name} Yoğunluk Grafiği", ln=True, align="C")
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


def create_bar_plot(reports, output_path, second, threshold=1):
    """
    Belirli bir saniye için çubuk grafik oluşturur ve kaydeder.

    Args:
        reports (list): Her saniyedeki nesne tespit raporlarını içeren liste.
        output_path (str): Kaydedilecek grafik dosyasının yolu.
        second (int): Çubuk grafiği oluşturulacak saniye.
        threshold (float): Minimum yoğunluk değeri.
    """
    for s, avg_counts in reports:
        if s == second:
            class_names = list(avg_counts.keys())
            counts = [math.ceil(v) if v >= threshold else 0 for v in avg_counts.values()]

            plt.figure(figsize=(10, 6))
            plt.bar(class_names, counts, color="skyblue")
            plt.xlabel("Nesne Sınıfları")
            plt.ylabel("Yoğunluk")
            plt.title(f"Saniye {second} Nesne Yoğunluğu")
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Görseli kaydet
            plt.savefig(output_path)
            plt.close()
            break


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
