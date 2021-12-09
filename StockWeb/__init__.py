import joblib
import tensorflow as tf 

model = tf.keras.models.load_model('dataset/Model/StockHelperModel.h5')

print('학습 모델 로딩')