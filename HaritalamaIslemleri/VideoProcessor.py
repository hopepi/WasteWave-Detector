import cv2


class VideoProcessor:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

        if not self.cap.isOpened():
            print("Video açılırken bir hata oluştu.")
            return

        # Videonun FPS değerini al
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

        # Videonun toplam kare sayısını al
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Videonun toplam süresini hesapla saniye cinsinden
        self.video_duration = self.total_frames / self.fps

        # FPS ve video süresi bilgisini ekrana yazdır
        print(f"-- FPS : {self.fps} , Video süresi : {self.video_duration} saniye --")

    def get_frames_per_second(self):
        """
        Her saniye için kareleri ayırır ve liste olarak döndürür her saniyenin karelerini alır ve eşitleme işlemi yapar

        Örneğin ilk 25 kare 1 saniyenin 25 kare ve 50 kare arası 2 saniyenin vs.
        """
        # Her saniye için kareleri saklayacak listeyi başlat
        frames_per_second = []
        current_second = 0  # İşlemeye ilk saniyeden başla

        # Video karelerini sırayla oku
        while True:
            ret, frame = self.cap.read()  # Bir kare oku

            # Video bitmişse döngüyü sonlandır
            if not ret:
                break

            # Hangi saniyede olduğumuzu hesapla
            second = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES) // self.fps)

            # Yeni bir saniyeye geçildiğinde, current_second değerini güncelle
            if second > current_second:
                current_second = second

            # Eğer mevcut saniye listede yoksa yeni bir alt liste oluştur
            if len(frames_per_second) <= second:
                frames_per_second.append([])

            # Bu saniyeye ait framei ilgili listeye ekle
            frames_per_second[second].append(frame)

        # Her saniyeye ait karelerin listesini döndür
        return frames_per_second
