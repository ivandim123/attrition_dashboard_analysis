import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="👥",
    layout="wide",
)

# ── Theme ─────────────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid")
COLOR_NO  = "#4A90D9"   # blue  → No Attrition
COLOR_YES = "#E05C5C"   # red   → Yes Attrition
PALETTE   = {"No": COLOR_NO, "Yes": COLOR_YES}

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 20px 24px;
        border-left: 5px solid #4A90D9;
        margin-bottom: 8px;
        min-height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-card.danger { border-left-color: #E05C5C; }
    .metric-label { font-size: 13px; color: #6c757d; margin-bottom: 4px; }
    .metric-value { font-size: 28px; font-weight: 700; color: #1a1a2e; }
    .metric-sub   { font-size: 12px; color: #6c757d; margin-top: 2px; min-height: 18px; }
    section[data-testid="stSidebar"] { background: #1a1a2e; }
    section[data-testid="stSidebar"] * { color: #e0e0e0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Data loader ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, "employee_data_cleaned.csv")
        df = pd.read_csv(path)
        if "Attrition" in df.columns:
            if df["Attrition"].dtype in [np.int64, np.float64]:
                df["Attrition"] = df["Attrition"].map({1: "Yes", 0: "No"})
            df["Attrition"] = df["Attrition"].where(df["Attrition"].isin(["Yes", "No"]), "No")
        return df, True
    except FileNotFoundError:
        return _sample_data(), False

def _sample_data():
    np.random.seed(42)
    n = 1000
    return pd.DataFrame({
        "EmployeeNumber":  range(1, n + 1),
        "Age":             np.random.randint(22, 60, n),
        "Gender":          np.random.choice(["Male", "Female"], n),
        "Department":      np.random.choice(["HR", "Sales", "Engineering", "Finance", "Marketing"], n),
        "EducationField":  np.random.choice(["Life Sciences", "Medical", "Marketing", "Technical Degree", "Other"], n),
        "JobRole":         np.random.choice(["Sales Executive", "Research Scientist", "Manager", "HR Rep", "Developer"], n),
        "BusinessTravel":  np.random.choice(["Travel_Rarely", "Travel_Frequently", "Non-Travel"], n),
        "MonthlyIncome":   np.random.randint(2000, 20000, n),
        "YearsAtCompany":  np.random.randint(0, 20, n),
        "JobSatisfaction": np.random.randint(1, 5, n),
        "WorkLifeBalance": np.random.randint(1, 5, n),
        "DistanceFromHome":np.random.randint(1, 30, n),
        "OverTime":        np.random.choice(["Yes", "No"], n, p=[0.28, 0.72]),
        "Attrition":       np.random.choice(["Yes", "No"], n, p=[0.16, 0.84]),
    })

emp_df, from_file = load_data()

EXCLUDE_COLS = {"Attrition", "EmployeeNumber", "EmployeeCount", "Over18", "StandardHours"}
feature_options = [c for c in emp_df.columns if c not in EXCLUDE_COLS]

df_no  = emp_df[emp_df["Attrition"] == "No"]
df_yes = emp_df[emp_df["Attrition"] == "Yes"]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 👥 HR Analytics")
    st.markdown("---")
    if not from_file:
        st.warning("⚠️ Menggunakan data sampel.\nLetakkan `employee_data_cleaned.csv` di folder yang sama untuk data nyata.")
    st.markdown("### 🔍 Eksplorasi Fitur")
    selected_feature = st.selectbox("Pilih Fitur:", feature_options)
    st.markdown("---")
    st.markdown("### 🎛️ Filter")
    if "Department" in emp_df.columns:
        all_depts = ["Semua"] + sorted(emp_df["Department"].unique().tolist())
        dept_filter = st.selectbox("Departemen:", all_depts)
        if dept_filter != "Semua":
            emp_df  = emp_df[emp_df["Department"] == dept_filter]
            df_no   = emp_df[emp_df["Attrition"] == "No"]
            df_yes  = emp_df[emp_df["Attrition"] == "Yes"]

# ── Header ────────────────────────────────────────────────────────────────────
st.title("📊 Dashboard HR Analytics")
st.caption("Analisis attrition karyawan berdasarkan berbagai faktor demografis & pekerjaan.")
st.divider()

# ── KPI Metrics ───────────────────────────────────────────────────────────────
total       = len(emp_df)
n_attrition = len(df_yes)
rate        = n_attrition / total * 100 if total else 0
avg_income  = emp_df["MonthlyIncome"].mean() if "MonthlyIncome" in emp_df.columns else None
avg_tenure  = emp_df["YearsAtCompany"].mean() if "YearsAtCompany" in emp_df.columns else None

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Total Karyawan</div>
        <div class="metric-value">{total:,}</div>
        <div class="metric-sub">&nbsp;</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class="metric-card danger">
        <div class="metric-label">Attrition Rate</div>
        <div class="metric-value">{rate:.1f}%</div>
        <div class="metric-sub">{n_attrition:,} karyawan keluar</div>
    </div>""", unsafe_allow_html=True)
with k3:
    val = f"Rp {avg_income:,.0f}" if avg_income else "—"
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Rata-rata Gaji/Bulan</div>
        <div class="metric-value" style="font-size:22px">{val}</div>
        <div class="metric-sub">&nbsp;</div>
    </div>""", unsafe_allow_html=True)
with k4:
    val = f"{avg_tenure:.1f} thn" if avg_tenure else "—"
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Rata-rata Lama Kerja</div>
        <div class="metric-value">{val}</div>
        <div class="metric-sub">&nbsp;</div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ── Attrition Overview (donut + bar by dept) ─────────────────────────────────
st.subheader("🔎 Overview Attrition")
ov1, ov2 = st.columns([1, 2])

with ov1:
    fig, ax = plt.subplots(figsize=(4, 4))
    sizes  = [len(df_no), len(df_yes)]
    colors = [COLOR_NO, COLOR_YES]
    wedges, texts, autotexts = ax.pie(
        sizes, labels=["No", "Yes"], colors=colors,
        autopct="%1.1f%%", startangle=90,
        wedgeprops=dict(width=0.55, edgecolor="white"),
        textprops=dict(fontsize=12),
    )
    for at in autotexts:
        at.set_fontsize(11)
        at.set_fontweight("bold")
    ax.set_title("Komposisi Attrition", fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with ov2:
    if "Department" in emp_df.columns:
        dept_atr = emp_df.groupby(["Department", "Attrition"]).size().reset_index(name="count")
        dept_tot = emp_df.groupby("Department").size().reset_index(name="total")
        dept_atr = dept_atr.merge(dept_tot, on="Department")
        dept_atr["pct"] = dept_atr["count"] / dept_atr["total"] * 100

        fig, ax = plt.subplots(figsize=(7, 4))
        dept_yes = dept_atr[dept_atr["Attrition"] == "Yes"].sort_values("pct", ascending=True)
        bars = ax.barh(dept_yes["Department"], dept_yes["pct"], color=COLOR_YES, edgecolor="white")
        ax.bar_label(bars, fmt="%.1f%%", padding=4, fontsize=10)
        ax.set_xlabel("Attrition Rate (%)", fontsize=10)
        ax.set_title("Attrition Rate per Departemen", fontsize=13, fontweight="bold")
        ax.set_xlim(0, dept_yes["pct"].max() * 1.25)
        sns.despine(left=True, bottom=True)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    else:
        st.info("Kolom 'Department' tidak tersedia.")

st.divider()

# ── Feature Deep-dive ─────────────────────────────────────────────────────────
st.subheader(f"🔬 Distribusi: `{selected_feature}` vs Attrition")
is_numeric = pd.api.types.is_numeric_dtype(emp_df[selected_feature])

if is_numeric:
    # Side-by-side histogram + combined KDE
    left, right = st.columns(2)

    with left:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(df_no[selected_feature].dropna(),  bins=20, kde=True, color=COLOR_NO,  label="No",  alpha=0.6, ax=ax)
        sns.histplot(df_yes[selected_feature].dropna(), bins=20, kde=True, color=COLOR_YES, label="Yes", alpha=0.6, ax=ax)
        ax.set_title(f"Distribusi {selected_feature}", fontsize=12, fontweight="bold")
        ax.set_xlabel(selected_feature)
        ax.set_ylabel("Jumlah")
        ax.legend(title="Attrition")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with right:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=emp_df, x="Attrition", y=selected_feature,
                    palette=PALETTE, order=["No", "Yes"], width=0.5, ax=ax)
        ax.set_title(f"Boxplot {selected_feature} per Attrition", fontsize=12, fontweight="bold")
        ax.set_xlabel("Attrition")
        ax.set_ylabel(selected_feature)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # Descriptive stats
    st.markdown("**Statistik Deskriptif**")
    stats_no  = df_no[selected_feature].describe().rename("No Attrition")
    stats_yes = df_yes[selected_feature].describe().rename("Yes Attrition")
    st.dataframe(pd.concat([stats_no, stats_yes], axis=1).style.format("{:.2f}"), use_container_width=True)

else:
    # Grouped count + percentage
    counts = emp_df.groupby([selected_feature, "Attrition"]).size().reset_index(name="count")
    totals = emp_df.groupby(selected_feature).size().reset_index(name="total")
    counts = counts.merge(totals, on=selected_feature)
    counts["pct"] = counts["count"] / counts["total"] * 100

    left, right = st.columns(2)
    with left:
        fig, ax = plt.subplots(figsize=(6, max(4, len(emp_df[selected_feature].unique()) * 0.5)))
        order = emp_df[selected_feature].value_counts().index
        sns.countplot(y=selected_feature, hue="Attrition", data=emp_df,
                      order=order, palette=PALETTE, ax=ax)
        ax.set_title(f"Jumlah per {selected_feature}", fontsize=12, fontweight="bold")
        ax.set_xlabel("Jumlah")
        ax.set_ylabel("")
        ax.legend(title="Attrition")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with right:
        fig, ax = plt.subplots(figsize=(6, max(4, len(emp_df[selected_feature].unique()) * 0.5)))
        pct_yes = counts[counts["Attrition"] == "Yes"].sort_values("pct", ascending=True)
        bars = ax.barh(pct_yes[selected_feature], pct_yes["pct"], color=COLOR_YES, edgecolor="white")
        ax.bar_label(bars, fmt="%.1f%%", padding=4, fontsize=10)
        ax.set_xlabel("Attrition Rate (%)")
        ax.set_title(f"Attrition Rate per {selected_feature}", fontsize=12, fontweight="bold")
        ax.set_xlim(0, pct_yes["pct"].max() * 1.3 if not pct_yes.empty else 100)
        sns.despine(left=True, bottom=True)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # Value counts table
    st.markdown("**Tabel Frekuensi**")
    pivot = counts.pivot_table(index=selected_feature, columns="Attrition", values="count", fill_value=0)
    pivot["Total"] = pivot.sum(axis=1)
    if "Yes" in pivot.columns:
        pivot["Attrition Rate (%)"] = (pivot["Yes"] / pivot["Total"] * 100).round(1)
    st.dataframe(pivot.style.format({"Attrition Rate (%)": "{:.1f}"}), use_container_width=True)

st.divider()

# ── Korelasi Attrition (top numeric features) ─────────────────────────────────
st.subheader("📈 Faktor yang Paling Berkorelasi dengan Attrition")
numeric_cols = emp_df.select_dtypes(include=np.number).columns.tolist()
numeric_cols = [c for c in numeric_cols if c not in {"EmployeeNumber"}]

if len(numeric_cols) >= 2:
    temp = emp_df.copy()
    temp["Attrition_bin"] = (temp["Attrition"] == "Yes").astype(int)
    corr = temp[numeric_cols + ["Attrition_bin"]].corr()["Attrition_bin"].drop("Attrition_bin")
    corr = corr.dropna().sort_values()

    fig, ax = plt.subplots(figsize=(9, max(3, len(corr) * 0.4)))
    colors_bar = [COLOR_YES if v > 0 else COLOR_NO for v in corr.values]
    ax.barh(corr.index, corr.values, color=colors_bar, edgecolor="white")
    ax.axvline(0, color="gray", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Koefisien Korelasi Pearson")
    ax.set_title("Korelasi Fitur Numerik terhadap Attrition", fontsize=13, fontweight="bold")
    patch_pos = mpatches.Patch(color=COLOR_YES, label="Positif (↑ risiko attrition)")
    patch_neg = mpatches.Patch(color=COLOR_NO,  label="Negatif (↓ risiko attrition)")
    ax.legend(handles=[patch_pos, patch_neg], fontsize=10)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
else:
    st.info("Tidak cukup kolom numerik untuk analisis korelasi.")

st.divider()

# ── Raw data (collapsed) ──────────────────────────────────────────────────────
with st.expander("📄 Lihat Data Mentah"):
    st.dataframe(emp_df, use_container_width=True)
    st.caption(f"Total: {len(emp_df):,} baris × {emp_df.shape[1]} kolom")
