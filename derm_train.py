import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, Activation
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.applications import VGG16
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, Activation,GlobalMaxPooling2D
from keras import layers

train_dir="data/train"
test_dir="data/test"


train_datagen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(train_dir, target_size=(224,224), batch_size=20, class_mode="categorical", classes=["Acne and Rosacea Photos",
    "Eczema Photos",
    "Hair Loss Photos Alopecia and other Hair Diseases",
    "Herpes HPV and other STDs Photos",
    "Melanoma Skin Cancer Nevi and Moles",
    "Nail Fungus and other Nail Disease",
    "Psoriasis Pictures Lichen Planus and related Diseases",
    "Scabies Lyme Disease and other Infestations and Bites",
    "Seborrheic Keratoses and other Benign Tumors",
    "Urticaria Hives",
    "Vascular Tumors",
    "Vasculitis Photos"])

validation_generator = test_datagen.flow_from_directory(test_dir, target_size=(224,224), batch_size=20, class_mode="categorical", classes=["Acne and Rosacea Photos",
    "Eczema Photos",
    "Hair Loss Photos Alopecia and other Hair Diseases",
    "Herpes HPV and other STDs Photos",
    "Melanoma Skin Cancer Nevi and Moles",
    "Nail Fungus and other Nail Disease",
    "Psoriasis Pictures Lichen Planus and related Diseases",
    "Scabies Lyme Disease and other Infestations and Bites",
    "Seborrheic Keratoses and other Benign Tumors",
    "Urticaria Hives",
    "Vascular Tumors",
    "Vasculitis Photos"])

input_shape = (224,224,3)

pre_trained_model = VGG16(input_shape=input_shape, include_top=False, weights="imagenet")

for layer in pre_trained_model.layers[:15]:
    layer.trainable = False

for layer in pre_trained_model.layers[15:]:
    layer.trainable = True

last_layer = pre_trained_model.get_layer('block5_pool')
last_output = last_layer.output

x = GlobalMaxPooling2D()(last_output)
x = Dense(512, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(12, activation='softmax')(x)

model = Model(pre_trained_model.input, x)

model.summary()

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(
    train_generator,
    epochs=5,
    validation_data=validation_generator
)

model.save("derm_model.h5")
