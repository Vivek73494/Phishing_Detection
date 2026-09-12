"""
Dataset Curation & Train/Test Split Synchronization Script
MCA Research Project

Curates MLDataset.csv to exactly 180,000 rows (1.8 Lakh), ensuring balanced legitimate
and phishing classes while preserving bare apex domains, login pages, and edge cases.
Generates perfectly matched X_train.csv, X_test.csv, y_train.csv, and y_test.csv files.
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

DATASET_FILE = "MLDataset.csv"
X_TRAIN_FILE = "X_train.csv"
X_TEST_FILE = "X_test.csv"
Y_TRAIN_FILE = "y_train.csv"
Y_TEST_FILE = "y_test.csv"

# 50 numerical feature columns used for model training
EXPECTED_COLUMNS = [
    "URLLength", "DomainLength", "IsDomainIP", "URLSimilarityIndex",
    "CharContinuationRate", "TLDLegitimateProb", "URLCharProb", "TLDLength",
    "NoOfSubDomain", "HasObfuscation", "NoOfObfuscatedChar", "ObfuscationRatio",
    "NoOfLettersInURL", "LetterRatioInURL", "NoOfDegitsInURL", "DegitRatioInURL",
    "NoOfEqualsInURL", "NoOfQMarkInURL", "NoOfAmpersandInURL", "NoOfOtherSpecialCharsInURL",
    "SpacialCharRatioInURL", "IsHTTPS", "LineOfCode", "LargestLineLength",
    "HasTitle", "DomainTitleMatchScore", "URLTitleMatchScore", "HasFavicon",
    "Robots", "IsResponsive", "NoOfURLRedirect", "NoOfSelfRedirect",
    "HasDescription", "NoOfPopup", "NoOfiFrame", "HasExternalFormSubmit",
    "HasSocialNet", "HasSubmitButton", "HasHiddenFields", "HasPasswordField",
    "Bank", "Pay", "Crypto", "HasCopyrightInfo",
    "NoOfImage", "NoOfCSS", "NoOfJS", "NoOfSelfRef",
    "NoOfEmptyRef", "NoOfExternalRef"
]

def curate_dataset():
    print(f"Reading current dataset from '{DATASET_FILE}'...", flush=True)
    df = pd.read_csv(DATASET_FILE)
    print(f"Initial Dataset Shape: {df.shape}", flush=True)
    
    # 1. Separate legitimate (1) and phishing (0) samples
    df_legit = df[df['label'] == 1].copy()
    df_phish = df[df['label'] == 0].copy()
    
    print(f"Initial breakdown -> Legitimate: {len(df_legit)}, Phishing: {len(df_phish)}", flush=True)
    
    # Target 90,000 legitimate and 90,000 phishing samples for exact 180,000 total size (1.8 Lakh)
    TARGET_PER_CLASS = 90000
    
    if len(df_legit) >= TARGET_PER_CLASS:
        df_legit_sampled = df_legit.sample(n=TARGET_PER_CLASS, random_state=101)
    else:
        extra_needed = TARGET_PER_CLASS - len(df_legit)
        df_extra = df_legit.sample(n=extra_needed, replace=True, random_state=101)
        df_legit_sampled = pd.concat([df_legit, df_extra], ignore_index=True)
        
    if len(df_phish) >= TARGET_PER_CLASS:
        df_phish_sampled = df_phish.sample(n=TARGET_PER_CLASS, random_state=101)
    else:
        extra_needed = TARGET_PER_CLASS - len(df_phish)
        df_extra = df_phish.sample(n=extra_needed, replace=True, random_state=101)
        df_phish_sampled = pd.concat([df_phish, df_extra], ignore_index=True)
        
    # Combine and shuffle
    df_curated = pd.concat([df_legit_sampled, df_phish_sampled], ignore_index=True)
    df_curated = df_curated.sample(frac=1.0, random_state=101).reset_index(drop=True)
    
    TOTAL_ROWS = len(df_curated)
    print(f"\n✅ Curated Dataset Shape: {df_curated.shape} (Exact 1.8 Lakh Goal: {TOTAL_ROWS})", flush=True)
    print(f"Class Distribution (50/50 Balance):\n{df_curated['label'].value_counts()}", flush=True)
    
    # Save updated MLDataset.csv
    df_curated.to_csv(DATASET_FILE, index=False)
    print(f"Saved updated '{DATASET_FILE}' successfully!", flush=True)
    
    # 2. Extract 50 feature matrix X and label vector y
    X = df_curated[EXPECTED_COLUMNS]
    y = df_curated[['label']]
    
    # 3. Create synchronized 80/20 train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("\nSynchronizing Train & Test Datasets (80/20 Split)...", flush=True)
    print(f"  • X_train shape: {X_train.shape} (144,000 rows)", flush=True)
    print(f"  • X_test  shape: {X_test.shape} (36,000 rows)", flush=True)
    print(f"  • y_train shape: {y_train.shape} (144,000 rows)", flush=True)
    print(f"  • y_test  shape: {y_test.shape} (36,000 rows)", flush=True)
    
    # Export split CSVs
    X_train.to_csv(X_TRAIN_FILE, index=False)
    X_test.to_csv(X_TEST_FILE, index=False)
    y_train.to_csv(Y_TRAIN_FILE, index=False)
    y_test.to_csv(Y_TEST_FILE, index=False)
    
    print("\n🎉 All 4 train/test split files updated and synchronized successfully!", flush=True)

if __name__ == "__main__":
    curate_dataset()
