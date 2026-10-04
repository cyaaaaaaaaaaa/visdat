# ============================================================
# PREPROCESSING DATA IHK 38 PROVINSI - UAS VISUALISASI
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


# ============================================================
# 1. PATH FILE
# ============================================================

# >>> NANTI CUKUP GANTI BAGIAN INI <<<
INPUT_FILE = Path(
    r"D:/SEM 6/VISDAT/UAS/IHK_38_Provinsi_2025_Cleaned.xlsx"
)

OUTPUT_DIR = INPUT_FILE.parent / "hasil_preprocessing_IHK"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_EXCEL = OUTPUT_DIR / "IHK_38_Provinsi_2025_Preprocessed.xlsx"


# ============================================================
# 2. MEMBACA DATA
# ============================================================

print("=" * 60)
print("MEMBACA DATA")
print("=" * 60)

xls = pd.ExcelFile(INPUT_FILE)

print("Sheet yang tersedia:")
print(xls.sheet_names)

# Data utama hasil cleaning
df = pd.read_excel(
    INPUT_FILE,
    sheet_name="Subkelompok_Wide"
)

# Kamus variabel
kamus = pd.read_excel(
    INPUT_FILE,
    sheet_name="Kamus_Variabel"
)

print("\nUkuran data awal:", df.shape)
print(df.head())


# ============================================================
# 3. MEMBERSIHKAN NAMA PROVINSI
# ============================================================

df["Provinsi"] = (
    df["Provinsi"]
    .astype(str)
    .str.strip()
)

# Hapus baris header yang tidak sengaja terbaca sebagai data
df = df[
    df["Provinsi"].str.lower() != "provinsi"
].copy()

# Reset index
df.reset_index(drop=True, inplace=True)

print("\nJumlah provinsi:", len(df))

if len(df) != 38:
    print(
        "WARNING: jumlah provinsi bukan 38. "
        "Cek kembali file input."
    )


# ============================================================
# 4. MENENTUKAN VARIABEL NUMERIK
# ============================================================

id_col = "Provinsi"

feature_cols = [
    col for col in df.columns
    if col != id_col
]

# Pastikan seluruh variabel numerik
for col in feature_cols:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

print("\nJumlah variabel:", len(feature_cols))


# ============================================================
# 5. CEK MISSING VALUE
# ============================================================

print("\n" + "=" * 60)
print("CEK MISSING VALUE")
print("=" * 60)

missing = pd.DataFrame({
    "Variabel": feature_cols,
    "Jumlah_NA": [
        df[col].isna().sum()
        for col in feature_cols
    ]
})

missing["Persen_NA"] = (
    missing["Jumlah_NA"]
    / len(df)
    * 100
).round(2)

missing = missing.sort_values(
    "Persen_NA",
    ascending=False
)

print(missing.to_string(index=False))


# ============================================================
# 6. MENENTUKAN VARIABEL YANG LAYAK DIPAKAI
# ============================================================

# Variabel dengan >50% missing tidak digunakan
MAX_MISSING_PERCENT = 50

usable_features = missing[
    missing["Persen_NA"] <= MAX_MISSING_PERCENT
]["Variabel"].tolist()

dropped_features = missing[
    missing["Persen_NA"] > MAX_MISSING_PERCENT
]["Variabel"].tolist()

print("\n" + "=" * 60)
print("SELEKSI VARIABEL")
print("=" * 60)

print(
    f"Variabel awal       : {len(feature_cols)}"
)

print(
    f"Variabel digunakan   : {len(usable_features)}"
)

print(
    f"Variabel dibuang     : {len(dropped_features)}"
)

if dropped_features:
    print("\nVariabel yang dibuang:")
    for col in dropped_features:
        print("-", col)


# ============================================================
# 7. DATASET SUBKELOMPOK ASLI
# ============================================================

# Ini adalah data asli yang tidak diimputasi.
# Dipakai untuk hierarchy supaya tidak mengubah nilai BPS.

df_original = df[
    [id_col] + usable_features
].copy()


# ============================================================
# 8. IMPUTASI MISSING VALUE
# ============================================================

print("\n" + "=" * 60)
print("IMPUTASI MISSING VALUE")
print("=" * 60)

X = df[usable_features].copy()

# Median dipilih karena lebih tahan terhadap outlier
# dibandingkan mean.
imputer = SimpleImputer(
    strategy="median"
)

X_imputed = pd.DataFrame(
    imputer.fit_transform(X),
    columns=usable_features
)

# Gabungkan kembali nama provinsi
df_imputed = pd.concat(
    [
        df[[id_col]].reset_index(drop=True),
        X_imputed.reset_index(drop=True)
    ],
    axis=1
)

print(
    "Jumlah NA setelah imputasi:",
    int(df_imputed[usable_features].isna().sum().sum())
)


# ============================================================
# 9. STANDARDISASI Z-SCORE
# ============================================================

print("\n" + "=" * 60)
print("STANDARDISASI")
print("=" * 60)

scaler = StandardScaler()

X_scaled = pd.DataFrame(
    scaler.fit_transform(
        df_imputed[usable_features]
    ),
    columns=usable_features
)

df_standardized = pd.concat(
    [
        df_imputed[[id_col]].reset_index(drop=True),
        X_scaled.reset_index(drop=True)
    ],
    axis=1
)

print(
    "Data standardized:",
    df_standardized.shape
)


# ============================================================
# 10. FLAG DATA YANG DIIMPUTASI
# ============================================================

flag_imputation = df[[id_col]].copy()

for col in usable_features:

    flag_imputation[
        col + "_imputed"
    ] = df[col].isna()

# Jumlah nilai yang diimputasi per provinsi
flag_imputation["Jumlah_Diimputasi"] = (
    flag_imputation
    .drop(columns=[id_col])
    .sum(axis=1)
)

print("\nJumlah imputasi per provinsi:")
print(
    flag_imputation[
        [id_col, "Jumlah_Diimputasi"]
    ].to_string(index=False)
)


# ============================================================
# 11. DATA LONG UNTUK HIERARCHY
# ============================================================

print("\n" + "=" * 60)
print("MEMBUAT DATA HIERARCHY")
print("=" * 60)

df_long = df_original.melt(
    id_vars=[id_col],
    var_name="Subkelompok",
    value_name="IHK_RataRata_2025"
)

# Buang nilai yang memang tidak tersedia
df_long = df_long.dropna(
    subset=["IHK_RataRata_2025"]
).copy()


# ============================================================
# 12. HUBUNGKAN DENGAN KAMUS VARIABEL
# ============================================================

# Pastikan nama kolom kamus sesuai
if {
    "Kelompok",
    "Subkelompok"
}.issubset(kamus.columns):

    kamus_join = kamus[
        ["Kelompok", "Subkelompok"]
    ].drop_duplicates()

    df_long = df_long.merge(
        kamus_join,
        on="Subkelompok",
        how="left"
    )

    # Urutan kolom
    df_long = df_long[
        [
            "Provinsi",
            "Kelompok",
            "Subkelompok",
            "IHK_RataRata_2025"
        ]
    ]

else:
    print(
        "WARNING: kolom Kelompok/Subkelompok "
        "tidak ditemukan pada Kamus_Variabel."
    )


# ============================================================
# 13. AUDIT FINAL
# ============================================================

audit = pd.DataFrame({
    "Informasi": [
        "Jumlah provinsi",
        "Jumlah variabel awal",
        "Jumlah variabel digunakan",
        "Jumlah variabel dibuang",
        "Jumlah NA sebelum imputasi",
        "Jumlah NA sesudah imputasi",
        "Jumlah baris hierarchy",
        "Metode imputasi",
        "Standardisasi"
    ],

    "Nilai": [
        len(df),
        len(feature_cols),
        len(usable_features),
        len(dropped_features),
        int(
            df[feature_cols]
            .isna()
            .sum()
            .sum()
        ),
        int(
            df_imputed[usable_features]
            .isna()
            .sum()
            .sum()
        ),
        len(df_long),
        "Median per variabel",
        "Z-score / StandardScaler"
    ]
})


# ============================================================
# 14. SIMPAN EXCEL FINAL
# ============================================================

print("\n" + "=" * 60)
print("MENYIMPAN HASIL")
print("=" * 60)

with pd.ExcelWriter(
    OUTPUT_EXCEL,
    engine="openpyxl"
) as writer:

    df_original.to_excel(
        writer,
        sheet_name="01_Data_Asli",
        index=False
    )

    df_imputed.to_excel(
        writer,
        sheet_name="02_Data_Imputed",
        index=False
    )

    df_standardized.to_excel(
        writer,
        sheet_name="03_Data_Standard",
        index=False
    )

    df_long.to_excel(
        writer,
        sheet_name="04_Hierarchy_Long",
        index=False
    )

    flag_imputation.to_excel(
        writer,
        sheet_name="05_Flag_Imputasi",
        index=False
    )

    missing.to_excel(
        writer,
        sheet_name="06_Audit_Missing",
        index=False
    )

    kamus.to_excel(
        writer,
        sheet_name="07_Kamus_Variabel",
        index=False
    )

    audit.to_excel(
        writer,
        sheet_name="08_Audit_Final",
        index=False
    )


# ============================================================
# 15. SIMPAN CSV
# ============================================================

df_original.to_csv(
    OUTPUT_DIR / "01_data_asli.csv",
    index=False
)

df_imputed.to_csv(
    OUTPUT_DIR / "02_data_imputed.csv",
    index=False
)

df_standardized.to_csv(
    OUTPUT_DIR / "03_data_standardized.csv",
    index=False
)

df_long.to_csv(
    OUTPUT_DIR / "04_hierarchy_long.csv",
    index=False
)

flag_imputation.to_csv(
    OUTPUT_DIR / "05_flag_imputasi.csv",
    index=False
)

missing.to_csv(
    OUTPUT_DIR / "06_audit_missing.csv",
    index=False
)

kamus.to_csv(
    OUTPUT_DIR / "07_kamus_variabel.csv",
    index=False
)


# ============================================================
# 16. SELESAI
# ============================================================

print("\n" + "=" * 60)
print("PREPROCESSING SELESAI")
print("=" * 60)

print(
    f"""
Output folder:
{OUTPUT_DIR}

Excel:
{OUTPUT_EXCEL}

Data siap PCA/network:
03_data_standardized.csv

Data siap hierarchy:
04_hierarchy_long.csv
"""
)