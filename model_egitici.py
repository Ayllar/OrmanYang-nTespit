import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import matplotlib.pyplot as plt

IMAGE_WIDTH = 256
IMAGE_HEIGHT = 256
BATCH_SIZE = 32
DATASET_DIR = 'fire_dataset'

train_datagen = ImageDataGenerator(
    rescale = 1./255,
    validation_split = 0.2,
    rotation_range = 20,
    width_shift_range = 0.2,
    height_shift_range = 0.2,
    horizontal_flip = True
)

train_generator = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size = (IMAGE_HEIGHT, IMAGE_WIDTH),
    batch_size = BATCH_SIZE,
    class_mode = 'binary',
    subset = 'training'
)
# --- EKSİK OLAN KISIM (Görselde atlanmış ama gerekli) ---
validation_generator = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(IMAGE_HEIGHT, IMAGE_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='validation'
)
# --------------------------------------------------------

# Görseldeki Kodun Başlangıcı
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_HEIGHT, IMAGE_WIDTH, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

print("\nModel Eğitimi başlıyor... Bu işlem biraz zaman alabilir...")

history = model.fit(train_generator, epochs=15, validation_data=validation_generator)

model.save('alev_radari_model.h5')

print("\nEğitim tamamlandı ve model alev_radari_model.h5 olarak kaydedildi.")

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(15)

plt.figure(figsize=(15, 7))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Eğitim Doğruluğu')
plt.savefig('egitim_dogrulugu.png')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Eğitim Kaybı')
plt.plot(epochs_range, val_loss, label='Doğrulama Kaybı')
plt.legend(loc='upper right')
plt.title('Eğitim ve Doğrulama Kaybı')
plt.savefig('egitim_kaybi.png')
print("Eğitim grafiği 'egitim_grafigi.png' adıyla ana klasöre kaydedildi. ")
