# -*- coding: utf-8 -*-
"""UAS DS01

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1O3weK2xBKmLvqLg0wDt7FpwY8FGLpuZZ

# 1.Pengumpulan Data
"""

import pandas as pd
import numpy as np

file_path = "/content/water_potability.csv"
water_data = pd.read_csv(file_path)

water_data.head()

water_data.tail()

"""# 2.Menelaah Data"""

water_data.info()

water_data.describe()

water_data.nunique()

water_data.value_counts()

"""# 3.Validasi dan Visualisasi Data

## VALIDASI
"""

import matplotlib.pyplot as plt
import seaborn as sns

water_data.duplicated().sum()

water_data.isnull().sum()

water_data.loc[:, water_data.isnull().any()].columns

columns_with_missing = ['ph', 'Sulfate', 'Trihalomethanes']

for col in columns_with_missing:
    water_data[col] = water_data[col].fillna(water_data[col].mean())

print(water_data[columns_with_missing].isnull().sum())

numerical_cols = water_data.select_dtypes(include=['float64', 'int64']).columns

plt.figure(figsize=(15, 10))
sns.boxplot(data=water_data[numerical_cols], orient='h', palette="Set2")
plt.title("Boxplot untuk Semua Kolom Numerik")
plt.show()

data_iqr = water_data.copy()
for col in water_data.select_dtypes(include=['int64', 'float64']).columns:
    if col not in ['Potability']:  # Kecualikan kolom bertipe kategorikal
        Q1 = water_data[col].quantile(0.25)
        Q3 = water_data[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Ganti outliers dengan batas bawah/atas
        data_iqr[col] = water_data[col].apply(lambda x: lower_bound if x < lower_bound else (upper_bound if x > upper_bound else x))
        print(f"Outliers pada kolom '{col}' telah ditangani menggunakan metode IQR.")

numerical_cols = data_iqr.select_dtypes(include=['float64', 'int64']).columns

plt.figure(figsize=(15, 10))
sns.boxplot(data=data_iqr[numerical_cols], orient='h', palette="Set2")
plt.title("Boxplot untuk Semua Kolom Numerik Setelah Penanganan Outliers")

"""## VISUALISASI"""

# Hitung jumlah data untuk setiap kelas 'Potability'
potability_counts_before = water_data['Potability'].value_counts()

# Buat bar plot
plt.figure(figsize=(8, 6))
sns.barplot(x=potability_counts_before.index, y=potability_counts_before.values)
plt.title('Distribusi Data Kualitas Air Sebelum Resampling')
plt.xlabel('Potability')
plt.ylabel('Jumlah Data')
plt.show()

from imblearn.over_sampling import SMOTE

# Pisahkan fitur dan target
X = water_data.drop('Potability', axis=1)
y = water_data['Potability']

# Lakukan oversampling menggunakan SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Gabungkan kembali fitur dan target yang telah di-resampling
water_data_resampled = pd.DataFrame(X_resampled, columns=X.columns)
water_data_resampled['Potability'] = y_resampled

# Data sebelum resampling (ganti dengan data Anda)
potability_counts_before = water_data['Potability'].value_counts()

# Data setelah resampling (ganti dengan data Anda)
potability_counts_after = water_data_resampled['Potability'].value_counts()

fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # 1 baris, 2 kolom

# Bar plot sebelum resampling
axes[0].bar(potability_counts_before.index, potability_counts_before.values, color=['green', 'blue'])
axes[0].set_title('Distribusi Data Kualitas Air Sebelum Resampling')
axes[0].set_xlabel('Potability')
axes[0].set_ylabel('Jumlah Data')
axes[0].set_xticks([0, 1])  # Menetapkan label sumbu-x (kategori 0 dan 1)

# Bar plot setelah resampling
axes[1].bar(potability_counts_after.index, potability_counts_after.values, color=['green', 'blue'])
axes[1].set_title('Distribusi Data Kualitas Air Setelah Resampling')
axes[1].set_xlabel('Potability')
axes[1].set_ylabel('Jumlah Data')
axes[1].set_xticks([0, 1])  # Menetapkan label sumbu-x (kategori 0 dan 1)

plt.tight_layout()  # Mengatur layout agar subplot tidak saling tumpang tindih
plt.show()  # Menampilkan plot

"""# 4.Menentukan Object"""

water_data.head()

water_data_target = water_data.drop('Potability', axis=1)

water_data_target.head()

water_data_target.info()

water_data.shape

"""# 5.Membersihkan Data"""

corr_matrix = water_data.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Korelasi Heatmap untuk Data Water Potability")
plt.show()

# Tentukan kolom numerik
numerical_cols = water_data.select_dtypes(include=['float64', 'int64']).columns
numerical_cols = numerical_cols[numerical_cols != 'Potability']

fig, axes = plt.subplots(len(numerical_cols) // 3, 3, figsize=(15, 15)) # 3 kolom, atur figsize sesuai kebutuhan
axes = axes.flatten()

for i, col in enumerate(numerical_cols):
       sns.histplot(data=water_data, x=col, bins=30, kde=True, ax=axes[i]) # y=col untuk histogram horizontal
       axes[i].set_title(f'Distribusi {col}')
       axes[i].set_xlabel(col)
       axes[i].set_ylabel('Frekuensi')

plt.tight_layout()
plt.show()

"""#6.Konstruksi Data"""

water_data.info()

water_data_target.info()

water_data_resampled.info()

"""# 7.Pemodelan"""

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,recall_score,f1_score,precision_score,roc_auc_score,confusion_matrix,precision_score

X = water_data_resampled.drop('Potability', axis=1)
y = water_data_resampled['Potability']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Naive Bayes
nb_model = GaussianNB()
nb_model.fit(X_train, y_train)

# Decision Tree
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)

# Random Forest
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Naive Bayes
nb_pred = nb_model.predict(X_test)
nb_accuracy = accuracy_score(y_test, nb_pred)
nb_cm = confusion_matrix(y_test, nb_pred)

# Decision Tree
dt_pred = dt_model.predict(X_test)
dt_accuracy = accuracy_score(y_test, dt_pred)
dt_cm = confusion_matrix(y_test, dt_pred)

# Random Forest
rf_pred = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_pred)
rf_cm = confusion_matrix(y_test, rf_pred)

print(confusion_matrix(y_test, nb_pred))
print('-'*60)
print(classification_report(y_test, nb_pred))

print(confusion_matrix(y_test, dt_pred))
print('-'*60)
print(classification_report(y_test, dt_pred))

print(confusion_matrix(y_test, rf_pred))
print('-'*60)
print(classification_report(y_test, rf_pred))

def print_confusion_matrix(cm, model_name):
    cm_df = pd.DataFrame(cm, index=['Not Potable', 'Potable'], columns=['Not Potable', 'Potable'])
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm_df, annot=True, fmt="d", cmap="Blues")
    plt.title(f"Confusion Matrix - {model_name}")
    plt.ylabel("Actual")
    plt.xlabel("Predicted")
    plt.show()

# Cetak confusion matrix dengan label
print_confusion_matrix(nb_cm, "Logistic Regression")
print_confusion_matrix(dt_cm, "Decision Tree")
print_confusion_matrix(rf_cm, "Random Forest")

"""# 8.Evaluasi"""

# Normalisasi data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Latih ulang model dengan data normalisasi
nb_model.fit(X_train_scaled, y_train)
dt_model.fit(X_train_scaled, y_train)
rf_model.fit(X_train_scaled, y_train)

# Prediksi dan hitung akurasi setelah normalisasi
nb_pred_scaled = nb_model.predict(X_test_scaled)
dt_pred_scaled = dt_model.predict(X_test_scaled)
rf_pred_scaled = rf_model.predict(X_test_scaled)

nb_accuracy_scaled = accuracy_score(y_test, nb_pred_scaled)
dt_accuracy_scaled = accuracy_score(y_test, dt_pred_scaled)
rf_accuracy_scaled = accuracy_score(y_test, rf_pred_scaled)

# Tampilkan hasil
print("Akurasi Sebelum Normalisasi:")
print("Naive Bayes:", nb_accuracy)
print("Decision Tree:", dt_accuracy)
print("Random Forest:", rf_accuracy)

print("\nAkurasi Setelah Normalisasi:")
print("Naive Bayes:", nb_accuracy_scaled)
print("Decision Tree:", dt_accuracy_scaled)
print("Random Forest:", rf_accuracy_scaled)

# Data sebelum normalisasi
model_comp1 = pd.DataFrame({'Model': ['Naive Bayes','Decision Tree','Random Forest'], 'Accuracy': [nb_accuracy*100, dt_accuracy*100, rf_accuracy*100]})

# Data setelah normalisasi
model_comp2 = pd.DataFrame({'Model': ['Naive Bayes','Decision Tree','Random Forest'], 'Accuracy': [nb_accuracy_scaled*100, dt_accuracy_scaled*100, rf_accuracy_scaled*100]})

fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # 1 baris, 2 kolom

# Bar plot sebelum normalisasi
bars1 = axes[0].bar(model_comp1['Model'], model_comp1['Accuracy'], color=['red', 'green', 'blue'])
axes[0].set_title('Akurasi kualitas air sebelum Normalisasi')
axes[0].set_xlabel('Model')
axes[0].set_ylabel('Accuracy (%)')
axes[0].set_xticks([0, 1, 2])  # Menetapkan label sumbu-x (kategori 0 dan 1)

# Bar plot setelah normalisasi
bars2 = axes[1].bar(model_comp2['Model'], model_comp2['Accuracy'], color=['red', 'green', 'blue'])
axes[1].set_title('Akurasi kualitas air sesudah Normalisasi')
axes[1].set_xlabel('Model')
axes[1].set_ylabel('Accuracy (%)')
axes[1].set_xticks([0, 1, 2])  # Menetapkan label sumbu-x (kategori 0 dan 1)

plt.tight_layout()  # Mengatur layout agar subplot tidak saling tumpang tindih

for bar in bars1.patches:
    yval = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

for bar in bars2.patches:
    yval = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

plt.show()  # Menampilkan plot

"""# 9.Kesimpulan

1. Tingkat Akurasi Setiap Algoritma

Algoritma	Akurasi

Naive Bayes = 53,5%

Decision Tree = 60,75%

Random Forest = 70,75%

2. Keunggulan dan Keterbatasan

A. Naive Bayes:

Keunggulan: model yang sederhana, namun dapat bersaing dengan model algoritma lainnya.

Keterbatasan:

memiliki masalah probabilitas nol, terutama saat Anda menemukan kata-kata dalam data pengujian untuk kelas tertentu yang tidak ada dalam data pelatihan.

B. Decision Tree:

Keunggulan: Mudah diinterpretasi, dapat menangani data non-linear dan kategorikal.

Keterbatasan: Rentan terhadap overfitting, sensitif terhadap perubahan kecil dalam data.

C. Random Forest:

Keunggulan: Akurasi tinggi, robust terhadap overfitting, dapat menangani data non-linear.

Keterbatasan: Lebih kompleks, interpretasi model lebih sulit, komputasi lebih mahal.

3. Rekomendasi Algoritma

Berdasarkan hasil analisis, Random Forest direkomendasikan sebagai algoritma yang paling efektif untuk memprediksi kualitas air dalam kasus ini.

Alasan:

Akurasi Tinggi: Random Forest mencapai akurasi tertinggi (70,75%) di antara algoritma yang diuji.

Robust: Algoritma ini relatif robust terhadap overfitting karena menggunakan ensemble learning dengan menggabungkan beberapa decision tree.

Penanganan Data Non-linear: Random Forest dapat memodelkan hubungan non-linear antara fitur dan target, yang penting dalam kasus kualitas air.

Meskipun Random Forest memiliki komputasi yang lebih mahal dibandingkan beberapa algoritma lain, akurasi dan robustness-nya menjadikannya pilihan optimal untuk prediksi kualitas air.
"""
