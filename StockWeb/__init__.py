import joblib
import tensorflow as tf 
import FinanceDataReader as fdr

model = tf.keras.models.load_model('dataset/Model/StockHelperModel.h5')

print('학습 모델 로딩')

# def kospi(ds, de):
#     kospi = fdr.DataReader('KS11', ds, de)[['Change']] 
#     kospi.rename(columns={'Change' : 'KOSPI'}, inplace=True)
#     return kospi
