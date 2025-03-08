import pytest
import torch
import numpy as np
from app.models.AI.LSTM import LSTM, LSTMModel

def test_lstm_forward_binary():
    """
    تست forward در حالت دسته‌بندی باینری (output_size = 1).
    انتظار داریم خروجی دارای شکل [batch_size, 1] بوده و مقدار آن بین 0 و 1 باشد (به دلیل استفاده از sigmoid).
    """
    input_size = 10
    output_size = 1  # باینری
    batch_size = 4
    seq_len = 5
    model = LSTM(input_size, output_size)
    x = torch.randn(batch_size, seq_len, input_size)
    y = model(x)
    # بررسی شکل خروجی
    assert y.shape == (batch_size, output_size)
    # بررسی اینکه خروجی به دلیل تابع sigmoid بین 0 و 1 باشد
    assert torch.all((y >= 0) & (y <= 1))

def test_lstm_forward_multiclass():
    """
    تست forward در حالت دسته‌بندی چندکلاسه (output_size > 1).
    انتظار داریم خروجی دارای شکل [batch_size, output_size] بوده و هر سطر (sample) مجموع احتمال برابر با 1 داشته باشد.
    """
    input_size = 10
    output_size = 3  # چندکلاسه
    batch_size = 4
    seq_len = 5
    model = LSTM(input_size, output_size)
    x = torch.randn(batch_size, seq_len, input_size)
    y = model(x)
    # بررسی شکل خروجی
    assert y.shape == (batch_size, output_size)
    # بررسی مجموع احتمالات هر نمونه (سطر) برابر با 1 (با تحمل خطای کوچک)
    row_sums = y.sum(dim=1)
    np.testing.assert_allclose(row_sums.cpu().detach().numpy(), np.ones(batch_size), rtol=1e-5)

def test_lstmmodel_initialization_unit():
    """
    تست اولیه‌سازی کلاس LSTMModel.
    بررسی می‌کنیم که:
    - مدل زیرین به درستی از نوع LSTM است.
    - پارامترهای مدل روی دستگاه مناسب (CPU یا CUDA) قرار دارند.
    """
    input_size = 10
    output_size = 1
    model_instance = LSTMModel(output_size=output_size, input_size=input_size)
    # بررسی نام کلاس مدل زیرین
    assert model_instance.model.__class__.__name__ == 'LSTM'
    # بررسی اینکه پارامترهای مدل روی دستگاه معتبر (cpu یا cuda) هستند
    for param in model_instance.model.parameters():
        assert param.device.type in ['cpu', 'cuda']
