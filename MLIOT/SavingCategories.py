import scipy.io
import numpy as n
from tensorflow.keras.preprocessing.image import ImageDataGenerator






base_dir = '/Users/aryaman/IOTProject'  



datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = datagen.flow_from_directory(
    base_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical',
    subset='training')

categories = list(train_generator.class_indices.keys())
category_indices = {category: i for i, category in enumerate(categories)}

scipy.io.savemat('waste_categories.mat', {'category_indices': category_indices})
import tensorflow as tf; print(tf.__version__)