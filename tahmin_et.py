import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os

MODEL_PATH = 'alev_radari_model.h5'
IMAGE_WIDTH = 256
IMAGE_HEIGHT = 256

print("Yapay zeka modeli yükleniyor...")

# 1. Model Yükleme Bölümü
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model başarıyla yüklendi.")
except Exception as e:
    print(f"Model yüklenirken hata oluştu: {e}")
    exit(1)

# 2. Tahmin Fonksiyonu
def tahmin_et(image_path):
    try:
        # Resmi yükle ve işle
        img = image.load_img(image_path, target_size=(IMAGE_WIDTH, IMAGE_HEIGHT))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        # Tahmin yap
        predictions = model.predict(img_array)[0][0]
        
        # Sonucu yorumla
        if predictions < 0.5:
            ihtimal = (1 - predictions) * 100
            print(f"SONUÇ: YANGIN TESPİT EDİLDİ! (İhtimal: %{ihtimal:.2f})")
        else:
            ihtimal = predictions * 100
            print(f"SONUÇ: YANGIN TESPİT EDİLMEDİ! (İhtimal: %{ihtimal:.2f})")

    except FileNotFoundError:
        print(f"Hata: '{image_path}' dosyası bulunamadı. Dosya yolunu kontrol edin.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# --- Ana Çalıştırma Bloğu ---
if __name__ == "__main__":
    
    # 1. Kullanıcıdan resim isteme
    resim_yolu = input("Analiz edilecek resmin yolunu girin (örn: yangin.jpg): ")
    if resim_yolu: # Eğer boş basıp geçmezseniz çalışır
        tahmin_et(resim_yolu)

    # 2. Otomatik Testler
    print("\n--- TEST 1: Yangın Görüntüsü ---")
    tahmin_et('test_yangin.jpg')

    print("\n--- TEST 2: Normal Görüntü ---")
    tahmin_et('test_normal.jpg')