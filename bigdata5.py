import streamlit as st
from pymongo import MongoClient

# Koneksi ke MongoDB Atlas
client = MongoClient("mongodb+srv://muhammadanbiyati23:QqyQWt2Zxx693CaR@bigdata-anbiya.vfjsm.mongodb.net/?retryWrites=true&w=majority&appName=bigdata-anbiya")
db = client["TokoOnline"]  
collection = db["KatalogElektronik"]  
collection2 = db["KatalogMenuAyamBunut"]  

# Judul Aplikasi
st.title("Manajemen Katalog Produk")

# Keterangan Kelompok
st.markdown("""
### Kelompok 2 - Big Data TI23F
**Anggota Kelompok:**
- **Muhammad Anbiya Fatah** - 20230040289
- **Mughis Fadhil A. Ridwan** - 20230040217
- **Muhammad Daniel Surya** - 20230040155
- **Rassya Ramadhani Priadi** - 20230040142
""")

# Pilihan Menu
menu = st.sidebar.radio("Pilih Kategori", ["Elektronik", "Katalog Makanan"])

if menu == "Elektronik":
    st.header("Tambah / Update Stok Produk Elektronik")

    with st.form("form_tambah_produk"):
        nama_produk = st.text_input("Nama Produk")
        harga = st.number_input("Harga", min_value=0)
        stok_tambah = st.number_input("Tambah Stok", min_value=0)

        st.subheader("Spesifikasi Produk")
        spesifikasi_keys = []
        spesifikasi_values = []

        for i in range(1, 6):
            col1, col2 = st.columns(2)
            with col1:
                spesifikasi_keys.append(st.text_input(f"Spesifikasi Tambahan {i}", key=f"spesifikasi_{i}"))
            with col2:
                spesifikasi_values.append(st.text_input(f"Keterangan Spesifikasi {i}", key=f"nilai_{i}"))

        spesifikasi = {key: value for key, value in zip(spesifikasi_keys, spesifikasi_values) if key and value}

        submit = st.form_submit_button("Simpan")

        if submit:
            if nama_produk and harga > 0 and stok_tambah >= 0:
                existing_product = collection.find_one({"nama": nama_produk})

                if existing_product:
                    new_stok = existing_product["stok"] + stok_tambah
                    update_data = {"stok": new_stok, "harga": harga}
                    if spesifikasi:
                        update_data["spesifikasi"] = spesifikasi

                    collection.update_one(
                        {"nama": nama_produk},
                        {"$set": update_data}
                    )
                    st.success(f"✅ Stok produk '{nama_produk}' berhasil ditambahkan! Stok sekarang: {new_stok}")
                else:
                    data_produk = {
                        "nama": nama_produk,
                        "harga": harga,
                        "stok": stok_tambah,
                        "spesifikasi": spesifikasi if spesifikasi else None
                    }
                    collection.insert_one(data_produk)
                    st.success(f"✅ Produk baru '{nama_produk}' berhasil ditambahkan!")
            else:
                st.error("❌ Mohon isi semua data dengan benar!")

elif menu == "Katalog Makanan":
    st.header("Tambah / Update Menu Makanan")

    kategori_menu = st.selectbox(
        "Pilih Kategori Menu",
        [
            "Menu Ayam",
            "Menu Ikan",
            "Menu Daging",
            "Tumis atau Pepes",
            "Menu Tradisional",
            "Mie & Nasi Goreng",
            "Menu Kudapan",
            "Menu Minuman",
            "Menu Varian Es",
            "Menu Varian Jus",
            "Kopi Bunut"
        ]
    )

    with st.form("form_tambah_menu"):
        nama_menu = st.text_input("Nama Menu")
        harga_menu = st.number_input("Harga Menu", min_value=0)
        keterangan_pesanan = st.text_area("Keterangan Pesanan")

        submit_menu = st.form_submit_button("Simpan")

        if submit_menu:
            if nama_menu and harga_menu > 0:
                existing_menu = collection2.find_one({"nama": nama_menu, "kategori": kategori_menu})

                if existing_menu:
                    collection2.update_one(
                        {"nama": nama_menu, "kategori": kategori_menu},
                        {"$set": {"harga": harga_menu}}
                    )
                    st.success(f"✅ Menu '{nama_menu}' di kategori '{kategori_menu}' berhasil diperbarui dengan harga {harga_menu}!")
                else:
                    data_menu = {
                        "kategori": kategori_menu,
                        "nama": nama_menu,
                        "harga": harga_menu,
                        "keterangan": keterangan_pesanan
                    }
                    collection2.insert_one(data_menu)
                    st.success(f"✅ Menu baru '{nama_menu}' berhasil ditambahkan di kategori '{kategori_menu}'!")
            else:
                st.error("❌ Mohon isi semua data dengan benar!")
