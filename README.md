# DWH Ecommerce

Project ini merupakan pipeline sederhana untuk mengambil data dari MySQL, melakukan profiling, transformasi, dan pengecekan kualitas data menggunakan Python, Pandas, dan Parquet.

## Alur project

```text
MySQL
  ↓
01_extract.ipynb / main.py
  ↓
data/extracted
  ↓
02_data_profiling.ipynb
  ↓
03_transform.ipynb
  ↓
data/transformed
  ↓
04_data_checking.ipynb
```

## Prasyarat

Pastikan komputer sudah memiliki:

- Git
- Python 3.10 atau versi yang lebih baru
- MySQL Server
- Akses ke database ecommerce dan tabel staging

Tabel staging yang digunakan antara lain:

- `stg_customers`
- `stg_products`
- `stg_orders`
- `stg_order_items`
- `stg_payments`
- `stg_shipments`
- `stg_returns`
- `stg_customer_reviews`
- `stg_marketing_campaigns`

## Clone repository

```bash
git clone https://github.com/novaandini/dwh_ecommerce.git
cd dwh_ecommerce
```

## Membuat virtual environment

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Jika PowerShell menolak aktivasi script, jalankan PowerShell sebagai user yang sesuai atau gunakan Command Prompt:

```bat
venv\Scripts\activate.bat
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install dependency

Install package yang digunakan project:

```bash
python -m pip install --upgrade pip
python -m pip install pandas SQLAlchemy mysql-connector-python python-dotenv pyarrow jupyter
```

## Konfigurasi koneksi database

Buat file `.env` di root project:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=nama_user_mysql
DB_PASSWORD=password_mysql
DB_NAME=nama_database
```

Sesuaikan nilainya dengan konfigurasi MySQL lokal. Jangan membagikan atau melakukan commit file `.env` karena berisi kredensial database.

## Menjalankan notebook

Jalankan notebook dengan urutan berikut:

### 1. `01_extract.ipynb`

Digunakan untuk membaca konfigurasi `.env`, menguji koneksi MySQL, dan mengambil data dari tabel staging.

### 2. `02_data_profiling.ipynb`

Membaca file Parquet dari `data/extracted` dan melakukan profiling berupa:

- ukuran tabel
- tipe data
- missing value
- nilai unik
- duplicate row
- statistik numerik
- lima nilai kategori yang paling sering muncul

### 3. `03_transform.ipynb`

Menerapkan transformasi dan validasi kualitas data, kemudian menyimpan hasilnya ke:

```text
data/transformed/
```

Notebook ini menambahkan flag audit seperti `age_imputed_flag`, `profit_status`, `payment_validation`, `refund_validation`, dan `delivery_days_corrected_flag`.

### 4. `04_data_checking.ipynb`

Membaca data hasil transformasi dari `data/transformed` dan melakukan pengecekan per tabel. Fungsi yang tersedia:

```python
profiling_table("stg_customers")
statistics_table("stg_customers")
categorical_analysis("stg_customers")
```

Ganti `stg_customers` dengan nama tabel lain untuk memeriksa tabel tersebut.

## Struktur folder

```text
dwh_ecommerce/
├── config/
│   └── database.py
├── data/
│   ├── extracted/
│   └── transformed/
├── extract/
│   └── extract_data.py
├── notebook/
│   ├── 01_extract.ipynb
│   ├── 02_data_profiling.ipynb
│   ├── 03_transform.ipynb
│   └── 04_data_checking.ipynb
├── DATA_PROFILING_FINDINGS.md
├── main.py
├── README.md
└── .env
```

## Troubleshooting

### `ModuleNotFoundError`

Pastikan virtual environment aktif, lalu install dependency kembali:

```bash
python -m pip install pandas SQLAlchemy mysql-connector-python python-dotenv pyarrow jupyter
```

### Gagal koneksi MySQL

Periksa hal berikut:

- MySQL Server sedang berjalan.
- `DB_HOST` dan `DB_PORT` benar.
- Username dan password benar.
- Database pada `DB_NAME` tersedia.
- User MySQL memiliki akses ke tabel staging.

### File Parquet tidak ditemukan

Pastikan notebook dijalankan dari folder `notebook` dan folder berikut tersedia:

```text
data/extracted/
data/transformed/
```

`02_data_profiling.ipynb` membutuhkan data pada `data/extracted`, sedangkan `04_data_checking.ipynb` membutuhkan hasil transformasi pada `data/transformed`.

## Dokumentasi hasil profiling

Temuan anomali dan rekomendasi perbaikannya tersedia di [DATA_PROFILING_FINDINGS.md](DATA_PROFILING_FINDINGS.md).
