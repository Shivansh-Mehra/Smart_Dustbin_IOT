import tensorflow as tf
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping

# Hyperparameters
learning_rate = 0.0001
batch_size = 32
epochs = 20
dropout_rate = 0.5
image_size = (224, 224)

# Load the pre-trained DenseNet121 model without the top layer
base_model = DenseNet121(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze the layers of DenseNet121
for layer in base_model.layers:
    layer.trainable = False

# Add custom layers on top of DenseNet121
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(dropout_rate)(x)  # Dropout layer to prevent overfitting
x = Dense(512, activation='relu')(x)  # Fully connected layer
predictions = Dense(4, activation='softmax')(x)  # Output layer for 4 classes

# Create the model
model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
              loss='categorical_crossentropy', metrics=['accuracy'])

# Data augmentation for training data
train_datagen = ImageDataGenerator(rescale=1./255,
                                   rotation_range=20,
                                   width_shift_range=0.1,
                                   height_shift_range=0.1,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True,
                                   fill_mode='nearest')

# Load the training data
train_generator = train_datagen.flow_from_directory('path_to_train_data',
                                                    target_size=image_size,
                                                    batch_size=batch_size,
                                                    class_mode='categorical')

# Data generator for validation data
val_datagen = ImageDataGenerator(rescale=1./255)
validation_generator = val_datagen.flow_from_directory('path_to_val_data',
                                                       target_size=image_size,
                                                       batch_size=batch_size,
                                                       class_mode='categorical')

# Early stopping to prevent overfitting
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Train the model
history = model.fit(train_generator,
                    validation_data=validation_generator,
                    epochs=epochs,
                    steps_per_epoch=train_generator.samples // batch_size,
                    validation_steps=validation_generator.samples // batch_size,
                    callbacks=[early_stopping])

# Save the trained model
model.save('garbage_segmentation_model.h5')