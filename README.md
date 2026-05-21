# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding

Jaya Jaya Maju adalah perusahaan multinasional yang telah beroperasi sejak tahun 2000 dan memiliki lebih dari 1000 karyawan yang tersebar di berbagai wilayah. Sebagai perusahaan besar, manajemen sumber daya manusia menjadi aspek krusial dalam keberlangsungan operasional perusahaan. Namun, perusahaan saat ini mengalami tantangan serius, yaitu tingginya angka attrition rate (tingkat keluar-masuk karyawan) yang telah melebihi 10%. Tingginya attrition rate ini tidak hanya meningkatkan biaya rekrutmen dan pelatihan, tetapi juga berpotensi mengganggu produktivitas dan kontinuitas operasional.  

Untuk mengatasi masalah ini, departemen Human Resources (HR) perlu memahami faktor-faktor yang memengaruhi keputusan karyawan untuk keluar dari perusahaan. Analisis data karyawan dan visualisasi yang tepat diharapkan dapat membantu pengambilan keputusan strategis dalam upaya menurunkan angka attrition tersebut.

### Permasalahan Bisnis

- Attrition rate perusahaan terlalu tinggi (lebih dari 10%) dan belum diketahui secara pasti faktor-faktor penyebab utamanya.

- Tidak adanya alat bantu visual (dashboard) yang dapat membantu manajer HR memonitor dan menganalisis kondisi karyawan secara efektif.

- Belum terdapat sistem prediktif untuk mengidentifikasi karyawan yang berisiko keluar dari perusahaan lebih awal.

### Cakupan Proyek

- Eksplorasi dan analisis data karyawan berdasarkan berbagai fitur seperti usia, jabatan, pendapatan, kepuasan kerja, dan lainnya untuk mengidentifikasi faktor-faktor yang berpengaruh terhadap attrition.

- Pembuatan business dashboard yang menampilkan visualisasi faktor-faktor kunci yang memengaruhi attrition secara intuitif dan informatif.

- Pengembangan model prediktif machine learning untuk memprediksi kemungkinan seorang karyawan keluar dari perusahaan, sebagai rekomendasi solusi lanjutan.


### Persiapan

Sumber data: [Jaya Jaya Maju Employee](https://github.com/dicodingacademy/dicoding_dataset/tree/main/employee)  
Acknowledgements: [IBM](https://www.ibm.com/communities/analytics/watson-analytics-blog/watson-analytics-use-case-for-hr-retaining-valuable-employees/)  
Deskripsi umum dataset: Dataset ini berisi informasi demografis dan metrik terkait pekerjaan karyawan, serta status attrition (pengunduran diri atau keluar dari perusahaan). Dataset ini umumnya digunakan untuk analisis sumber daya manusia, khususnya untuk memprediksi atau memahami faktor-faktor yang memengaruhi attrition karyawan.

Setup environment:
- Anaconda

```
conda create --name main-ds python=3.12
conda activate main-ds
pip install -r requirements.txt
```

- Shell/Terminal

```
pip install pipenv
pipenv install
pipenv shell
pip install -r requirements.txt
```

Di sini saya menggunakan streamlit untuk membuat dashboard. Saya juga sudah deploy aplikasi dashboard ini ke streamlit dengan integrasi bersama github.  
Berikut link github dari aplikasi ini:  
[Github Dashboard](https://github.com/ivandim123/DS_PA)  
Berikut link dashboard dari aplikasi ini:  
[Streamlit Dashboard](https://kdc4eiy2zazwvrxhjsobsp.streamlit.app/)  

## Business Dashboard
Dashboard yang sudah saya buat memiliki beberapa fitur sebagai berikut:
- Terdapat judul proyek dan beberapa info jika flow dari akses dataset berhasil
- Di sini digunakan 2 buah plot sekaligus yang dipisahkan berdasarkan kolom attrition karena kita ingin menganalisis perbedaan antara karyawan attrition dengan yang tidak
- Plot dapat diubah-ubah berdasarkan filter yang diatur dari sidebar
- Plot akan beradaptasi sesuai jenis fitur yang dipilih, jika dipilih fitur numerik, akan diplot bar grafik dengan line trend, sedangkan untuk fitur kategorikal, akan diplot bar grafik berdasarkan unique value dari masing-masing fitur
- Ada fitur untuk menampilkan raw data dalam tabel (opsional)
- Di bagian bawah juga ada fitur statistik deskriptif dari plot data yang dipilih. Ini juga akan auto adjust jika filter diubah
- Pada sidebar terdapat beberapa info tambahan dan debug info  

Setelah menganalisis dashboard yang telah dibuat, berikut insight dari saya:
- Attrition banyak terjadi pada usia 29 hingga 33 tahun
- Attrition cendrung minimum pada dailyrate 200, 800, dan 1300
- Attrition banyak terjadi dari departemen R&D
- Attrition banyak terjadi karyawan yang rumahnya dekat kantor
- Attrition banyak terjadi pada tingkat edukasi sekitar 3.0
- Attrition banyak terjadi pada bidang edukasi life science
- Attrition banyak terjadi pada karyawan yang tidak puas dengan lingkungan kerjanya
- Attrition banyak terjadi pada karyawan dengan job level yang rendah (sekitar 1.0)
- Attrition banyak terjadi pada jobrole laboratory technician
- Attrition banyak terjadi pada  jobsatisfaction menengah (3.0)
- Attrition banyak terjadi pada mereka yang belum menikah
- Attrition banyak terjadi pada mereka yang memiliki monthly income kecil (sekitar 2500)
- Attrition banyak terjadi pada mereka memiliki performance rate rendah (sekitar 3.0)
- Attrition banyak terjadi pada mereka yang baru beberapa tahun saja di perusahaan (sekitar 1.5 tahun)
- Attrition banyak terjadi pada mereka baru saja dipromosikan (< 1 tahun)

## Conclusion

Melalui proses eksplorasi data, visualisasi interaktif melalui dashboard, serta pengembangan model prediktif berbasis machine learning, proyek ini berhasil mengidentifikasi pola-pola penting yang berkaitan dengan tingginya angka *attrition* (keluar-masuk karyawan) di perusahaan **Jaya Jaya Maju**.

Beberapa faktor utama yang berkontribusi terhadap attrition antara lain:
- Usia muda (29–33 tahun)
- Pendapatan bulanan yang rendah
- Status belum menikah
- Ketidakpuasan terhadap lingkungan kerja
- Job level yang rendah dan baru saja dipromosikan
- Lama bekerja yang masih singkat
- Jabatan seperti **Laboratory Technician**
- Karyawan dari departemen **Research & Development**

Model prediktif yang dibangun menggunakan:
- **Random Forest**  
  - Akurasi data train: 100%  
  - Akurasi data test: 84%
- **Gradient Boosting**  
  - Akurasi data train: 97%  
  - Akurasi data test: 85%

Model ini menunjukkan performa yang cukup baik dan dapat dijadikan sebagai sistem peringatan dini (*early warning system*) oleh tim HR untuk melakukan intervensi terhadap karyawan yang berisiko keluar.

### Rekomendasi Action Items (Optional)

Berikut adalah langkah-langkah yang direkomendasikan untuk mengurangi angka attrition dan meningkatkan retensi karyawan:

### 1. Fokus Retensi pada Usia Muda dan Job Level Rendah
Program mentorship dan pengembangan karier bagi karyawan usia 29–33 tahun, terutama yang berada di level rendah atau baru dipromosikan, perlu diimplementasikan secara sistematis.

### 2. Tinjau Struktur Kompensasi Karyawan Berpendapatan Rendah
Karyawan dengan pendapatan di bawah rata-rata (sekitar 2500) memiliki risiko attrition tinggi. Tinjau ulang skema kompensasi untuk menjaga motivasi dan loyalitas.

### 3. Meningkatkan Kepuasan Lingkungan Kerja
Banyak karyawan merasa tidak puas dengan lingkungan kerja. Inisiatif peningkatan budaya kerja yang kolaboratif dan suportif perlu diadakan secara rutin.

### 4. Perhatikan Karyawan Baru dan yang Baru Dipromosikan
Karyawan dalam dua kategori ini rentan keluar. Onboarding yang lebih komprehensif dan program penyesuaian setelah promosi harus diperkuat.

### 5. Bangun Sistem Prediktif Internal
Integrasikan model prediktif ke dalam sistem HRIS untuk membantu mendeteksi risiko keluar secara otomatis dan memberikan notifikasi dini ke manajemen.

### 6. Kembangkan Program Retensi Berdasarkan Jabatan
Beberapa jabatan seperti **Laboratory Technician** lebih rentan terhadap attrition. Buat jalur karier dan insentif yang relevan sesuai bidang kerja mereka.

### 7. Segmentasi & Intervensi via Dashboard
Gunakan dashboard interaktif untuk memantau data karyawan secara real-time dan lakukan segmentasi untuk menyusun strategi retensi yang lebih efektif dan tepat sasaran.

