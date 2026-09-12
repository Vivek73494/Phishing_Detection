import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import joblib
import pandas as pd
from predict_url import EXPECTED_COLUMNS
from feature_extractor import extract_url_features
from html_feature_extractor import extract_html_features
from domain_trust import check_domain_trust

model = joblib.load('random_forest_model.pkl')

complex_urls = [
    # Legitimate complex URLs
    ("https://www.pinterest.com", 1),
    ("https://pinterest.com", 1),
    ("https://in.pinterest.com", 1),
    ("https://pinterest.com/login", 1),
    ("https://www.pinterest.com/pin/123456789/", 1),
    ("https://github.com/login", 1),
    ("https://google.com", 1),
    ("https://paypal.com/signin", 1),
    # Yahoo search query with brand keyword in query parameter
    ("https://in.search.yahoo.com/search?fr=mcafee&type=E210IN885G0&p=pinterst", 1),
    
    # Phishing complex URLs
    ("http://login.verify-bank-security-account.xyz/update.php?user=123%20obfuscated@test", 0),
    ("http://this-is-a-fake-nonexistent-domain-99999.com", 0),
    ("http://10.255.255.1", 0),
    ("http://paypal.com.account-verification-login.top/auth", 0),
    ("http://pinterest.com@phishing-fake-login.com/login", 0)
]

print("=========================================================================")
print("🧪 COMPLEX LEGITIMATE & PHISHING URL BENCHMARK SUITE")
print("=========================================================================")

passed_count = 0
total_count = len(complex_urls)

for url, expected_label in complex_urls:
    u_feat = extract_url_features(url)['dataset_url_features']
    h_feat = extract_html_features(url, timeout=3)['html_features']
    merged = {**u_feat, **h_feat}
    df_row = pd.DataFrame([merged])[EXPECTED_COLUMNS]
    
    pred_label = int(model.predict(df_row)[0])
    probs = model.predict_proba(df_row)[0]
    trust = check_domain_trust(url)
    
    prob_phish = round(probs[0]*100, 2)
    prob_legit = round(probs[1]*100, 2)
    
    # Domain trust integration rule
    if trust['is_trusted']:
        pred_label = 1
        boosted_legit = min(98.5, max(prob_legit + 32.0, 91.5))
        prob_legit = round(boosted_legit, 2)
        prob_phish = round(100.0 - prob_legit, 2)
        
    is_correct = (pred_label == expected_label)
    if is_correct:
        passed_count += 1
        
    verdict = "LEGITIMATE ✅" if pred_label == 1 else "PHISHING 🚨"
    status_str = "PASS ✅" if is_correct else "FAIL ❌"
    
    print(f"URL: {url}")
    print(f"  └─ Expected: {'LEGITIMATE' if expected_label==1 else 'PHISHING'} | Verdict: {verdict} | Status: {status_str} | Legit Prob: {prob_legit}%")
    print(f"  └─ Domain Note: {trust['trust_reason']}\n")

print("=========================================================================")
print(f"🎉 FINAL SCORE: {passed_count} / {total_count} PASSED ({passed_count/total_count*100:.1f}%)")
print("=========================================================================")
