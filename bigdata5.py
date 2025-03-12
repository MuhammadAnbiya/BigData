import streamlit as st
from pymongo import MongoClient

# Koneksi ke MongoDB Atlas
client = MongoClient("mongodb+srv://muhammadanbiyati23:QqyQWt2Zxx693CaR@bigdata-anbiya.vfjsm.mongodb.net/?retryWrites=true&w=majority&appName=bigdata-anbiya")
db = client["TokoOnline"]  # Nama database
collection = db["KatalogElektronik"]  # Nama koleksi

# Judul Aplikasi
st.title("Tambah / Update Stok Produk")

# Form Input Produk
with st.form("form_tambah_produk"):
    nama_produk = st.text_input("Nama Produk")
    harga = st.number_input("Harga", min_value=0)
    kategori = st.selectbox("Kategori", ["Elektronik", "Pakaian", "Makanan", "Lainnya"])
    stok_tambah = st.number_input("Tambah Stok", min_value=0)

    # Tombol Simpan
    submit = st.form_submit_button("Simpan")

    if submit:
        if nama_produk and harga > 0 and stok_tambah >= 0:
            # Cek apakah produk sudah ada di database
            existing_product = collection.find_one({"nama": nama_produk})

            if existing_product:
                # Jika produk sudah ada, update stok
                new_stok = existing_product["stok"] + stok_tambah
                collection.update_one(
                    {"nama": nama_produk},
                    {"$set": {"stok": new_stok, "harga": harga, "kategori": kategori}}
                )
                st.success(f"✅ Stok produk '{nama_produk}' berhasil ditambahkan! Stok sekarang: {new_stok}")
            else:
                # Jika produk belum ada, tambahkan baru
                data_produk = {
                    "nama": nama_produk,
                    "harga": harga,
                    "kategori": kategori,
                    "stok": stok_tambah
                }
                collection.insert_one(data_produk)
                st.success(f"✅ Produk baru '{nama_produk}' berhasil ditambahkan!")

        else:
            st.error("❌ Mohon isi semua data dengan benar!")
