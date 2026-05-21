import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set page configuration (harus ditempatkan di awal script)
st.set_page_config(
    page_title="Dashboard HR Analytics",
    layout="wide"
)

# Set style (menggunakan set_theme untuk kompatibilitas versi terbaru)
sns.set_theme(style="whitegrid")

# Judul Dashboard
st.title("Dashboard HR Analytics")
st.markdown("Dashboard ini menampilkan visualisasi data karyawan berdasarkan berbagai fitur dan status attrition.")

# Create sample data if file doesn't exist (untuk testing)
@st.cache_data
def load_or_create_sample_data():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "employee_data_cleaned.csv")
        emp_df = pd.read_csv(file_path)
        st.success("Data berhasil dimuat dari file CSV")

        # Pastikan kolom Attrition memiliki format yang benar
        if 'Attrition' in emp_df.columns:
            if emp_df['Attrition'].dtype in [np.int64, np.float64]:
                st.info("Mengkonversi kolom Attrition dari numerik ke string 'Yes'/'No'")
                emp_df['Attrition'] = emp_df['Attrition'].map({1: 'Yes', 0: 'No'})
            
            valid_values = ['Yes', 'No']
            invalid_mask = ~emp_df['Attrition'].isin(valid_values)
            if invalid_mask.any():
                st.warning(f"Terdapat {invalid_mask.sum()} nilai tidak valid di kolom Attrition. Mengkonversi ke 'No'")
                emp_df.loc[invalid_mask, 'Attrition'] = 'No'

        return emp_df

    except FileNotFoundError:
        st.warning("File 'employee_data_cleaned.csv' tidak ditemukan. Menggunakan data sampel untuk demonstrasi.")

        # Buat data sampel
        np.random.seed(42)
        n = 1000
        genders = ["Male", "Female"]
        departments = ["HR", "Sales", "Engineering", "Finance", "Marketing"]
        education_fields = ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Other"]
        job_roles = ["Sales Executive", "Research Scientist", "Manager", "Healthcare Representative", "Developer"]
        business_travel = ["Travel_Rarely", "Travel_Frequently", "Non-Travel"]

        data = {
            "EmployeeNumber": range(1, n+1),
            "Age": np.random.randint(18, 65, n),
            "Gender": np.random.choice(genders, n),
            "Department": np.random.choice(departments, n),
            "EducationField": np.random.choice(education_fields, n),
            "JobRole": np.random.choice(job_roles, n),
            "BusinessTravel": np.random.choice(business_travel, n),
            "MonthlyIncome": np.random.randint(1000, 20000, n),
            "YearsAtCompany": np.random.randint(0, 20, n),
            "JobSatisfaction": np.random.randint(1, 5, n),
            "WorkLifeBalance": np.random.randint(1, 5, n),
            "DistanceFromHome": np.random.randint(1, 30, n),
            "Attrition": np.random.choice(["Yes", "No"], n, p=[0.16, 0.84])
        }

        return pd.DataFrame(data)

# Load data
emp_df = load_or_create_sample_data()

# Debug information
st.sidebar.subheader("Debug Info")
st.sidebar.write(f"Data shape: {emp_df.shape}")
st.sidebar.write(f"Attrition counts: {emp_df['Attrition'].value_counts().to_dict()}")
st.sidebar.write(f"Attrition dtype: {emp_df['Attrition'].dtype}")

# Sidebar fitur
st.sidebar.header("Pilih Fitur untuk Divisualisasikan")
feature_options = [col for col in emp_df.columns if col not in ["Attrition", "EmployeeNumber", "EmployeeCount", "Over18", "StandardHours"]]
selected_feature = st.sidebar.selectbox("Pilih Fitur:", feature_options, index=0)

# Pisahkan data berdasarkan Attrition
df_0 = emp_df[emp_df["Attrition"] == "No"]
df_1 = emp_df[emp_df["Attrition"] == "Yes"]

# Debug info for separation
st.sidebar.write(f"No Attrition: {len(df_0)} rows")
st.sidebar.write(f"Yes Attrition: {len(df_1)} rows")

# Deteksi tipe fitur
is_numeric = pd.api.types.is_numeric_dtype(emp_df[selected_feature])
st.sidebar.write(f"Feature type: {'Numeric' if is_numeric else 'Categorical'}")

# Fungsi untuk memeriksa apakah data kosong
def is_data_empty(df, column):
    return df[column].count() == 0

# Visualisasi
st.subheader(f"Distribusi Fitur '{selected_feature}' Berdasarkan Attrition")

# Ensuring the figure size is large enough
plt.rcParams["figure.figsize"] = (10, 6)

col1, col2 = st.columns(2)

try:
    # Periksa apakah ada data untuk divisualisasikan
    if is_data_empty(df_0, selected_feature) and is_data_empty(df_1, selected_feature):
        st.error(f"Tidak ada data untuk fitur '{selected_feature}'. Silakan pilih fitur lain.")
    else:
        if is_numeric:
            # Visualisasi histogram berdampingan untuk data numerik
            with col1:
                st.markdown("**Attrition: No**")
                if not is_data_empty(df_0, selected_feature):
                    fig1, ax1 = plt.subplots()
                    sns.histplot(df_0[selected_feature].dropna(), bins=20, kde=True, color="skyblue", ax=ax1)
                    ax1.set_title("No Attrition")
                    ax1.set_xlabel(selected_feature)
                    ax1.set_ylabel("Jumlah")
                    plt.tight_layout()
                    st.pyplot(fig1)
                else:
                    st.info("Tidak ada data untuk 'No Attrition'")
            
            with col2:
                st.markdown("**Attrition: Yes**")
                if not is_data_empty(df_1, selected_feature):
                    fig2, ax2 = plt.subplots()
                    sns.histplot(df_1[selected_feature].dropna(), bins=20, kde=True, color="salmon", ax=ax2)
                    ax2.set_title("Yes Attrition")
                    ax2.set_xlabel(selected_feature)
                    ax2.set_ylabel("Jumlah")
                    plt.tight_layout()
                    st.pyplot(fig2)
                else:
                    st.info("Tidak ada data untuk 'Yes Attrition'")
        else:
            # Visualisasi countplot berdampingan untuk data kategorikal
            with col1:
                st.markdown("**Attrition: No**")
                if not is_data_empty(df_0, selected_feature):
                    fig1, ax1 = plt.subplots()
                    value_counts = df_0[selected_feature].value_counts()
                    if not value_counts.empty:
                        # Menambahkan parameter hue untuk menghindari warning Seaborn
                        sns.countplot(y=selected_feature, data=df_0, 
                                    order=value_counts.index, 
                                    hue=selected_feature, legend=False,
                                    palette="Blues_d", ax=ax1)
                        ax1.set_title("No Attrition")
                        ax1.set_xlabel("Jumlah")
                        plt.tight_layout()
                        st.pyplot(fig1)
                    else:
                        st.info("Tidak ada data kategori untuk 'No Attrition'")
                else:
                    st.info("Tidak ada data untuk 'No Attrition'")
            
            with col2:
                st.markdown("**Attrition: Yes**")
                if not is_data_empty(df_1, selected_feature):
                    fig2, ax2 = plt.subplots()
                    value_counts = df_1[selected_feature].value_counts()
                    if not value_counts.empty:
                        # Menambahkan parameter hue untuk menghindari warning Seaborn
                        sns.countplot(y=selected_feature, data=df_1, 
                                    order=value_counts.index, 
                                    hue=selected_feature, legend=False,
                                    palette="Reds_d", ax=ax2)
                        ax2.set_title("Yes Attrition")
                        ax2.set_xlabel("Jumlah")
                        plt.tight_layout()
                        st.pyplot(fig2)
                    else:
                        st.info("Tidak ada data kategori untuk 'Yes Attrition'")
                else:
                    st.info("Tidak ada data untuk 'Yes Attrition'")
        
except Exception as e:
    st.error(f"Error saat membuat visualisasi: {e}")
    st.write("Detail error:")
    st.exception(e)

# Tampilkan data mentah (opsional)
if st.checkbox("Tampilkan Data Mentah"):
    st.dataframe(emp_df[[selected_feature, "Attrition"]])

# Tambahkan statistik deskriptif
st.subheader("Statistik Deskriptif")
if is_numeric:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Attrition: No**")
        if not is_data_empty(df_0, selected_feature):
            st.write(df_0[selected_feature].describe())
        else:
            st.info("Tidak ada data untuk dianalisis")
    with col2:
        st.markdown("**Attrition: Yes**")
        if not is_data_empty(df_1, selected_feature):
            st.write(df_1[selected_feature].describe())
        else:
            st.info("Tidak ada data untuk dianalisis")
else:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Attrition: No**")
        if not is_data_empty(df_0, selected_feature):
            st.write(df_0[selected_feature].value_counts().reset_index())
        else:
            st.info("Tidak ada data untuk dianalisis")
    with col2:
        st.markdown("**Attrition: Yes**")
        if not is_data_empty(df_1, selected_feature):
            st.write(df_1[selected_feature].value_counts().reset_index())
        else:
            st.info("Tidak ada data untuk dianalisis")
