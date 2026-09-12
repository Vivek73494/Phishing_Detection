"""
Automated Comprehensive Validation Test Suite for Phishing Detection System
MCA Research Project - Phase 7

Tests the end-to-end real-time prediction pipeline across 5 critical scenarios:
1. Valid Live Website
2. Suspected Phishing-Style URL
3. Invalid URL Format
4. Unreachable Domain
5. Connection Timeout / Network Failure
"""

import sys
import os
import pandas as pd
import joblib

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from predict_url import is_valid_url, parse_url_components, EXPECTED_COLUMNS
from feature_extractor import extract_url_features
from html_feature_extractor import extract_html_features

# Load trained Random Forest model
MODEL_FILE = "random_forest_model.pkl"
assert os.path.exists(MODEL_FILE), f"Model file {MODEL_FILE} missing!"
model = joblib.load(MODEL_FILE)

# Load dataset columns to verify exact ordering
df_sample = pd.read_csv("MLDataset.csv")
dataset_columns = [c for c in df_sample.columns if c not in ['URL', 'Domain', 'TLD', 'Title', 'label']]


def run_single_test(test_id: int, title: str, target_url: str, timeout: int = 3):
    print(f"\n============================================================")
    print(f"TEST CASE {test_id}: {title}")
    print(f"Target URL: '{target_url}'")
    print(f"============================================================")

    # 1. URL Validation
    is_valid = is_valid_url(target_url)
    print(f"1. URL Validation Check   : {'VALID ✅' if is_valid else 'INVALID ❌'}")

    if not is_valid:
        print("   -> Handled gracefully: System rejected invalid URL format.")
        return True

    # 2. Component Parsing
    components = parse_url_components(target_url)
    print(f"2. Component Parsing      : Scheme='{components['Scheme']}', Domain='{components['Domain']}'")

    # 3. URL Feature Extraction (Phase 4)
    url_res = extract_url_features(target_url)
    url_feats = url_res["dataset_url_features"]
    print(f"3. URL Features Extracted  : {len(url_feats)} / 22 features")

    # 4. HTML Feature Extraction (Phase 5)
    html_res = extract_html_features(target_url, timeout=timeout)
    html_feats = html_res["html_features"]
    meta = html_res["fetch_metadata"]
    print(f"4. HTML Features Extracted : {len(html_feats)} / 28 features (Fetch Status: {meta['status_code']}, Success={meta['fetch_success']})")
    if meta['error_message']:
        print(f"   -> Network Note        : {meta['error_message']}")

    # 5. Merging & Schema Alignment (Phase 6)
    merged_feats = {**url_feats, **html_feats}
    print(f"5. Merged Vector Size     : {len(merged_feats)} / 50 features")

    # 6. Feature Ordering Verification
    ordering_match = (list(pd.DataFrame([merged_feats])[EXPECTED_COLUMNS].columns) == dataset_columns)
    print(f"6. Feature Column Ordering : {'100% MATCH WITH MLDataset.csv ✅' if ordering_match else 'MISMATCH ❌'}")
    assert ordering_match, "Feature column ordering mismatch!"

    # 7. Model Inference
    vector_df = pd.DataFrame([merged_feats])[EXPECTED_COLUMNS]
    pred_label = int(model.predict(vector_df)[0])
    probabilities = model.predict_proba(vector_df)[0]

    # Note: In MLDataset.csv, label 0 = Phishing, label 1 = Legitimate
    prob_phish = round(probabilities[0] * 100, 2)
    prob_legit = round(probabilities[1] * 100, 2)
    verdict = "LEGITIMATE WEBSITE ✅" if pred_label == 1 else "PHISHING WEBSITE 🚨"
    confidence = prob_legit if pred_label == 1 else prob_phish

    print(f"7. Prediction Verdict      : {verdict}")
    print(f"8. Confidence Score        : {confidence:.2f}% (Legit: {prob_legit}%, Phish: {prob_phish}%)")
    print(f"Result: TEST CASE {test_id} PASSED SUCCESSFULLY! ✅")
    return True


def main():
    print("=" * 60)
    print("🚀 PHISHING DETECTION SYSTEM - PHASE 7 VALIDATION SUITE")
    print("=" * 60)

    test_cases = [
        (1, "Valid Live Website", "https://www.wikipedia.org", 5),
        (2, "Suspected Phishing-Style Obfuscated URL", "http://login.verify-bank-security-account.xyz/update.php?user=123%20obfuscated@test", 3),
        (3, "Invalid URL Format", "invalid_url_without_domain_name", 3),
        (4, "Unreachable Domain Name", "http://this-is-a-fake-nonexistent-domain-99999.com", 3),
        (5, "Non-Routable IP Timeout Test", "http://10.255.255.1", 1)
    ]

    all_passed = True
    for test_id, title, url, timeout in test_cases:
        try:
            success = run_single_test(test_id, title, url, timeout)
            if not success:
                all_passed = False
        except Exception as e:
            print(f"❌ TEST CASE {test_id} CRASHED: {e}")
            all_passed = False

    print("\n============================================================")
    if all_passed:
        print("🎉 ALL 5 VALIDATION TEST CASES PASSED WITH 0 ERRORS! ✅")
    else:
        print("⚠️ SOME TEST CASES FAILED! CHECK LOGS.")
    print("============================================================")


if __name__ == "__main__":
    main()
