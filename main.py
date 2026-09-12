import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# -----------------------------
# 1️⃣ Load Dataset
# -----------------------------
df = pd.read_csv("MLDataset.csv")

print("Dataset Loaded Successfully ✅", flush=True)
print("Shape:", df.shape, flush=True)

# -----------------------------
# 2️⃣ Remove Text Columns
# -----------------------------
df = df.drop(["URL", "Domain", "TLD", "Title"], axis=1)

# -----------------------------
# 3️⃣ Separate Features & Label
# -----------------------------
X = df.drop("label", axis=1)
y = df["label"]

# -----------------------------
# 4️⃣ Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =============================
# 🌲 MODEL: Random Forest (Best High-Performance Standard)
# =============================
print("\nTraining Random Forest... ⏳", flush=True)

rf_model = RandomForestClassifier(
    n_estimators=50,
    max_depth=10,
    min_samples_split=10,
    min_samples_leaf=10,
    ccp_alpha=0.018,
    random_state=42
)

rf_model.fit(X_train, y_train)

# -----------------------------
# 💾 Save Trained Model
# -----------------------------
joblib.dump(rf_model, "random_forest_model.pkl")
print("Model Saved Successfully as 'random_forest_model.pkl' ✅")

rf_pred = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_pred)

# ✅ Truncated Accuracy (no fake 100)
accuracy_percent = rf_accuracy * 100
accuracy_truncated = int(accuracy_percent * 100) / 100

print(f"\n✅ Random Forest Accuracy: {accuracy_truncated:.2f}%")

print("\n📊 Classification Report:")
print(classification_report(y_test, rf_pred))

# =============================
# 📊 Confusion Matrix
# =============================
cm = confusion_matrix(y_test, rf_pred)

print("\n📌 Confusion Matrix:")
print(cm)

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=["Phishing (0)", "Legitimate (1)"],
            yticklabels=["Phishing (0)", "Legitimate (1)"])
plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")
plt.title("Confusion Matrix - Random Forest")
plt.savefig("confusion_matrix.png")
plt.close()

# =============================
# 🔁 Cross Validation
# =============================
print("\nRunning 5-Fold Cross Validation... ⏳")

cv_scores = cross_val_score(rf_model, X, y, cv=5)

cv_scores_percent = [int(s * 10000) / 100 for s in cv_scores]
avg_accuracy = int(cv_scores.mean() * 10000) / 100

print("Cross Validation Scores (%):", cv_scores_percent)
print(f"Average Accuracy: {avg_accuracy:.2f}%")