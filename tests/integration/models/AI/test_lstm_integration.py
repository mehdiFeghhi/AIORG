import pytest
import numpy as np
import torch
from app.models.AI.LSTM import LSTMModel

@pytest.fixture
def binary_seq_data():
    """
    Fixture تولید داده‌های دنباله‌ای (sequence data) برای دسته‌بندی باینری.
    - X: داده‌های ورودی با شکل [samples, seq_len, input_size]
    - y: برچسب‌های باینری
    """
    input_size = 10
    seq_len = 5
    X_train = np.random.rand(100, seq_len, input_size).astype(np.float32)
    y_train = np.random.randint(0, 2, 100).astype(np.float32)
    X_test = np.random.rand(20, seq_len, input_size).astype(np.float32)
    y_test = np.random.randint(0, 2, 20).astype(np.float32)
    return X_train, y_train, X_test, y_test, input_size

def test_lstmmodel_training_prediction_evaluation(binary_seq_data):
    """
    تست یکپارچه LSTMModel:
    - آموزش مدل با داده‌های آموزش.
    - پیش‌بینی روی داده‌های تست.
    - ارزیابی مدل (بررسی دقت خروجی در بازه [0, 1]).
    """
    X_train, y_train, X_test, y_test, input_size = binary_seq_data
    # مقداردهی اولیه مدل برای دسته‌بندی باینری
    model = LSTMModel(output_size=1, input_size=input_size)
    
    # آموزش مدل به مدت 1 epoch (برای سرعت تست)
    model.train(X_train, y_train, epochs=1, batch_size=16, learning_rate=0.01)
    
    # پیش‌بینی روی داده‌های تست
    preds = model.predict(X_test)
    # بررسی تعداد پیش‌بینی‌ها برابر با تعداد نمونه‌های تست
    assert preds.shape[0] == X_test.shape[0]
    
    # ارزیابی مدل و بررسی اینکه دقت خروجی در بازه [0, 1] باشد
    acc = model.evaluate(X_test, y_test)
    assert 0 <= acc <= 1
