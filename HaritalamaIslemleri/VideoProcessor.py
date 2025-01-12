import cv2


class VideoProcessor:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

        # Video açılamaz ise hata mesajı göster
        if not self.cap.isOpened():
            print("Video açılırken bir hata oluştu.")
            return

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        # Video uzunluğunu hesaplama
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.video_duration = self.total_frames / self.fps

        # FPS ve video süresi bilgisini ekrana yazdır rapor olarak
        print(f"-- FPS : {self.fps} , Video süresi : {self.video_duration} saniye --")

    def get_frames_per_second(self):
        # Her saniye için kareleri saklayacak liste
        frames_per_second = []
        current_second = 0  # İlk saniyeye başla

        # Video karelerini sırayla oku
        while True:
            ret, frame = self.cap.read()

            # Video bitmişse döngüyü sonlandır
            if not ret:
                break

            # Hangi saniyede olduğumuzu bul
            second = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES) // self.fps)

            # Yeni bir saniyeye geçildiğinde, önceki saniyeyi kaydedip yeni saniyeye geç
            if second > current_second:
                current_second = second

            # Eğer mevcut saniye listede yoksa yeni bir liste oluştur
            if len(frames_per_second) <= second:
                frames_per_second.append([])

            # Bu saniyeye ait frami listeye ekle
            frames_per_second[second].append(frame)

        return frames_per_second  # Her saniye için karelerin listesini döndür