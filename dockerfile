FROM python:3.12-slim

# نصب ابزارهای لازم برای نصب برخی پکیج‌ها مثل psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ساخت دایرکتوری کاری
WORKDIR /app

# کپی کردن فایل‌های موردنیاز
COPY requirements.txt .
COPY packages/ ./packages/

# نصب پکیج‌ها با استفاده از wheelها (فقط لوکال، بدون اینترنت)
RUN pip install --no-index --find-links=packages -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
