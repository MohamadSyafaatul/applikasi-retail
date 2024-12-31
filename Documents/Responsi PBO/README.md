# Sistem Manajemen Ritel

## Gambaran Umum

Sistem Manajemen Ritel adalah aplikasi desktop yang dibangun menggunakan Python dan Tkinter. Aplikasi ini memungkinkan pengguna untuk mengelola produk dan transaksi dalam lingkungan ritel. Pengguna dapat menambah, memperbarui, menghapus produk, dan mencatat transaksi dengan cap waktu.

## Fitur

- **Manajemen Produk**: 
  - Menambah produk baru dengan nama dan harga.
  - Memperbarui produk yang sudah ada.
  - Menghapus produk dari inventaris.
  - Melihat daftar semua produk.

- **Manajemen Transaksi**: 
  - Mencatat transaksi dengan produk yang dipilih dan jumlahnya.
  - Menampilkan total harga dan cap waktu untuk setiap transaksi.



## Cara menjalankan program
1. running program
2. isi inputan
    jika ingin update, delete klik 2 kali data untuk mempercepat inputan
3. jika ingin input add transaction, maka isi juga inputan nama product dan harga product

## Database

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);