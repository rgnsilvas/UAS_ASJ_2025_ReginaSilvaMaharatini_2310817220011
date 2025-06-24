# Gunakan image python resmi
FROM python:3.12-slim

# Set working directory di dalam container
WORKDIR /app

# Salin file requirements.txt dan install dependensi
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Salin semua isi folder lokal ke folder /app di container
COPY . .

# Jalankan aplikasi
CMD ["python", "app.py"]
