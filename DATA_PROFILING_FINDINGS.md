# Ringkasan Anomali Data dan Perbaikan

Dokumen ini merangkum hasil profiling data pada file `notebook/02_data_profiling.ipynb` dan data Parquet di `data/extracted`.

## Ringkasan umum

- Tidak ditemukan duplicate row pada seluruh tabel.
- Tidak ditemukan orphan foreign key pada relasi utama antar tabel.
- Anomali utama berkaitan dengan missing value, konsistensi nilai turunan, profit negatif, dan sinkronisasi status.

## `stg_customers`

Anomali:

- `age` kosong pada 250 baris.
- `preferred_device` kosong pada 125 baris.
- `last_order_date` kosong pada 2.300 baris.
- 2.300 customer berstatus `Never Purchased` memiliki `total_orders`, `total_spend`, dan `average_order_value` bernilai 0.
- `age` kosong, tetapi `age_group` tetap terisi.

Perbaikan:

- Pertahankan `last_order_date = NULL` untuk customer yang belum pernah membeli.
- Pastikan metrik transaksi customer `Never Purchased` bernilai 0.
- Isi `age` dengan hasil imputasi atau label `Unknown`.
- Hitung ulang `age_group` dari `age`; gunakan `Unknown` jika umur tidak tersedia.
- Isi `preferred_device` yang kosong dengan `Unknown` jika data memang tidak tersedia.

## `stg_customer_reviews`

Anomali:

- `review_sentiment` kosong pada 233 baris.
- Terdapat konsentrasi 3.499 review pada 31 Desember 2025 yang perlu divalidasi.

Perbaikan:

- Isi sentiment berdasarkan rating: rating 1–2 menjadi `Negative`, rating 3 menjadi `Neutral`, dan rating 4–5 menjadi `Positive`.
- Periksa apakah lonjakan tanggal 31 Desember berasal dari batch import atau kesalahan tanggal.

## `stg_marketing_campaigns`

Anomali:

- Sembilan campaign memiliki ROI negatif.
- ROI terendah adalah -0,6.

Perbaikan:

- Jangan menghapus campaign tersebut karena dapat menunjukkan campaign yang benar-benar merugi.
- Validasi `campaign_cost`, `revenue_generated`, dan rumus ROI.
- Tandai campaign tersebut sebagai `Underperforming` atau `Loss Making`.
- Rumus ROI saat ini konsisten dengan `(revenue_generated - campaign_cost) / campaign_cost`.

## `stg_orders`

Anomali:

- `coupon_code` kosong pada 33.711 baris.
- `campaign_id` kosong pada 82.821 baris.
- `discount_percentage` tidak tercermin pada `final_amount`.
- Jika diskon diterapkan ulang, 68.808 baris tidak sesuai.
- `final_amount` konsisten dengan `subtotal + shipping_fee + tax_amount`.

Perbaikan:

- Jika coupon dan campaign bersifat opsional, gunakan label `No Coupon` dan `No Campaign` saat analisis.
- Klarifikasi apakah `subtotal` sudah merupakan nilai setelah diskon.
- Jika belum, hitung ulang `final_amount` dengan menerapkan diskon.
- Dokumentasikan definisi kolom agar diskon tidak dihitung dua kali.

## `stg_order_items`

Anomali:

- `profit` negatif pada 37.838 item.
- Profit terendah sekitar -108.249,36.
- Tidak ditemukan missing value, duplicate key, atau foreign key yang tidak cocok.

Perbaikan:

- Validasi `unit_price`, `item_cost`, `quantity`, dan diskon.
- Bedakan kerugian bisnis yang valid dari kesalahan perhitungan.
- Tandai item dengan profit negatif sebagai `Loss Making Item`.

## `stg_payments`

Tidak ditemukan anomali struktural:

- Tidak ada missing value.
- `payment_id` unik.
- Tidak ada orphan `order_id`.
- Nilai nol konsisten dengan status `Failed`, `Pending`, dan `Not Charged`.
- `refund_amount` hanya muncul pada pembayaran `Refunded`.

Validasi yang disarankan:

- `Success` harus memiliki `amount_paid > 0`.
- `Failed`, `Pending`, dan `Not Charged` harus memiliki `amount_paid = 0`.
- `Refunded` harus memiliki `refund_amount > 0`.

## `stg_products`

Anomali:

- `rating_average` kosong pada 4 baris.
- Satu produk memiliki `rating_count = 0`, tetapi memiliki rating.
- Dua produk memiliki nama `Morar Basic Art Supplie` dengan `product_id` berbeda.

Perbaikan:

- Jika `rating_count = 0`, ubah `rating_average` menjadi `NULL`.
- Isi rating kosong berdasarkan data review atau biarkan `NULL`.
- Validasi apakah nama yang sama merupakan varian berbeda.
- Jika bukan varian, lakukan standardisasi atau deduplikasi nama produk.

## `stg_returns`

Anomali:

- `refund_amount = 0` pada 1.810 baris.
- Sebanyak 5.394 return terhubung ke order dengan status selain `Returned`.

Perbaikan:

- `Pending` dan `Rejected` boleh memiliki refund 0.
- `Refund Completed` harus memiliki refund lebih besar dari 0.
- Sinkronkan status order dengan status return, atau dokumentasikan bahwa order dapat tetap `Delivered` selama proses return.
- Pertimbangkan lifecycle status terpisah untuk order dan return.

## `stg_shipments`

Anomali:

- `actual_delivery_date` dan `delivery_days` kosong pada 2.321 baris.
- Seluruh baris tersebut berstatus `Cancelled in Transit`, sehingga kemungkinan besar valid.
- `delivery_days` tidak sesuai dengan selisih `actual_delivery_date - dispatch_date` pada 910 baris.

Perbaikan:

- Pertahankan tanggal kosong untuk pengiriman yang dibatalkan.
- Hitung ulang `delivery_days` dari tanggal dispatch dan actual delivery.
- Jika menggunakan hari kerja, dokumentasikan aturan perhitungannya.
- Validasi ulang 910 baris yang tidak sesuai.

## Prioritas perbaikan

1. Klarifikasi dan perbaiki penerapan diskon pada `stg_orders`.
2. Investigasi profit negatif pada `stg_order_items`.
3. Perbaiki perhitungan `delivery_days` pada `stg_shipments`.
4. Tangani missing value pada `stg_customers` dan `stg_customer_reviews`.
5. Sinkronkan status return dengan status order.

